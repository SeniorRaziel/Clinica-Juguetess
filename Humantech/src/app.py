from flask import Flask, render_template, redirect, request, session, url_for, flash, send_file
from flask_mysqldb import MySQL
import os
import logging

app = Flask(__name__, template_folder="templates")

app.secret_key = os.getenv("SECRET_KEY", "clinica-juguetes-secret")

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "127.0.0.1")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "123456789")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT", 3306))
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "clinica_juguetes")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

logging.basicConfig(filename="app.log", level=logging.ERROR)


@app.before_request
def before_request():
    try:
        mysql.connection.ping()
    except Exception as e:
        print("Error de reconexión:", e)


def usuario_actual_id():
    return session.get("usuario_id")


def login_requerido():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para continuar.", "warning")
        return False
    return True


def validar_registro(form):
    errores = []

    cedula = form.get("Cedula_Donante", "").strip()
    primer_nombre = form.get("primer_nombre", "").strip()
    primer_apellido = form.get("primer_apellido", "").strip()
    contacto = form.get("contacto", "").strip()
    clave = form.get("clave", "")
    clave2 = form.get("clave2", "")

    if not cedula:
        errores.append("La cédula es obligatoria.")
    elif not cedula.isdigit():
        errores.append("La cédula solo debe contener números.")
    elif len(cedula) < 6 or len(cedula) > 12:
        errores.append("La cédula debe tener entre 6 y 12 dígitos.")

    if not primer_nombre or len(primer_nombre) < 2:
        errores.append("El primer nombre debe tener mínimo 2 caracteres.")

    if not primer_apellido or len(primer_apellido) < 2:
        errores.append("El primer apellido debe tener mínimo 2 caracteres.")

    if not contacto or len(contacto) < 7:
        errores.append("El contacto debe tener mínimo 7 caracteres.")

    if not clave or len(clave) < 6:
        errores.append("La contraseña debe tener mínimo 6 caracteres.")

    if clave != clave2:
        errores.append("Las contraseñas no coinciden.")

    return len(errores) == 0, errores


def obtener_categoria_donacion(form):
    tipo = form.get("tipo_donacion", "")

    campos = {
        "carros": "categoria_carros",
        "munecas": "categoria_munecas",
        "balones": "categoria_balones",
        "otros": "categoria_otros",
    }

    campo = campos.get(tipo)
    return form.get(campo, "").strip() if campo else ""


def validar_donacion(form):
    errores = []

    tipo_donacion = form.get("tipo_donacion", "").strip()
    descripcion = form.get("descripcion", "").strip()
    beneficiario_id = form.get("beneficiario_id", "").strip()
    categoria = obtener_categoria_donacion(form)

    if not tipo_donacion:
        errores.append("Debes seleccionar un tipo de donación.")

    if tipo_donacion and not categoria:
        errores.append("Debes seleccionar una categoría.")

    if not descripcion or len(descripcion) < 5:
        errores.append("La descripción debe tener mínimo 5 caracteres.")

    if not beneficiario_id:
        errores.append("Debes seleccionar un beneficiario.")

    return len(errores) == 0, errores


def obtener_beneficiarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, documento FROM beneficiarios ORDER BY nombre")
    beneficiarios = cur.fetchall()
    cur.close()
    return beneficiarios


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    next_page = request.args.get("next")

    if request.method == "POST":
        cedula = request.form.get("Cedula_Donante", "").strip()
        clave = request.form.get("clave", "")

        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM usuarios WHERE cedula = %s", (cedula,))
            usuario = cur.fetchone()
            cur.close()

            if not usuario:
                flash("El usuario con esa cédula no existe.", "error")
                return render_template("login.html")

            if usuario["clave"] != clave:
                flash("Contraseña incorrecta.", "error")
                return render_template("login.html")

            session["usuario_id"] = usuario["id"]
            session["usuario_cedula"] = usuario["cedula"]
            session["usuario_nombre"] = usuario["primer_nombre"]
            session["usuario_rol"] = usuario["rol"]

            flash(f"Bienvenido, {usuario['primer_nombre']}.", "success")
            return redirect(next_page or url_for("home"))

        except Exception as e:
            logging.exception("Error en login")
            flash(f"Error al iniciar sesión: {str(e)}", "error")

    return render_template("login.html")

@app.route('/registro', methods=['GET', 'POST'])
def registro():

    datos = {}

    if request.method == "POST":

        datos = {
            "Cedula_Donante": request.form.get("Cedula_Donante", "").strip(),
            "primer_nombre": request.form.get("primer_nombre", "").strip(),
            "segundo_nombre": request.form.get("segundo_nombre", "").strip(),
            "primer_apellido": request.form.get("primer_apellido", "").strip(),
            "segundo_apellido": request.form.get("segundo_apellido", "").strip(),
            "contacto": request.form.get("contacto", "").strip()
        }

        valido, errores = validar_registro(request.form)

        if not valido:

            for error in errores:
                flash(error, "error")

            return render_template(
                "register.html",
                datos=datos
            )

        try:

            cur = mysql.connection.cursor()

            cur.execute(
                """
                SELECT id
                FROM usuarios
                WHERE cedula = %s
                """,
                (datos["Cedula_Donante"],)
            )

            usuario_existente = cur.fetchone()

            if usuario_existente:

                cur.close()

                flash(
                    "Ya existe un usuario registrado con esa cédula.",
                    "warning"
                )

                return render_template(
                    "register.html",
                    datos=datos
                )

            cur.execute(
                """
                INSERT INTO usuarios (
                    cedula,
                    primer_nombre,
                    segundo_nombre,
                    primer_apellido,
                    segundo_apellido,
                    contacto,
                    clave,
                    rol
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    'donante'
                )
                """,
                (
                    datos["Cedula_Donante"],
                    datos["primer_nombre"],
                    datos["segundo_nombre"],
                    datos["primer_apellido"],
                    datos["segundo_apellido"],
                    datos["contacto"],
                    request.form.get("clave")
                )
            )

            mysql.connection.commit()

            cur.close()

            flash(
                "Usuario registrado correctamente. Ahora puedes iniciar sesión.",
                "success"
            )

            return redirect(url_for("login"))

        except Exception as e:

            logging.exception("Error en registro")

            flash(
                f"Error al registrar usuario: {str(e)}",
                "error"
            )

            return render_template(
                "register.html",
                datos=datos
            )

    return render_template(
        "register.html",
        datos=datos
    )

@app.route("/donacion", methods=["GET", "POST"])
def donacion():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para registrar un juguete.", "warning")
        return redirect(url_for("login", next=request.url))

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
                "gestion_donacion.html",
                datos=datos,
                categorias=categorias
            )

        try:

            cur = mysql.connection.cursor()

            cur.execute(
                """
                SELECT id
                FROM juguetes
                WHERE codigo_barras = %s
                """,
                (datos["codigo_barras"],)
            )

            juguete_existente = cur.fetchone()

            if juguete_existente:

                cur.close()

                flash(
                    "Ya existe un juguete registrado con ese código de barras.",
                    "warning"
                )

                return render_template(
                    "gestion_donacion.html",
                    datos=datos,
                    categorias=categorias
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
                )
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
                )
            )

            mysql.connection.commit()

            cur.close()

            flash(
                "Juguete registrado correctamente.",
                "success"
            )

            return redirect(url_for("historial"))

        except Exception as e:

            logging.exception("Error registrando juguete")

            flash(
                f"Error técnico al registrar juguete: {str(e)}",
                "error"
            )

            return render_template(
                "gestion_donacion.html",
                datos=datos,
                categorias=categorias
            )

    return render_template(
        "gestion_donacion.html",
        datos=datos,
        categorias=categorias
    )

@app.route("/historial")
def historial():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para consultar el historial.", "warning")
        return redirect(url_for("login", next=request.url))

    estado = request.args.get("estado", "").strip()
    codigo_barras = request.args.get("codigo_barras", "").strip()
    donante = request.args.get("donante", "").strip()
    beneficiario = request.args.get("beneficiario", "").strip()

    try:
        cur = mysql.connection.cursor()

        query = """
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
                b.documento AS beneficiario_documento,
                e.lugar_entrega,
                e.fecha_entrega

            FROM juguetes j
            INNER JOIN categorias c ON c.id = j.categoria_id
            LEFT JOIN entregas e ON e.juguete_id = j.id
            LEFT JOIN beneficiarios b ON b.id = e.beneficiario_id
            WHERE 1 = 1
        """

        params = []

        if session.get("usuario_rol") != "admin":
            query += " AND j.donante_id = %s"
            params.append(session["usuario_id"])

        if estado:
            query += " AND j.estado_actual = %s"
            params.append(estado)

        if codigo_barras:
            query += " AND j.codigo_barras LIKE %s"
            params.append(f"%{codigo_barras}%")

        if donante:
            query += """
                AND (
                    j.donante_nombre LIKE %s
                    OR j.donante_correo LIKE %s
                    OR j.donante_telefono LIKE %s
                )
            """
            like_donante = f"%{donante}%"
            params.extend([like_donante, like_donante, like_donante])

        if beneficiario:
            query += """
                AND (
                    b.nombre LIKE %s
                    OR b.documento LIKE %s
                )
            """
            like_beneficiario = f"%{beneficiario}%"
            params.extend([like_beneficiario, like_beneficiario])

        query += " ORDER BY j.fecha_recepcion DESC"

        cur.execute(query, tuple(params))
        juguetes = cur.fetchall()
        cur.close()

        filtros = {
            "estado": estado,
            "codigo_barras": codigo_barras,
            "donante": donante,
            "beneficiario": beneficiario,
        }

        return render_template(
            "historial.html",
            juguetes=juguetes,
            filtros=filtros
        )

    except Exception as e:
        logging.exception("Error cargando historial")
        flash(f"Error al cargar historial: {str(e)}", "error")
        return render_template("historial.html", juguetes=[], filtros={})

@app.route("/juguetes/<int:juguete_id>/estado", methods=["POST"])
def actualizar_estado_juguete(juguete_id):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión.", "warning")
        return redirect(url_for("login"))

    if session.get("usuario_rol") != "admin":
        flash("No tienes permisos para actualizar estados.", "error")
        return redirect(url_for("historial"))

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
        return redirect(url_for("historial"))

    try:
        cur = mysql.connection.cursor()

        cur.execute("SELECT estado_actual FROM juguetes WHERE id = %s", (juguete_id,))
        juguete = cur.fetchone()

        if not juguete:
            cur.close()
            flash("El juguete no existe.", "error")
            return redirect(url_for("historial"))

        estado_anterior = juguete["estado_actual"]

        cur.execute(
            "UPDATE juguetes SET estado_actual = %s WHERE id = %s",
            (nuevo_estado, juguete_id)
        )

        cur.execute("""
            INSERT INTO historial_estados_juguete (
                juguete_id,
                estado_anterior,
                estado_nuevo,
                observacion,
                usuario_id
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            juguete_id,
            estado_anterior,
            nuevo_estado,
            observacion,
            session["usuario_id"],
        ))

        if nuevo_estado == "entregado":
            beneficiario_nombre = request.form.get("beneficiario_nombre", "").strip()
            beneficiario_edad = request.form.get("beneficiario_edad", "").strip()
            beneficiario_institucion = request.form.get("beneficiario_institucion", "").strip()
            lugar_entrega = request.form.get("lugar_entrega", "").strip()
            observaciones_entrega = request.form.get("observaciones_entrega", "").strip()

            if not beneficiario_nombre or not lugar_entrega:
                mysql.connection.rollback()
                cur.close()
                flash("Para entregar el juguete debes ingresar beneficiario y lugar de entrega.", "error")
                return redirect(url_for("historial"))

            cur.execute("""
                INSERT INTO beneficiarios (
                    nombre,
                    edad,
                    institucion,
                    observaciones
                )
                VALUES (%s, %s, %s, %s)
            """, (
                beneficiario_nombre,
                int(beneficiario_edad) if beneficiario_edad else None,
                beneficiario_institucion or None,
                observaciones_entrega or None,
            ))

            beneficiario_id = cur.lastrowid

            cur.execute("""
                INSERT INTO entregas (
                    juguete_id,
                    beneficiario_id,
                    entregado_por_id,
                    lugar_entrega,
                    observaciones
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                juguete_id,
                beneficiario_id,
                session["usuario_id"],
                lugar_entrega,
                observaciones_entrega or None,
            ))

        mysql.connection.commit()
        cur.close()

        flash("Estado actualizado correctamente.", "success")

    except Exception as e:
        logging.exception("Error actualizando estado")
        flash(f"Error al actualizar estado: {str(e)}", "error")

    return redirect(url_for("historial"))

@app.route("/categorias", methods=["GET", "POST"])
def categorias():
    if session.get("usuario_rol") != "admin":
        flash("No tienes permisos para administrar categorías.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()

        if not nombre or len(nombre) < 2:
            flash("El nombre debe tener mínimo 2 caracteres.", "error")
            return redirect(url_for("categorias"))

        try:
            cur = mysql.connection.cursor()

            cur.execute("""
                INSERT INTO categorias (nombre, activa)
                VALUES (%s, TRUE)
            """, (nombre,))

            mysql.connection.commit()
            cur.close()

            flash("Categoría creada correctamente.", "success")

        except Exception as e:
            logging.exception("Error creando categoría")
            flash(f"Error creando categoría: {str(e)}", "error")

        return redirect(url_for("categorias"))

    nombre = request.args.get("nombre", "").strip()
    estado = request.args.get("estado", "").strip()

    query = """
        SELECT
            id,
            nombre,
            activa,
            creado_en
        FROM categorias
        WHERE 1 = 1
    """

    params = []

    if nombre:
        query += " AND LOWER(nombre) LIKE LOWER(%s)"
        params.append(f"%{nombre}%")

    if estado == "activas":
        query += " AND activa = TRUE"

    elif estado == "inactivas":
        query += " AND activa = FALSE"

    query += " ORDER BY activa DESC, nombre ASC"

    cur = mysql.connection.cursor()
    cur.execute(query, tuple(params))

    categorias = cur.fetchall()

    cur.close()

    filtros = {
        "nombre": nombre,
        "estado": estado
    }

    return render_template(
        "categorias.html",
        categorias=categorias,
        filtros=filtros
    )

@app.route("/categorias/<int:categoria_id>/editar", methods=["POST"])
def editar_categoria(categoria_id):
    if session.get("usuario_rol") != "admin":
        flash("No tienes permisos para editar categorías.", "error")
        return redirect(url_for("home"))

    nombre = request.form.get("nombre", "").strip()
    activa = request.form.get("activa") == "1"

    if not nombre or len(nombre) < 2:
        flash("El nombre de la categoría debe tener mínimo 2 caracteres.", "error")
        return redirect(url_for("categorias"))

    slug = generar_slug(nombre)

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE categorias
            SET nombre = %s,
                slug = %s,
                activa = %s
            WHERE id = %s
        """, (nombre, slug, activa, categoria_id))

        mysql.connection.commit()
        cur.close()

        flash("Categoría actualizada correctamente.", "success")

    except Exception as e:
        logging.exception("Error actualizando categoría")
        flash(f"Error actualizando categoría: {str(e)}", "error")

    return redirect(url_for("categorias"))

def obtener_categorias_activas():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, nombre, slug
        FROM categorias
        WHERE activa = TRUE
        ORDER BY nombre
    """)
    categorias = cur.fetchall()
    cur.close()
    return categorias


def obtener_categorias():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, nombre, slug, activa, creado_en
        FROM categorias
        ORDER BY activa DESC, nombre
    """)
    categorias = cur.fetchall()
    cur.close()
    return categorias


def generar_slug(texto):
    return (
        texto.strip()
        .lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace(" ", "_")
    )

def validar_donacion(form):
    errores = []

    codigo_barras = form.get("codigo_barras", "").strip()
    donante_nombre = form.get("donante_nombre", "").strip()
    donante_correo = form.get("donante_correo", "").strip()
    donante_telefono = form.get("donante_telefono", "").strip()
    categoria_id = form.get("categoria_id", "").strip()
    descripcion = form.get("descripcion", "").strip()

    if not codigo_barras:
        errores.append("Debes escanear o ingresar el código de barras.")

    if not donante_nombre or len(donante_nombre) < 2:
        errores.append("El nombre del donante debe tener mínimo 2 caracteres.")

    if not donante_correo:
        errores.append("El correo del donante es obligatorio.")
    elif "@" not in donante_correo or "." not in donante_correo:
        errores.append("El correo del donante no tiene un formato válido.")

    if donante_telefono and len(donante_telefono) < 7:
        errores.append("El teléfono debe tener mínimo 7 caracteres.")

    if not categoria_id:
        errores.append("Debes seleccionar una categoría.")

    if not descripcion or len(descripcion) < 5:
        errores.append("La descripción debe tener mínimo 5 caracteres.")

    return len(errores) == 0, errores

@app.route("/juguetes/<int:juguete_id>")
def detalle_juguete(juguete_id):
    if "usuario_id" not in session:
        flash("Debes iniciar sesión.", "warning")
        return redirect(url_for("login"))

    cur = mysql.connection.cursor()

    cur.execute("""
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
    """, (juguete_id,))

    juguete = cur.fetchone()

    cur.execute("""
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
    """, (juguete_id,))

    historial = cur.fetchall()
    cur.close()

    return render_template(
        "detalle_juguete.html",
        juguete=juguete,
        historial=historial
    )

@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001, threaded=True)