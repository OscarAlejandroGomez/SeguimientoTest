#from flask import Flask, render_template, json, blueprints
from os import name
import os
from flask import Flask, json,render_template,redirect,request,jsonify,url_for, blueprints
from flask_socketio import SocketIO, rooms,leave_room,join_room

from flask_mysqldb import MySQL
from Views.login import Login
from Views.index import Index
from Views.Registro_usuario.Registro_usuarios import Registro_usuarios
from Views.Carga_informacion.carga_archivo import Carga_archivo
from Views.Carga_informacion.eliminar_informacion import Eliminar_informacion
from Views.Verificar_informacion.revisar_documentos import Revisar_documentos
from Views.Verificar_informacion.documentos_aprobados import Documentos_aprobados
from Views.Verificar_informacion.documentos_devueltos import Documentos_devueltos
from Views.Visualizar_informacion.visualiza_informacion import Visualizar_documentos
from Views.Funciones.observaciones_documento import Observaciones_documento
from uuid import uuid4

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime 
from pathlib import Path


app = Flask(__name__)

app.register_blueprint(Login)
app.register_blueprint(Index)
app.register_blueprint(Registro_usuarios)
app.register_blueprint(Carga_archivo)
app.register_blueprint(Eliminar_informacion)
app.register_blueprint(Revisar_documentos)
app.register_blueprint(Documentos_aprobados)
app.register_blueprint(Documentos_devueltos)
app.register_blueprint(Visualizar_documentos)
app.register_blueprint(Observaciones_documento)


app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')  #'host.docker.internal'
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))#31122
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')  #'Z1'
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD') #'1234'
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB') ## 'bdordenesz1'

print(os.environ.get('MYSQL_HOST'))
print(os.environ.get('MYSQL_PORT'))
print(os.environ.get('MYSQL_USER'))
print(os.environ.get('MYSQL_PASSWORD'))
print(os.environ.get('MYSQL_DB'))

# app.config['MYSQL_HOST'] =  'localhost' #'host.docker.internal'
# app.config['MYSQL_PORT'] = 31122
# app.config['MYSQL_USER'] = 'Z1'
# app.config['MYSQL_PASSWORD'] = '1234'
# app.config['MYSQL_DB'] = 'bdordenesz1'


mysql = MySQL(app)

print([mysql])
socket = SocketIO(app)
valid = False

app.secret_key = 'mysecretkey'

@app.route('/')
def default():
        mas_dias()
        # mail_content = "Hello, This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library"
        # #The mail addresses and password
        # sender_address = 'rosemberg.zambrano1177@correo.policia.gov.co'
        # sender_pass = 'Zaar2022+-'
        # receiver_address = 'OFITE.GRUDE@POLICIA.GOV.CO'
        # #Setup the MIME
        # message = MIMEMultipart()
        # message['From'] = sender_address
        # message['To'] = receiver_address
        # message['Subject'] = 'A test mail sent by Python. It has an attachment.'   
        # #The subject line
        # #The body and the attachments for the mail
        # message.attach(MIMEText(mail_content, 'plain'))
        # #Create SMTP session for sending the mail
        # session = smtplib.SMTP('172.28.9.205', 235) #use gmail with port
        # session.starttls() #enable security
        # session.login(sender_address, sender_pass) #login with mail_id and password
        # text = message.as_string()
        # session.sendmail(sender_address, receiver_address, text)
        # session.quit()
        # print('Mail Sent')
        return render_template('login.html')  

        # to_emails= "rosemberg.zambrano1177@correo.policia.gov.co"
        # message="Hi, this is the email body"
        # s = smtplib.SMTP(host='smtp.office365.com', port=235)
        # s.starttls()
        # s.login('rosemberg.zambrano1177@correo.policia.gov.co','Zaar2022*+')
        # msg = MIMEMultipart()
        # msg['From']='mylogininfo'
        # msg['To']=to_emails
        # msg['Subject']="My Subject"
        # msg.attach(MIMEText(message, 'plain'))
        # s.send_message(msg)
        # del msg
        # s.quit()

def mas_dias():
        today = datetime.today()
        print("Below files will be deleted.") 
        for i in Path('./static/adjuntos/').rglob('*'):
                mtime = datetime.fromtimestamp(i.stat().st_mtime)
                filetime = mtime - today
                if 30 < filetime.days:
                        print(f'{i.name:<20} older {abs(filetime.days)} days')
                        i.unlink()


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, use_debugger=False, use_reloader=False)

