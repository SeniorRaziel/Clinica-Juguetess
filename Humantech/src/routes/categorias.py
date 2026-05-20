import logging

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from extensions import mysql

categorias_bp = Blueprint("categorias", __name__)

from services.juguetes_helpers import generar_slug


@categorias_bp.route("/categorias", methods=["GET", "POST"])
def categorias():
    if session.get("usuario_rol") != "admin":
        flash("No tienes permisos para administrar categorías.", "error")
        return redirect(url_for("home.home"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()

        if not nombre or len(nombre) < 2:
            flash("El nombre debe tener mínimo 2 caracteres.", "error")
            return redirect(url_for("categorias.categorias"))

        try:
            cur = mysql.connection.cursor()

            cur.execute(
                """
                INSERT INTO categorias (nombre, activa)
                VALUES (%s, TRUE)
                """,
                (nombre,),
            )

            mysql.connection.commit()
            cur.close()

            flash("Categoría creada correctamente.", "success")

        except Exception as e:
            logging.exception("Error creando categoría")
            flash(f"Error creando categoría: {str(e)}", "error")

        return redirect(url_for("categorias.categorias"))

    nombre = request.args.get("nombre", "").strip()
    estado = request.args.get("estado", "").strip()

    page = request.args.get("page", 1, type=int)
    per_page = 10

    if page < 1:
        page = 1

    offset = (page - 1) * per_page

    base_query = """
        FROM categorias
        WHERE 1 = 1
    """

    params = []

    if nombre:
        base_query += " AND LOWER(nombre) LIKE LOWER(%s)"
        params.append(f"%{nombre}%")

    if estado == "activas":
        base_query += " AND activa = TRUE"
    elif estado == "inactivas":
        base_query += " AND activa = FALSE"

    try:
        cur = mysql.connection.cursor()

        count_query = "SELECT COUNT(*) AS total " + base_query
        cur.execute(count_query, tuple(params))
        total = cur.fetchone()["total"]

        query = (
            """
            SELECT
                id,
                nombre,
                activa,
                creado_en
        """
            + base_query
            + """
            ORDER BY activa DESC, nombre ASC
            LIMIT %s OFFSET %s
        """
        )

        cur.execute(query, tuple(params + [per_page, offset]))
        categorias = cur.fetchall()
        cur.close()

        total_pages = (total + per_page - 1) // per_page

        filtros = {
            "nombre": nombre,
            "estado": estado,
        }

        return render_template(
            "categorias.html",
            categorias=categorias,
            filtros=filtros,
            page=page,
            total_pages=total_pages,
            total=total,
        )

    except Exception as e:
        logging.exception("Error cargando categorías")
        flash(f"Error cargando categorías: {str(e)}", "error")

        return render_template(
            "categorias.html",
            categorias=[],
            filtros={},
            page=1,
            total_pages=0,
            total=0,
        )


@categorias_bp.route("/categorias/<int:categoria_id>/editar", methods=["POST"])
def editar_categoria(categoria_id):
    if session.get("usuario_rol") != "admin":
        flash("No tienes permisos para editar categorías.", "error")
        return redirect(url_for("home.home"))

    nombre = request.form.get("nombre", "").strip()
    activa = request.form.get("activa") == "1"

    if not nombre or len(nombre) < 2:
        flash("El nombre de la categoría debe tener mínimo 2 caracteres.", "error")
        return redirect(url_for("categorias.categorias"))

    slug = generar_slug(nombre)

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE categorias
            SET nombre = %s,
                slug = %s,
                activa = %s
            WHERE id = %s
        """,
            (nombre, slug, activa, categoria_id),
        )

        mysql.connection.commit()
        cur.close()

        flash("Categoría actualizada correctamente.", "success")

    except Exception as e:
        logging.exception("Error actualizando categoría")
        flash(f"Error actualizando categoría: {str(e)}", "error")

    return redirect(url_for("categorias.categorias"))
