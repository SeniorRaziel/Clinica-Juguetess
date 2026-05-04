class Notificacion:
    def enviar(self, destinatario, asunto, mensaje):
        raise NotImplementedError

class NotificacionCorreo(Notificacion):
    def enviar(self, destinatario, asunto, mensaje):
        import smtplib
        from email.mime.text import MIMEText
        remitente = "tucorreo@gmail.com"
        password = "tu_contraseña"
        msg = MIMEText(mensaje)
        msg['Subject'] = asunto
        msg['From'] = remitente
        msg['To'] = destinatario
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remitente, password)
            server.sendmail(remitente, destinatario, msg.as_string())

class NotificacionFactory:
    @staticmethod
    def crear(tipo):
        if tipo == "correo":
            return NotificacionCorreo()
        # Puedes agregar más tipos (SMS, WhatsApp, etc.)
        raise ValueError("Tipo de notificación no soportado")