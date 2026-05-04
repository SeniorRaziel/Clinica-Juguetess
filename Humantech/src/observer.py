class ObservadorDonacion:
    def actualizar(self, donacion):
        pass

class CorreoAgradecimiento(ObservadorDonacion):
    def actualizar(self, donacion):
        # Lógica para enviar correo
        pass

class LogDonacion(ObservadorDonacion):
    def actualizar(self, donacion):
        print(f"Donación registrada: {donacion}")

class SujetoDonacion:
    def __init__(self):
        self.observadores = []

    def agregar(self, obs):
        self.observadores.append(obs)

    def notificar(self, donacion):
        for obs in self.observadores:
            obs.actualizar(donacion)