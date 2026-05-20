import logging

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from extensions import mysql
from services.validators import validar_donacion

from services.juguetes_helpers import obtener_categorias_activas

juguetes_bp = Blueprint("juguetes", __name__)


@juguetes_bp.route("/donacion", methods=["GET", "POST"])
def donacion():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para registrar un juguete.", "warning")
        return redirect(url_for("auth.login", next=request.url))

    datos = {}

    categorias = obtener_categorias_activas()

    if request.method == "POST":

        datos = {
            "codigo_barras": request.form.get("codigo_barras", "").strip(),
            "donante_nombre": request.form.get("donante_nombre", "").strip(),
            "donante_correo": request.form.get("donante_correo", "").strip(),
            "donante_telefono": request.form.get("donante_telefono", "").strip(),
            "categoria_id": request.form.get("categoria_id", "").strip(),
            "descripcion": request.form.get("descripcion", "").strip(),
        }

        valido, errores = validar_donacion(request.form)

        if not valido:

            for error in errores:
                flash(error, "error")

            return render_template(
                "gestion_donacion.html", datos=datos, categorias=categorias
            )

        try:

            cur = mysql.connection.cursor()

            cur.execute(
                """
                SELECT id
                FROM juguetes
                WHERE codigo_barras = %s
                """,
                (datos["codigo_barras"],),
            )

            juguete_existente = cur.fetchone()

            if juguete_existente:

                cur.close()

                flash(
                    "Ya existe un juguete registrado con ese código de barras.",
                    "warning",
                )

                return render_template(
                    "gestion_donacion.html", datos=datos, categorias=categorias
                )

            cur.execute(
                """
                INSERT INTO juguetes (
                    codigo_barras,
                    nombre,
                    categoria_id,
                    descripcion,
                    donante_id,
                    donante_nombre,
                    donante_correo,
                    donante_telefono,
                    estado_actual
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    'registrado'
                )
                """,
                (
                    datos["codigo_barras"],
                    "Juguete donado",
                    datos["categoria_id"],
                    datos["descripcion"],
                    session.get("usuario_id"),
                    datos["donante_nombre"],
                    datos["donante_correo"],
                    datos["donante_telefono"] or None,
                ),
            )

            juguete_id = cur.lastrowid

            cur.execute(
                """
                INSERT INTO historial_estados_juguete (
                    juguete_id,
                    estado_anterior,
                    estado_nuevo,
                    observacion,
                    usuario_id
                )
                VALUES (
                    %s,
                    NULL,
                    'registrado',
                    %s,
                    %s
                )
                """,
                (
                    juguete_id,
                    "Juguete recibido y registrado en el sistema.",
                    session.get("usuario_id"),
                ),
            )

            mysql.connection.commit()

            cur.close()

            flash("Juguete registrado correctamente.", "success")

            return redirect(url_for("juguetes.historial"))

        except Exception as e:

            logging.exception("Error registrando juguete")

            flash(f"Error técnico al registrar juguete: {str(e)}", "error")

            return render_template(
                "gestion_donacion.html", datos=datos, categorias=categorias
            )

    return render_template("gestion_donacion.html", datos=datos, categorias=categorias)


@juguetes_bp.route("/historial")
def historial():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para consultar el historial.", "warning")
        return redirect(url_for("auth.login", next=request.url))

    estado = request.args.get("estado", "").strip()
    codigo_barras = request.args.get("codigo_barras", "").strip()
    donante = request.args.get("donante", "").strip()
    beneficiario = request.args.get("beneficiario", "").strip()

    page = request.args.get("page", 1, type=int)
    per_page = 6

    if page < 1:
        page = 1

    offset = (page - 1) * per_page

    try:
        cur = mysql.connection.cursor()

        base_from = """
            FROM juguetes j
            INNER JOIN categorias c ON c.id = j.categoria_id
            LEFT JOIN entregas e ON e.juguete_id = j.id
            LEFT JOIN beneficiarios b ON b.id = e.beneficiario_id
            WHERE 1 = 1
        """

        params = []

        if session.get("usuario_rol") != "admin":
            base_from += " AND j.donante_id = %s"
            params.append(session["usuario_id"])

        if estado:
            base_from += " AND j.estado_actual = %s"
            params.append(estado)

        if codigo_barras:
            base_from += " AND j.codigo_barras LIKE %s"
            params.append(f"%{codigo_barras}%")

        if donante:
            base_from += """
                AND (
                    j.donante_nombre LIKE %s
                    OR j.donante_correo LIKE %s
                    OR j.donante_telefono LIKE %s
                )
            """
            like_donante = f"%{donante}%"
            params.extend([like_donante, like_donante, like_donante])

        if beneficiario:
            base_from += """
                AND (
                    b.nombre LIKE %s
                    OR b.institucion LIKE %s
                )
            """
            like_beneficiario = f"%{beneficiario}%"
            params.extend([like_beneficiario, like_beneficiario])

        count_query = "SELECT COUNT(*) AS total " + base_from

        cur.execute(count_query, tuple(params))
        total = cur.fetchone()["total"]

        query = (
            """
            SELECT
                j.id,
                j.codigo_barras,
                j.nombre,
                j.descripcion,
                j.estado_actual,
                j.fecha_recepcion,
                j.donante_nombre,
                j.donante_correo,
                j.donante_telefono,

                c.nombre AS categoria_nombre,

                b.nombre AS beneficiario_nombre,
                b.edad AS beneficiario_edad,
                b.institucion AS beneficiario_institucion,
                e.lugar_entrega,
                e.fecha_entrega
        """
            + base_from
            + """
            ORDER BY j.fecha_recepcion DESC
            LIMIT %s OFFSET %s
        """
        )

        cur.execute(query, tuple(params + [per_page, offset]))
        juguetes = cur.fetchall()
        cur.close()

        total_pages = (total + per_page - 1) // per_page

        filtros = {
            "estado": estado,
            "codigo_barras": codigo_barras,
            "donante": donante,
            "beneficiario": beneficiario,
        }

        return render_template(
            "historial.html",
            juguetes=juguetes,
            filtros=filtros,
            page=page,
            total_pages=total_pages,
            total=total,
        )

    except Exception as e:
        logging.exception("Error cargando historial")
        flash(f"Error al cargar historial: {str(e)}", "error")

        return render_template(
            "historial.html",
            juguetes=[],
            filtros={},
            page=1,
            total_pages=0,
            total=0,
        )


@juguetes_bp.route("/juguetes/<int:juguete_id>/estado", methods=["POST"])
def actualizar_estado_juguete(juguete_id):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión.", "warning")
        return redirect(url_for("login"))

    if session.get("usuario_rol") != "admin":
        flash("No tienes permisos para actualizar estados.", "error")
        return redirect(url_for("juguetes.historial"))

    nuevo_estado = request.form.get("estado", "").strip()
    observacion = request.form.get("observacion", "").strip()

    estados_validos = [
        "registrado",
        "en_revision",
        "en_reparacion",
        "reparado",
        "listo_para_entrega",
        "entregado",
        "descartado",
    ]

    if nuevo_estado not in estados_validos:
        flash("Estado no válido.", "error")
        return redirect(url_for("juguetes.historial"))

    try:
        cur = mysql.connection.cursor()

        cur.execute("SELECT estado_actual FROM juguetes WHERE id = %s", (juguete_id,))
        juguete = cur.fetchone()

        if not juguete:
            cur.close()
            flash("El juguete no existe.", "error")
            return redirect(url_for("juguetes.historial"))

        estado_anterior = juguete["estado_actual"]

        cur.execute(
            "UPDATE juguetes SET estado_actual = %s WHERE id = %s",
            (nuevo_estado, juguete_id),
        )

        cur.execute(
            """
            INSERT INTO historial_estados_juguete (
                juguete_id,
                estado_anterior,
                estado_nuevo,
                observacion,
                usuario_id
            )
            VALUES (%s, %s, %s, %s, %s)
        """,
            (
                juguete_id,
                estado_anterior,
                nuevo_estado,
                observacion,
                session["usuario_id"],
            ),
        )

        if nuevo_estado == "entregado":
            beneficiario_nombre = request.form.get("beneficiario_nombre", "").strip()
            beneficiario_edad = request.form.get("beneficiario_edad", "").strip()
            beneficiario_institucion = request.form.get(
                "beneficiario_institucion", ""
            ).strip()
            lugar_entrega = request.form.get("lugar_entrega", "").strip()
            observaciones_entrega = request.form.get(
                "observaciones_entrega", ""
            ).strip()

            if not beneficiario_nombre or not lugar_entrega:
                mysql.connection.rollback()
                cur.close()
                flash(
                    "Para entregar el juguete debes ingresar beneficiario y lugar de entrega.",
                    "error",
                )
                return redirect(url_for("juguetes.historial"))

            cur.execute(
                """
                INSERT INTO beneficiarios (
                    nombre,
                    edad,
                    institucion,
                    observaciones
                )
                VALUES (%s, %s, %s, %s)
            """,
                (
                    beneficiario_nombre,
                    int(beneficiario_edad) if beneficiario_edad else None,
                    beneficiario_institucion or None,
                    observaciones_entrega or None,
                ),
            )

            beneficiario_id = cur.lastrowid

            cur.execute(
                """
                INSERT INTO entregas (
                    juguete_id,
                    beneficiario_id,
                    entregado_por_id,
                    lugar_entrega,
                    observaciones
                )
                VALUES (%s, %s, %s, %s, %s)
            """,
                (
                    juguete_id,
                    beneficiario_id,
                    session["usuario_id"],
                    lugar_entrega,
                    observaciones_entrega or None,
                ),
            )

        mysql.connection.commit()
        cur.close()

        flash("Estado actualizado correctamente.", "success")

    except Exception as e:
        logging.exception("Error actualizando estado")
        flash(f"Error al actualizar estado: {str(e)}", "error")

    return redirect(url_for("juguetes.historial"))


@juguetes_bp.route("/juguetes/<int:juguete_id>")
def detalle_juguete(juguete_id):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión.", "warning")
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT
            j.*,
            c.nombre AS categoria_nombre,
            b.nombre AS beneficiario_nombre,
            b.edad AS beneficiario_edad,
            b.institucion AS beneficiario_institucion,
            e.lugar_entrega,
            e.fecha_entrega,
            e.observaciones AS entrega_observaciones
        FROM juguetes j
        INNER JOIN categorias c ON c.id = j.categoria_id
        LEFT JOIN entregas e ON e.juguete_id = j.id
        LEFT JOIN beneficiarios b ON b.id = e.beneficiario_id
        WHERE j.id = %s
    """,
        (juguete_id,),
    )

    juguete = cur.fetchone()

    cur.execute(
        """
        SELECT
            h.estado_anterior,
            h.estado_nuevo,
            h.observacion,
            h.creado_en,
            u.primer_nombre,
            u.primer_apellido
        FROM historial_estados_juguete h
        INNER JOIN usuarios u ON u.id = h.usuario_id
        WHERE h.juguete_id = %s
        ORDER BY h.creado_en ASC
    """,
        (juguete_id,),
    )

    historial = cur.fetchall()
    cur.close()

    return render_template("detalle_juguete.html", juguete=juguete, historial=historial)
