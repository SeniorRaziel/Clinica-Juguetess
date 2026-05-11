from flask import Flask, render_template, redirect, request, Response, session, url_for, flash, send_file
from flask_mysqldb import MySQL, MySQLdb
from datetime import date
import smtplib
from email.mime.text import MIMEText
import io
import pandas as pd
import os
import logging
from informes import GeneradorInforme, InformeExcel
from validaciones import ValidarMonto, ValidarDescripcion

# 1. Uso de variables de entorno para configuración sensible
app = Flask(__name__, template_folder='templates')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '123456789')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'sysong')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# 2. Logging centralizado
logging.basicConfig(filename='app.log', level=logging.ERROR)

# 3. Modularización de funciones auxiliares
def obtener_beneficiarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM beneficiarios")
    beneficiarios = cur.fetchall()
    cur.close()
    return beneficiarios

def obtener_donante_por_cedula(cedula):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM donantes WHERE Cedula_Donante=%s", (cedula,))
    donante = cur.fetchone()
    cur.close()
    return donante

def validar_registro(form):
    errores = []

    cedula = form.get("Cedula_Donante", "").strip()
    primer_nombre = form.get("primer_nombre", "").strip()
    segundo_nombre = form.get("segundo_nombre", "").strip()
    primer_apellido = form.get("primer_apellido", "").strip()
    segundo_apellido = form.get("segundo_apellido", "").strip()
    contacto = form.get("contacto", "").strip()
    clave = form.get("clave", "")
    clave2 = form.get("clave2", "")

    if not cedula:
        errores.append("La cédula es obligatoria.")
    elif not cedula.isdigit():
        errores.append("La cédula solo debe contener números.")
    elif len(cedula) < 6 or len(cedula) > 12:
        errores.append("La cédula debe tener entre 6 y 12 dígitos.")

    if not primer_nombre:
        errores.append("El primer nombre es obligatorio.")
    elif len(primer_nombre) < 2:
        errores.append("El primer nombre debe tener mínimo 2 caracteres.")

    if segundo_nombre and len(segundo_nombre) < 2:
        errores.append("El segundo nombre debe tener mínimo 2 caracteres.")

    if not primer_apellido:
        errores.append("El primer apellido es obligatorio.")
    elif len(primer_apellido) < 2:
        errores.append("El primer apellido debe tener mínimo 2 caracteres.")

    if segundo_apellido and len(segundo_apellido) < 2:
        errores.append("El segundo apellido debe tener mínimo 2 caracteres.")

    if not contacto:
        errores.append("El contacto es obligatorio.")
    elif len(contacto) < 7:
        errores.append("El contacto debe tener mínimo 7 caracteres.")

    if not clave:
        errores.append("La contraseña es obligatoria.")
    elif len(clave) < 6:
        errores.append("La contraseña debe tener mínimo 6 caracteres.")

    if clave != clave2:
        errores.append("Las contraseñas no coinciden.")

    return len(errores) == 0, errores

def validar_donacion_form(form):
    campos = ['tipo', 'descripcion', 'beneficiario_Cedula']
    for campo in campos:
        if not form.get(campo):
            return False, f"El campo {campo} es obligatorio."
    return True, ""

# Reintento de conexión antes de cada request
@app.before_request
def before_request():
    try:
        mysql.connection.ping()
    except Exception as e:
        print("Error de reconexión:", e)

@app.route('/')
def home():
    id_donante = None
    if 'usuario' in session:
        cur = mysql.connection.cursor()
        # CAMBIO: buscar por Cedula_Donante, no por contacto
        cur.execute("SELECT Cedula_Donante FROM donantes WHERE Cedula_Donante=%s", (session['usuario'],))
        donante = cur.fetchone()
        cur.close()
        if donante:
            id_donante = donante['Cedula_Donante']
    return render_template('home.html', id_donante=id_donante)

@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')
    if request.method == "POST":
        cedula_donante = request.form['Cedula_Donante']
        clave = request.form['clave']
        try:
            mysql.connection.ping()
            cur = mysql.connection.cursor()
            try:
                cur.execute("SELECT * FROM donantes WHERE Cedula_Donante=%s", (cedula_donante,))
                usuario = cur.fetchone()
                if not usuario:
                    return render_template("login.html", error="El usuario con esa cédula no existe.")
                # Si existe, ahora verifica la clave
                if usuario['clave'] != clave:
                    return render_template("login.html", error="Contraseña incorrecta.")
                session['usuario'] = usuario['Cedula_Donante']
                return redirect(next_page or url_for('home'))
            finally:
                cur.close()
        except Exception as e:
            return render_template("login.html", error=str(e))
    return render_template("login.html")

### REGISTRO CONFIGURATION

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

            return render_template("register.html", datos=datos)

        try:
            cur = mysql.connection.cursor()

            cur.execute(
                "SELECT Cedula_Donante FROM donantes WHERE Cedula_Donante = %s",
                (datos["Cedula_Donante"],)
            )

            donante_existente = cur.fetchone()

            if donante_existente:
                cur.close()
                flash("Ya existe un usuario registrado con esa cédula.", "warning")
                return render_template("register.html", datos=datos)

            cur.execute("""
                INSERT INTO donantes (
                    Cedula_Donante,
                    primer_nombre,
                    segundo_nombre,
                    primer_apeliido,
                    segundo_apellido,
                    contacto,
                    clave
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                datos["Cedula_Donante"],
                datos["primer_nombre"],
                datos["segundo_nombre"],
                datos["primer_apellido"],
                datos["segundo_apellido"],
                datos["contacto"],
                request.form.get("clave")
            ))

            mysql.connection.commit()
            cur.close()

            flash("Usuario registrado correctamente. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("login"))

        except Exception as e:
            logging.exception("Error en registro")
            flash(f"Error al registrar usuario: {str(e)}", "error")
            return render_template("register.html", datos=datos)

    return render_template("register.html", datos=datos)

@app.route('/donacion', methods=['GET', 'POST'])
def gestion():
    if 'usuario' not in session:
        return redirect(url_for('login', next=request.url))

    beneficiarios = obtener_beneficiarios()

    if request.method == "POST":
        # Validación con Chain of Responsibility
        cadena = ValidarMonto(ValidarDescripcion())
        if not cadena.manejar(request.form):
            mensaje = "Datos inválidos en la donación"
            return render_template('gestion_donacion.html', mensaje=mensaje, beneficiarios=beneficiarios)

        valido, mensaje = validar_donacion_form(request.form)
        if not valido:
            return render_template('gestion_donacion.html', mensaje=mensaje, beneficiarios=beneficiarios)
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        monto = request.form.get('monto') or 0
        beneficiario_cedula = request.form.get('beneficiario_Cedula')
        observaciones = request.form.get('observaciones', '')
        fecha = date.today()

        if not beneficiario_cedula:
            mensaje = "Debes seleccionar un beneficiario."
            return render_template('gestion_donacion.html', mensaje=mensaje, beneficiarios=beneficiarios)
        beneficiario_cedula = int(beneficiario_cedula)

        # Obtener donante_id
        donante = obtener_donante_por_cedula(session['usuario'])
        if not donante:
            mensaje = "No se encontró el usuario."
            return render_template('gestion_donacion.html', mensaje=mensaje, beneficiarios=beneficiarios)

        donante_id = donante['Cedula_Donante']

        # Determinar la categoría según el tipo
        categoria = ""
        if tipo == "ropa":
            categoria = request.form.get('categoria_persona', '')
        elif tipo == "medicamentos":
            categoria = request.form.get('categoria_medicamento', '')
        elif tipo == "alimentos":
            categoria = request.form.get('categoria_alimento', '')

        try:
            cur = mysql.connection.cursor()
            # Insertar donación
            cur.execute("INSERT IGNORE INTO fecha_donacion (donacion_fecha) VALUES (%s)", (fecha,))
            cur.execute("""
                INSERT INTO donaciones (beneficiario_Cedula, donante_id, fecha_donacion, tipo_donacion, descripcion, monto, categoria)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (beneficiario_cedula, donante_id, fecha, tipo, descripcion, monto, categoria))
            donacion_id = cur.lastrowid

            # Registrar seguimiento_beneficiario
            cur.execute("""
                INSERT INTO seguimiento_beneficiario (beneficiario_Cedula, personal_id, fecha, observaciones)
                VALUES (%s, %s, %s, %s)
            """, (beneficiario_cedula, None, fecha, observaciones))

            # Registrar seguimiento_donante (ingreso=1, egreso=0)
            cur.execute("""
                INSERT INTO seguimiento_donante (donaciones_id, fecha, ingreso, egreso)
                VALUES (%s, %s, %s, %s)
            """, (donacion_id, fecha, 1, 0))

            mysql.connection.commit()
            cur.close()
        except Exception as e:
            logging.error(f"Error al registrar la donación: {e}")
            mensaje = f"Error al registrar la donación: {e}"
            return render_template('gestion_donacion.html', mensaje=mensaje, beneficiarios=beneficiarios)

        mensaje = "¡Donación registrada exitosamente!"
        return render_template('gestion_donacion.html', mensaje=mensaje, beneficiarios=beneficiarios)

    return render_template('gestion_donacion.html', beneficiarios=beneficiarios)

@app.route('/historial', methods=['GET'])
def ver_historial():
    if 'usuario' not in session:
        return redirect(url_for('login', next=request.url))
    id_donante = request.args.get('id_donante')
    if not id_donante:
        return render_template('historial.html', existe=None, donaciones=[], id_donante=None)
    try:
        mysql.connection.ping()
        cur = mysql.connection.cursor()
        try:
            cur.execute("SELECT * FROM donantes WHERE Cedula_Donante = %s", (id_donante,))
            donante = cur.fetchone()
            if not donante:
                return render_template('historial.html', existe=False, donaciones=[], id_donante=id_donante)
            cur.execute("""
                SELECT d.*, 
                       b.primer_nombre AS nombre_beneficiario, 
                       b.edad AS edad_beneficiario
                FROM donaciones d
                LEFT JOIN beneficiarios b ON d.beneficiario_Cedula = b.Cedula
                WHERE d.donante_id = %s
            """, (id_donante,))
            donaciones = cur.fetchall()
        finally:
            cur.close()
        return render_template('historial.html', existe=True, donaciones=donaciones, id_donante=id_donante)
    except Exception as e:
        print("ERROR EN HISTORIAL:", e)
        return render_template('historial.html', existe=False, donaciones=[], id_donante=id_donante, error=str(e))

@app.route('/enviar-agradecimientos', methods=['POST'])
def enviar_agradecimientos():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT DISTINCT d.contacto, d.primer_nombre
        FROM donantes d
        JOIN donaciones don ON d.Cedula_Donante = don.donante_id
    """)
    donantes = cur.fetchall()
    cur.close()

    remitente = ""
    password = ""
    asunto = "¡Gracias por tu donación!"
    for donante in donantes:
        destinatario = donante['contacto']
        nombre = donante['primer_nombre']
        cuerpo = f"Estimado/a {nombre},\n\nGracias por tu generosa donación. Tu ayuda ha beneficiado a personas que lo necesitaban. ¡Juntos transformamos vidas!\n\nClinica de Juguetes"
        msg = MIMEText(cuerpo)
        msg['Subject'] = asunto
        msg['From'] = remitente
        msg['To'] = destinatario
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(remitente, password)
                server.sendmail(remitente, destinatario, msg.as_string())
        except Exception as e:
            print(f"Error enviando correo a {destinatario}: {e}")

    flash("¡Agradecimientos enviados a todos los donantes!")
    return redirect(url_for('home'))

@app.route('/descargar-informe-donaciones')
def descargar_informe_donaciones():
    id_donante = request.args.get('id_donante')
    if not id_donante:
        flash("No se especificó el donante.")
        return redirect(url_for('home'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT d.id_donacion, d.tipo_donacion, d.categoria, d.descripcion, d.monto, d.fecha_donacion,
               b.primer_nombre AS nombre_beneficiario, b.primer_apellido AS apellido_beneficiario, b.edad AS edad_beneficiario
        FROM donaciones d
        LEFT JOIN beneficiarios b ON d.beneficiario_Cedula = b.Cedula
        WHERE d.donante_id = %s
    """, (id_donante,))
    donaciones = cur.fetchall()
    cur.close()

    import os
    if not os.path.exists('informes'):
        os.makedirs('informes')
    ruta_archivo = os.path.join('informes', f'informe_donaciones_{id_donante}.xlsx')

    # Uso del patrón Strategy para generación de informes
    generador = GeneradorInforme(InformeExcel())
    generador.generar(donaciones, ruta_archivo)

    return send_file(ruta_archivo, download_name=f"informe_donaciones_{id_donante}.xlsx", as_attachment=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/verificar-cedulas')
def verificar_cedulas():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT d.Cedula_Donante, don.donante_id, d.primer_nombre, d.segundo_nombre, don.id_donacion
        FROM donantes d
        JOIN donaciones don ON d.Cedula_Donante = don.donante_id
    """)
    coincidencias = cur.fetchall()
    cur.close()
    return render_template('verificar_cedulas.html', coincidencias=coincidencias)

if __name__ == '__main__':
    app.secret_key = "sysong"
    app.secret_key = "clinica-juguetes-secret"
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)