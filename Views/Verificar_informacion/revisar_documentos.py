from flask import Blueprint, Flask, render_template, request, json, session
from flask_mysqldb import MySQL
import urllib, json
import requests
from datetime import datetime
import socket
import Views.Funciones.perfiles as perfil
import Views.Funciones.temas as temas
import Views.Funciones.funcionario as funcionario


app = Flask(__name__)
mysql = MySQL(app)

Revisar_documentos = Blueprint("revisar_documentos", __name__)

@Revisar_documentos.route('/revisar_documentos')
def revisar_documentos():
    perfile = perfil.valida_perfiles()
    t = temas.visualiza_temas()
    f = funcionario.visualiza_datos_funcionario()
    i = 1
    p = []
    for i in perfile:
        p.extend(i)
    return render_template('./Verifica_informacion/revisar_documentos.html', perfiles = p, tema = t, funcionario = f)


@Revisar_documentos.route('/f_visualizar_subtemas', methods=["POST"])
def f_visualizar_subtemas():
    try:
        Id_padre_tema	 = int(request.form['Id_tema'])
        cur = mysql.connection.cursor()
        cur.execute('''SET @row_number = 0;''')
        cur.execute('''select * from 
        (SELECT 
            (@row_number:=@row_number + 1) AS N°,
            url.Id_tema,
            url.Id_subtema,
            t.Descripcion_tema,
			gd.Fecha_graba,
            url.Estado,
            url.Id_registro_url,
            gd.Id_gestion_documento
        FROM
            temas t,
            registro_url url,
            gestion_documentos gd
        WHERE
            t.Id_padre_tema = %s AND t.Estado = 1
                AND url.Id_subtema = t.Id_tema
                AND gd.Id_registro_url= url.Id_registro_url
                AND url.Estado = 1
                and gd.Id_estado_documento = 3
        UNION
        SELECT 
            (@row_number:=@row_number + 1) AS N°,
            t.Id_tema,
            '0' AS Id_subtema,
            t.Descripcion_tema,
            '0' AS Fecha_graba,
            '0' as Estado,
            '' as Id_registro_url,
            '' as Id_gestion_documento
        FROM
            temas t
        WHERE
            t.Id_padre_tema = %s AND t.Id_tema
                AND t.Id_tema NOT IN (SELECT 
                                    t.Id_tema
                                FROM
                                    temas t,
                                    registro_url url,
                                    gestion_documentos gd
                                WHERE
                                    t.Estado = 1
                                        AND url.Id_subtema = t.Id_tema
                                        AND url.Estado = 1
                                        AND t.Id_padre_tema = %s
                                        AND gd.Id_registro_url = url.Id_registro_url
                                        AND gd.Id_estado_documento in (3,5)))o
                        group by o.Descripcion_tema
        ''',(Id_padre_tema, Id_padre_tema, Id_padre_tema,))
        mysql.connection.commit()
        Id_padre_tema = cur.fetchall()
        cur.close()
        return json.dumps({'status':1, 'data':Id_padre_tema})
    except Exception as e:
        print("This is an error message f_visualizar_subtemas !{}".format(e))
    

@Revisar_documentos.route('/visualiza_documento', methods=["POST"])
def visualiza_documento():
    try:
        if request.method == 'POST':
            Id_tema	 = int(request.form['Id_tema'])
            Id_subtema = int(request.form['Id_subtema'])
            cur = mysql.connection.cursor()
            cur.execute('''SELECT DISTINCT
                 (ru.Id_registro_url), ru.url, gd.Contexto_documento, t.Descripcion_tema, st.Descripcion_tema
            FROM
                usuarios u,
                registro_url ru,
                gestion_documentos gd,
                temas t,
                temas st
            WHERE
                u.Identificacion = ru.Identificacion
                    AND u.Id_habilitar IN (1 , 2)
                    AND ru.Estado = 1
                    AND u.Id_tema = ru.Id_tema
                    AND u.Id_subtema = ru.Id_subtema
                    AND gd.Id_registro_url = ru.Id_registro_url
                    AND t.Id_tema  = ru.Id_tema
                    AND st.Id_tema = ru.Id_subtema
                    AND ru.Id_registro_url = (SELECT 
                        MAX(ru.Id_registro_url)
                    FROM
                        usuarios u,
                        registro_url ru
                    WHERE
                        u.Identificacion = ru.Identificacion
                            AND u.Id_habilitar IN (1 , 2)
                            AND ru.Estado = 1
                            AND u.Id_tema = ru.Id_tema
                            AND u.Id_subtema = ru.Id_subtema
                            AND u.Id_tema = %s
                            AND u.Id_subtema = %s)
            ORDER BY 1''',(Id_tema, Id_subtema,))
            mysql.connection.commit()
            documento = cur.fetchall()
            cur.close()
            return json.dumps({'status':1, 'data':documento}) 
    except Exception as e:
        print("This is an error message visualiza_documento !{}".format(e))
  


@Revisar_documentos.route('/p_aprobar_documento', methods=["POST"])
def p_aprobar_documento():
    try:
        Id_registro_url  = int(request.form['Id_registro_url_1'])
        Id_gestion_documento  = int(request.form['Id_gestion_documento_1'])
        Fecha = datetime.now()
        Fecha_grab = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        Maquina_grab = (s.getsockname()[0])
        Usuario_grab = session['Usuario']
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE gestion_documentos u
        SET 
            u.Id_estado_documento = 5,
            u.Usuario_modifica = %s,
            u.Maquina_modifica = %s,
            u.Fecha_modifica = %s
        WHERE
            u.Id_gestion_documento = %s
            ''',(Usuario_grab, Maquina_grab, Fecha_grab, Id_gestion_documento,))
        mysql.connection.commit()
        cur.close()
        return json.dumps({'status':'OK'})
    except Exception as e:
            print ("This is an error message f_eliminar_observacion !{}".format(e)) 




@Revisar_documentos.route('/p_devolver_documento', methods=["POST"])
def p_devolver_documento():
    try:

        Id_observacion =  0
        Id_registro_url  = int(request.form['Id_registro_url_1'])  
        Id_gestion_documento  = int(request.form['Id_gestion_documento_1'])
        Mensaje_revisor = request.form['Mensaje_revisor']
        Fecha = datetime.now()
        Fecha_graba = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        Maquina_graba = (s.getsockname()[0])
        Usuario_graba = session['Usuario']
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE gestion_documentos u
        SET 
            u.Id_estado_documento = 4,
            u.Usuario_modifica = %s,
            u.Maquina_modifica = %s,
            u.Fecha_modifica = %s
        WHERE
            u.Id_gestion_documento = %s
            ''',(Usuario_graba, Maquina_graba, Fecha_graba, Id_gestion_documento,))
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO observaciones_documento(Id_observacion, Id_gestion_documento, Id_registro_url, Mensaje_revisor, Usuario_graba, Maquina_graba, Fecha_graba) VALUES (%s, %s, %s, %s, %s, %s, %s)",  (Id_observacion, Id_gestion_documento, Id_registro_url, Mensaje_revisor, Usuario_graba, Maquina_graba, Fecha_graba,))
        mysql.connection.commit()
        cur.close()
        return json.dumps({'status':'OK'})
    except Exception as e:
            print ("This is an error message p_devolver_documento !{}".format(e)) 