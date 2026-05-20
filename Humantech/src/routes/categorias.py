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

    filtros = {"nombre": nombre, "estado": estado}

    return render_template("categorias.html", categorias=categorias, filtros=filtros)


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
