from flask import session, flash


def usuario_actual_id():
    return session.get("usuario_id")


def login_requerido():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para continuar.", "warning")
        return False
    return True


def login_requerido():
    if "usuario_id" not in session:
        flash("Debes iniciar sesión para continuar.", "warning")
        return False

    return True


def admin_requerido():
    if session.get("usuario_rol") != "admin":
        flash("No tienes permisos para acceder a esta sección.", "error")
        return False

    return True
