class ValidadorBase:
    def __init__(self, siguiente=None):
        self.siguiente = siguiente

    def manejar(self, form):
        if self.validar(form):
            if self.siguiente:
                return self.siguiente.manejar(form)
            return True
        return False

    def validar(self, form):
        raise NotImplementedError


class ValidarDescripcion(ValidadorBase):
    def validar(self, form):
        descripcion = form.get("descripcion", "").strip()
        return bool(descripcion) and len(descripcion) >= 5


class ValidarMonto(ValidadorBase):
    def validar(self, form):
        monto = form.get("monto")
        if monto is None or monto == "":
            return True  # Si no es donación monetaria, es válido
        try:
            return float(monto) >= 0
        except ValueError:
            return False


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
