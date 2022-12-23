from flask import Blueprint, Flask, render_template, request, json, session
from flask_mysqldb import MySQL
import urllib, json
import requests
from datetime import datetime
import socket
import Views.Funciones.perfiles as perfil
import Views.Funciones.temas as temas


app = Flask(__name__)
mysql = MySQL(app)

Registro_usuarios = Blueprint("registro_usuarios", __name__)


@Registro_usuarios.route('/registro_usuarios')
def registro_usuarios():
    perfile = perfil.valida_perfiles()
    t = temas.visualiza_temas()
    i = 1
    p = []
    for i in perfile:
        p.extend(i)
    return render_template('./Administracion/Registro_usuarios.html', perfiles = p, tema = t)


@Registro_usuarios.route('/f_consultar_perfil', methods=["POST"])
def f_consultar_perfil():
    try:
        Estado	 = int(request.form['Estado'])
        cur = mysql.connection.cursor()
        cur.execute('''select p.Id_perfil, 
        p.Descripcion_perfil 
        from perfiles p 
        where p.Id_padre = %s
        ''',(Estado,))
        mysql.connection.commit()
        perfiles = cur.fetchall()
        cur.close()
        return json.dumps({'status':1, 'data':perfiles})
    except Exception as e:
        print("This is an error message f_consultar_perfil !{}".format(e))


@Registro_usuarios.route('/f_consultar_opcion_habilitar', methods=["POST"])
def f_consultar_opcion_habilitar():
    try:
        Estado	 = int(request.form['Estado'])
        cur = mysql.connection.cursor()
        cur.execute('''SELECT t.Id_dominio, t.Descripcion_dominio 
        from ctrl_dominios t 
        where t.Estado = %s
        AND t.Id_padre =1; 
        ''',(Estado,))
        mysql.connection.commit()
        habilitar = cur.fetchall()
        cur.close()
        return json.dumps({'status':1, 'data':habilitar})
    except Exception as e:
        print("This is an error message f_consultar_opcion_habilitar !{}".format(e))


@Registro_usuarios.route('/f_visualiza_temas', methods=["POST"])
def f_visualiza_temas():
    try:
        Estado	 = int(request.form['Estado'])
        cur = mysql.connection.cursor()
        cur.execute('''SELECT 
            t.Id_tema, t.Descripcion_tema
        FROM
            temas t
        WHERE
            t.Id_padre_tema = 0 AND t.Estado = %s
        ORDER BY 1; 
        ''',(Estado,))
        mysql.connection.commit()
        temas = cur.fetchall()
        cur.close()
        return json.dumps({'status':1, 'data':temas})
    except Exception as e:
        print("This is an error message f_visualiza_temas !{}".format(e))


@Registro_usuarios.route('/f_visualiza_subtemas', methods=["POST"])
def f_visualiza_subtemas():
    try:
        Id_tema	 = int(request.form['Id_tema'])
        cur = mysql.connection.cursor()
        cur.execute('''SELECT 
            t.Id_tema, t.Descripcion_tema
        FROM
            temas t
        WHERE
            t.Id_padre_tema = %s
            AND t.Estado = 1
        ORDER BY 1; 
        ''',(Id_tema,))
        mysql.connection.commit()
        subtemas = cur.fetchall() 
        cur.close()
        return json.dumps({'status':1, 'data':subtemas})
    except Exception as e:
        print("This is an error message f_visualiza_subtemas !{}".format(e))


@Registro_usuarios.route('/p_identificacion', methods=["POST"])
def p_identificacion():
    try:
        Identificacion	 = request.form['Identificacion']
        url = "https://catalogoservicioweb.policia.gov.co/sw/token"
        payload='password=Policia2017*&username=edwin.bustos1929@correo.policia.gov.co&grant_type=password'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        djson = json.loads(response.text)
        # print(djson["access_token"])

        
        url = f'https://catalogoservicioweb.policia.gov.co/sw/api/DiversidadPonal/ConsultarImagenFuncionario?_numeroDocumento=' + Identificacion
        headers = {
        'Authorization': 'Bearer ' + djson["access_token"],
        'Content-Type': 'application/json',
        }
        responses = requests.request("POST", url, headers=headers)
        djsonI = json.loads(responses.text)


        url = f'https://catalogoservicioweb.policia.gov.co/sw/api/DiversidadPonal/DatosFuncionarioPonalIdentificacion?_identificacion=' + Identificacion
        headers = {
        'Authorization': 'Bearer ' + djson["access_token"],
        'Content-Type': 'application/json',
        }
        responses = requests.request("POST", url, headers=headers)
        djson1 = json.loads(responses.text)
        return json.dumps({'status':1, 'data':djson1, 'data1': djsonI})
    except Exception as e:
        print("This is an error message p_identificacion !{}".format(e))


@Registro_usuarios.route('/p_registro_permisos_funcionario', methods=["POST"])
def p_registro_permisos_funcionario():
    try:
        if request.method == 'POST':
            array = request.form.to_dict()
            subtema = request.form.to_dict(array)
            Id_usuario = int(array['obj[Id_usuario]'])
            if Id_usuario >0:
                json_dicti = json.loads(subtema['obj[Id_subtema]']) 
                for i in json_dicti:
                    Id_subtema =  int(i)
                    if Id_subtema > 0:
                        Id_tema = int(array['obj[Id_tema]']) 
                        Identificacion = int(array['obj[Identificacion]']) 
                        Fecha_fin_rol = array['obj[Fecha_fin_rol]']
                        Justificacion = array['obj[Justificacion]']
                        Id_Perfil = int(array['obj[Id_Perfil]'])
                        Id_habilitar = int(array['obj[Id_habilitar]'])

                        Funcionario = array['obj[Funcionario]']
                        Unidad = array['obj[Unidad]']
                        Id_codigo_cargo = int(array['obj[Id_codigo_cargo]'])
                        Cargo = array['obj[Cargo]']
                        Situacion_actual = array['obj[Situacion_actual]']
                        Usuario = array['obj[Usuario]']
                        Correo_electronico = array['obj[Correo_electronico]']
                        Fecha = datetime.now()
                        Fecha_graba = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.connect(("8.8.8.8", 80))
                        Maquina_graba = (s.getsockname()[0])
                        Usuario_graba = session['Usuario']
                        cur = mysql.connection.cursor()
                        cur.execute('''UPDATE usuarios u
                        SET 
                            u.Id_habilitar = %s,
                            u.Id_perfil = %s,
                            u.Id_tema = %s,
                            u.Id_subtema = %s,
                            u.Justificacion = %s,
                            u.Fecha_fin_rol = %s,
                            u.Usuario_graba = %s,
                            u.Maquina_graba = %s,
                            u.Fecha_graba = %s

                        WHERE u.Id_usuario = %s 
                        AND u.Estado = 1''',(Id_habilitar, Id_Perfil, Id_tema, Id_subtema, Justificacion, Fecha_fin_rol, Usuario, Maquina_graba, Fecha_graba, Id_usuario,))
                        mysql.connection.commit()
                        cur.close()
                        return json.dumps({'status':'2'})
            else: 
                json_dicti = json.loads(subtema['obj[Id_subtema]']) 
                for i in json_dicti:
                    Id_subtema =  int(i)
                    if Id_subtema > 0:
                        Id_tema = int(array['obj[Id_tema]']) 
                        Identificacion = int(array['obj[Identificacion]']) 
                        Fecha_fin_rol = array['obj[Fecha_fin_rol]']
                        Justificacion = array['obj[Justificacion]']
                        Id_Perfil = int(array['obj[Id_Perfil]'])
                        Id_habilitar = int(array['obj[Id_habilitar]'])
                        con = valida_permisos_existentes(Id_tema, Id_subtema, Identificacion, Fecha_fin_rol, Justificacion, Id_Perfil, Id_habilitar)
                        if con == 1:
                            con = 0
                        else:
                            con = 0
                            Funcionario = array['obj[Funcionario]']
                            Unidad = array['obj[Unidad]']
                            Id_codigo_cargo = int(array['obj[Id_codigo_cargo]'])
                            Cargo = array['obj[Cargo]']
                            Situacion_actual = array['obj[Situacion_actual]']
                            Usuario = array['obj[Usuario]']
                            Correo_electronico = array['obj[Correo_electronico]']
                            Fecha = datetime.now()
                            Fecha_graba = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
                            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            s.connect(("8.8.8.8", 80))
                            Maquina_graba = (s.getsockname()[0])
                            Usuario_graba = session['Usuario']
                            cur = mysql.connection.cursor()
                            cur.execute("INSERT INTO usuarios(Id_usuario, Identificacion, Funcionario, Unidad, Id_codigo_cargo, Cargo, Situacion_actual, Id_habilitar, Id_Perfil, Fecha_fin_rol, Id_tema, Id_subtema, Justificacion, Correo_electronico, Usuario, Usuario_graba, Maquina_graba, Fecha_graba) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  (Id_usuario, Identificacion, Funcionario, Unidad, Id_codigo_cargo, Cargo, Situacion_actual, Id_habilitar, Id_Perfil, Fecha_fin_rol, Id_tema, Id_subtema, Justificacion, Correo_electronico, Usuario, Usuario_graba, Maquina_graba, Fecha_graba))
                            mysql.connection.commit()
                            cur.close()
        return json.dumps({'status':'1'})
    except Exception as e:
        print("This is an error message p_registro_permisos_funcionario !{}".format(e))


def valida_permisos_existentes(Id_tema, Id_subtema, Identificacion, Fecha_fin_rol, Justificacion, Id_Perfil, Id_habilitar):
    try:
        global con
        Fecha = datetime.now()
        Fecha_grab = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        Maquina_grab = (s.getsockname()[0])
        Usuario_grab = session['Usuario']
        cur = mysql.connection.cursor()
        cur.execute('''SELECT 
                    u.Id_usuario
                FROM
                    usuarios u
                WHERE
                    u.Identificacion =  %s
                        AND u.Id_habilitar in (1,2)
                        AND u.Id_tema =  %s
                        AND u.Id_subtema =  %s
                        AND u.Id_perfil = %s''',(Identificacion, Id_tema, Id_subtema, Id_Perfil))
        mysql.connection.commit()
        dato = cur.fetchone()
        if len(dato)>0:
            cur.execute('''UPDATE usuarios usu 
            SET 
                usu.Id_habilitar =1,
                usu.Estado = 1,
                usu.Usuario_modifica =  %s,
                usu.Maquina_modifica =  %s,
                usu.Fecha_modifica =  %s,
                usu.Fecha_fin_rol = %s,
                usu.Justificacion = %s,
                usu.Id_perfil = %s,
                usu.Id_habilitar = %s
            WHERE
                usu.Id_usuario = (SELECT 
                        u.Id_usuario
                    FROM
                        usuarios u
                    WHERE
                        u.Identificacion =  %s
                            AND u.Id_habilitar in (2,1)
                            AND u.Estado = 1
                            AND u.Id_tema =  %s
                            AND u.Id_subtema =  %s)''',(Usuario_grab, Maquina_grab, Fecha_grab, Fecha_fin_rol, Justificacion, Id_Perfil, Id_habilitar, Identificacion, Id_tema, Id_subtema))
            mysql.connection.commit()
            cur.close()
            con = 1
            return (con)
    except Exception as e:
        print("This is an error message valida_permisos_existentes !{}".format(e))


@Registro_usuarios.route('/f_permisos', methods=["POST"])
def f_permisos():
    try:
        if request.method == 'POST':
            Identificacion = int(request.form['Identificacion'])
            cur = mysql.connection.cursor()
            cur.execute('''SET @row_number = 0;''')
            cur.execute('''SELECT 
                (@row_number:=@row_number + 1) AS N°,
                u.Id_usuario,
                u.Funcionario,
                u.Id_codigo_cargo,
                u.Cargo,
                u.Unidad,
                u.Id_habilitar,
                cd.Descripcion_dominio habilitado,
                p.Id_perfil,
                p.Descripcion_perfil perfil,
                t.Id_tema,
                t.Descripcion_tema tema,
                te.Id_tema Id_subtema,
                te.Descripcion_tema subtema,
                u.Justificacion,
                u.Fecha_fin_rol,
                u.Identificacion
            FROM
                usuarios u,
                temas t,
                temas te,
                ctrl_dominios cd,
                perfiles p
            WHERE
                u.Identificacion = %s
                    AND u.Estado = 1
                    AND t.Id_tema = u.Id_tema
                    AND te.Id_tema = u.Id_subtema
                    AND cd.Id_dominio = u.Id_habilitar
                    AND u.Id_perfil = p.Id_perfil
            ORDER BY 1 asc ; 
            ''',(Identificacion,))
            mysql.connection.commit()
            permisos = cur.fetchall()
            cur.close()
            return json.dumps({'status':1, 'data':permisos})
    except Exception as e:
        print("This is an error message f_permisos !{}".format(e))


@Registro_usuarios.route('/f_eliminar_permiso', methods=["POST"])
def f_eliminar_permiso():
    try:
        Id_usuario = int(request.form['Id_usuario'])
        Fecha = datetime.now()
        Fecha_grab = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        Maquina_grab = (s.getsockname()[0])
        Usuario_grab = 'rr.zambrano002'
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE usuarios u
        SET 
            u.estado = 0,
            u.Usuario_modifica = %s,
            u.Maquina_modifica = %s,
            u.Fecha_modifica = %s
        WHERE
            u.Id_usuario  = %s ''',(Usuario_grab, Maquina_grab, Fecha_grab, Id_usuario,))
        mysql.connection.commit()
        cur.close()
        return json.dumps({'status':'OK'})
    except Exception as e:
            print ("This is an error message p_eliminar_documento !{}".format(e)) 


@Registro_usuarios.route('/f_editar_permiso', methods=["POST"])
def f_editar_permiso():
    try:
        if request.method == 'POST':
            Id_usuario = int(request.form['Id_usuario'])
            cur = mysql.connection.cursor()
            cur.execute('''SET @row_number = 0;''')
            cur.execute('''SELECT 
                (@row_number:=@row_number + 1) AS N°,
                u.Id_usuario,
                u.Id_habilitar,
                cd.Descripcion_dominio habilitado,
                p.Id_perfil,
                p.Descripcion_perfil perfil,
                t.Id_tema,
                t.Descripcion_tema tema,
                te.Id_tema Id_subtema,
                te.Descripcion_tema subtema,
                u.Justificacion,
                u.Fecha_fin_rol,
                u.Identificacion
            FROM
                usuarios u,
                temas t,
                temas te,
                ctrl_dominios cd,
                perfiles p
            WHERE
                u.Id_usuario = %s
                    AND u.Estado = 1
                    AND t.Id_tema = u.Id_tema
                    AND te.Id_tema = u.Id_subtema
                    AND cd.Id_dominio = u.Id_habilitar
                    AND u.Id_perfil = p.Id_perfil
            ORDER BY 1 asc ; 
            ''',(Id_usuario,))
            mysql.connection.commit()
            permiso = cur.fetchall()
            cur.close()
            j=0
            for v in permiso:
                k = len(v)
                for i in v:
                    if v.index != "":
                        j=j+1
                        if j == k:
                            Identificacion = str(i)
                            url = "https://catalogoservicioweb.policia.gov.co/sw/token"
                            payload='password=Policia2017*&username=edwin.bustos1929@correo.policia.gov.co&grant_type=password'
                            headers = {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            }
                            response = requests.request("POST", url, headers=headers, data=payload)
                            djson = json.loads(response.text)

                            url = f'https://catalogoservicioweb.policia.gov.co/sw/api/DiversidadPonal/DatosFuncionarioPonalIdentificacion?_identificacion=' + Identificacion
                            headers = {
                            'Authorization': 'Bearer ' + djson["access_token"],
                            'Content-Type': 'application/json',
                            }
                            responses = requests.request("POST", url, headers=headers)
                            djson1 = json.loads(responses.text)
                            return json.dumps({'status':1, 'data1':djson1, 'status':1, 'data':permiso })
    except Exception as e:
        print("This is an error message f_editar_permiso !{}".format(e))
