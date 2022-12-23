from urllib import response
from flask import Blueprint, Flask, render_template, request, redirect, session, json
from flask_mysqldb import MySQL
import urllib, json
import requests
import MySQLdb.cursors

app = Flask(__name__)
# print([app])
mysql = MySQL(app)

Login = Blueprint("login", __name__)

@Login.route('/f_iniciar_sesion', methods=["POST"])
def f_iniciar_sesion():
    try:
        Usuario = request.form["Usuario"]
        password = request.form["password"]
        # array = request.form.to_dict()
        url = "https://catalogoservicioweb.policia.gov.co/sw/token"
        payload='password=Policia2017*&username=edwin.bustos1929@correo.policia.gov.co&grant_type=password'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        djson = json.loads(response.text)

        url = "https://catalogoservicioweb.policia.gov.co/sw/api/DiversidadPonal/LoginOud"
        payload = json.dumps({
        "Usuario": Usuario,
        "Contrasena": password
        })
        headers = {
        'Authorization': 'Bearer ' + djson["access_token"],
        'Content-Type': 'application/json',
        }
        responses = requests.request("POST", url, headers=headers, data=payload)
        djson1 = json.loads(responses.text)
        if djson1["Codigo"] == 4:
            Usuario	 = request.form["Usuario"]
            if Usuario == "rr.zambrano002":
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute('''SELECT 
                    u.Id_usuario,
                    u.Id_perfil,
                    u.Identificacion,
                    u.Id_codigo_cargo,
                    u.Situacion_actual,
                    u.Unidad,
                    u.Id_tema,
                    u.Id_subtema,
                    u.Usuario
                FROM
                    usuarios u, perfiles p
                WHERE
                    u.Usuario = %s
                    AND u.Estado = 1
                    AND u.Situacion_actual = 'LABORANDO'
                    AND p.Id_perfil = u.Id_perfil
                    AND p.Id_perfil = 10
                ''',(Usuario,))
                Datos_session = cur.fetchone()
            else:
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute('''SELECT 
                    u.Id_usuario,
                    u.Id_perfil,
                    u.Identificacion,
                    u.Id_codigo_cargo,
                    u.Situacion_actual,
                    u.Unidad,
                    u.Id_tema,
                    u.Id_subtema,
                    u.Usuario
                FROM
                    usuarios u, perfiles p
                WHERE
                    u.Usuario = %s
                        AND u.Estado = 1
                        AND u.Fecha_fin_rol > SYSDATE()
                        AND u.Situacion_actual = 'LABORANDO'
                        AND p.Id_perfil = u.Id_perfil
                        AND p.Id_perfil = 10
                ''',(Usuario,))
                Datos_session = cur.fetchone()
            if Datos_session is None:
                return render_template('login.html', retorno=6)
            else:
                if Datos_session:
                    session['loggedin'] = True
                    session['Id_usuario'] = Datos_session['Id_usuario']
                    session['Id_perfil'] = Datos_session['Id_perfil']
                    session['Identificacion'] = Datos_session['Identificacion']
                    session['Id_codigo_cargo'] = Datos_session['Id_codigo_cargo']
                    session['Situacion_actual'] = Datos_session['Situacion_actual']
                    session['Unidad'] = Datos_session['Unidad']
                    session['Id_tema'] = Datos_session['Id_tema']
                    session['Id_subtema'] = Datos_session['Id_subtema']
                    session['Usuario'] = Datos_session['Usuario']
                    
                    url = "https://catalogoservicioweb.policia.gov.co/sw/token"
                    payload='password=Policia2017*&username=edwin.bustos1929@correo.policia.gov.co&grant_type=password'
                    headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    }
                    response = requests.request("POST", url, headers=headers, data=payload)
                    djson = json.loads(response.text)

                    Identificacion = str(session['Identificacion'])        
                    url = f'https://catalogoservicioweb.policia.gov.co/sw/api/DiversidadPonal/DatosFuncionarioPonalIdentificacion?_identificacion=' + Identificacion
                    headers = {
                    'Authorization': 'Bearer ' + djson["access_token"],
                    'Content-Type': 'application/json',
                    }
                    responses = requests.request("POST", url, headers=headers)
                    djson1 = json.loads(responses.text)
                    # v=[]
                    # for v in djson1:
                    #     if v == "Respuesta":
                    #         if v.index[2]== "OFITE":
                    #             H = v.index[2]
                            # for i in v:
                            #     if i =="function variables":
                            #         for j in i:
                            #             if j.index != "":
                            #                 if j == "SITUACION_LABORAL":

                                # if j == k:
                                    #    SITUACION_LABORAL = str(i)
                        #                 if session['Situacion_actual'] == SITUACION_LABORAL:
                    return redirect("/index")  
        else:
            return render_template('login.html', retorno=5)  
               

    except Exception as e:
        #e.print_exc()
        print ("This is an error message f_iniciar_sesion!{}".format(e))
    