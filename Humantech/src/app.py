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
    campos = ['Cedula_Donante', 'primer_nombre', 'primer_apeliido', 'segundo_apellido', 'contacto', 'clave', 'clave2']
    for campo in campos:
        if not form.get(campo):
            return False, f"El campo {campo} es obligatorio."
    if form['clave'] != form['clave2']:
        return False, "Las contraseñas no coinciden"
    return True, ""

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


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    mensaje = ""
    datos = {}
    if request.method == "POST":
        valido, mensaje = validar_registro(request.form)
        if not valido:
            return render_template('register.html', mensaje=mensaje, datos=request.form)
        cedula_donante = request.form['Cedula_Donante']
        primer_nombre = request.form['primer_nombre']
        segundo_nombre = request.form['segundo_nombre']
        primer_apellido = request.form['primer_apellido']
        segundo_apellido = request.form['segundo_apellido']
        contacto = request.form['contacto']
        clave = request.form['clave']
        clave2 = request.form['clave2']

        datos = {
            "Cedula_Donante": cedula_donante,
            "primer_nombre": primer_nombre,
            "segundo_nombre": segundo_nombre,
            "primer_apellido": primer_apellido,
            "segundo_apellido": segundo_apellido,
            "contacto": contacto
        }

        try:
            mysql.connection.ping()
            cur = mysql.connection.cursor()
            try:
                cur.execute("SELECT * FROM donantes WHERE Cedula_Donante=%s", (cedula_donante,))
                existe = cur.fetchone()
                if existe:
                    mensaje = "La cédula ya existe"
                    return render_template('register.html', mensaje=mensaje, datos=datos)

                cur.execute("""
                    INSERT INTO donantes 
                    (Cedula_Donante, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, contacto, clave)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (cedula_donante, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, contacto, clave))
                mysql.connection.commit()
            finally:
                cur.close()
        except MySQLdb.OperationalError as e:
            logging.error(f"Error de conexión en registro: {e}")
            mensaje = "Error de conexión con la base de datos. Intenta más tarde."
            return render_template('register.html', mensaje=mensaje, datos=datos)

        mensaje = "Registro exitoso. Ahora puedes iniciar sesión."
        return redirect(url_for('login'))
    return render_template('register.html', datos=datos)

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
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)