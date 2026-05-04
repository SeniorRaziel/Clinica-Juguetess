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
        descripcion = form.get('descripcion', '').strip()
        return bool(descripcion) and len(descripcion) >= 5

class ValidarMonto(ValidadorBase):
    def validar(self, form):
        monto = form.get('monto')
        if monto is None or monto == '':
            return True  # Si no es donación monetaria, es válido
        try:
            return float(monto) >= 0
        except ValueError:
            return False