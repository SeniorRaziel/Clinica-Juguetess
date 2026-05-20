import logging

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from extensions import mysql

from services.validators import validar_registro

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
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
            return redirect(next_page or url_for("home.home"))

        except Exception as e:
            logging.exception("Error en login")
            flash(f"Error al iniciar sesión: {str(e)}", "error")

    return render_template("login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():

    datos = {}

    if request.method == "POST":

        datos = {
            "Cedula_Donante": request.form.get("Cedula_Donante", "").strip(),
            "primer_nombre": request.form.get("primer_nombre", "").strip(),
            "segundo_nombre": request.form.get("segundo_nombre", "").strip(),
            "primer_apellido": request.form.get("primer_apellido", "").strip(),
            "segundo_apellido": request.form.get("segundo_apellido", "").strip(),
            "contacto": request.form.get("contacto", "").strip(),
        }

        valido, errores = validar_registro(request.form)

        if not valido:

            for error in errores:
                flash(error, "error")

            return render_template("register.html", datos=datos)

        try:

            cur = mysql.connection.cursor()

            cur.execute(
                """
                SELECT id
                FROM usuarios
                WHERE cedula = %s
                """,
                (datos["Cedula_Donante"],),
            )

            usuario_existente = cur.fetchone()

            if usuario_existente:

                cur.close()

                flash("Ya existe un usuario registrado con esa cédula.", "warning")

                return render_template("register.html", datos=datos)

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
                    request.form.get("clave"),
                ),
            )

            mysql.connection.commit()

            cur.close()

            flash(
                "Usuario registrado correctamente. Ahora puedes iniciar sesión.",
                "success",
            )

            return redirect(url_for("auth.login"))

        except Exception as e:

            logging.exception("Error en registro")

            flash(f"Error al registrar usuario: {str(e)}", "error")

            return render_template("register.html", datos=datos)

    return render_template("register.html", datos=datos)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("home.home"))
