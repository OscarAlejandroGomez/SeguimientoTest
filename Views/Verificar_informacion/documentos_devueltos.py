from flask import Blueprint, Flask, render_template, request, json, session
from flask_mysqldb import MySQL
from datetime import datetime
import socket
import Views.Funciones.perfiles as perfil
import Views.Funciones.temas as temas
import Views.Funciones.funcionario as funcionario


app = Flask(__name__)
mysql = MySQL(app)

Documentos_devueltos = Blueprint("documentos_devueltos", __name__)

@Documentos_devueltos.route('/documentos_devueltos')
def documentos_aprobados():
    perfile = perfil.valida_perfiles()
    t = temas.visualiza_temas()
    f = funcionario.visualiza_datos_funcionario()
    i = 1
    p = []
    for i in perfile:
        p.extend(i)
    return render_template('./Verifica_informacion/documentos_devueltos.html', perfiles = p, tema = t, funcionario = f)



@Documentos_devueltos.route('/f_visualizar_subtemas_devueltos', methods=["POST"])
def f_visualizar_subtemas_devueltos():
    try:
        Id_padre_tema	 = int(request.form['Id_tema'])
        cur = mysql.connection.cursor()
        cur.execute('''SET @row_number = 0;''')
        cur.execute('''SELECT 
            (@row_number:=@row_number + 1) AS N°,
            url.Id_tema,
            url.Id_subtema,
            t.Descripcion_tema,
            (CASE gd.Id_estado_documento
			 when 3 then gd.Fecha_graba
			ELSE
              gd.Fecha_modifica
			END)as Fecha_graba,
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
                AND gd.Id_registro_url = url.Id_registro_url
                AND url.Estado = 1
                AND gd.Id_estado_documento in (4,6)
        GROUP BY t.Descripcion_tema
        ''',(Id_padre_tema,))
        mysql.connection.commit()
        Id_padre_tema = cur.fetchall()
        cur.close()
        return json.dumps({'status':1, 'data':Id_padre_tema})
    except Exception as e:
        print("This is an error message f_visualizar_subtemas_devueltos !{}".format(e))
    

@Documentos_devueltos.route('/visualiza_documento_devuelto', methods=["POST"])
def visualiza_documento_devuelto():
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
                            AND u.Id_habilitar IN (1,2)
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
        print("This is an error message visualiza_documento_devuelto !{}".format(e))
  


@Documentos_devueltos.route('/p_aprobar_documento_devuelto', methods=["POST"])
def p_aprobar_documento_devuelto():
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
            print ("This is an error message p_aprobar_documento_devuelto !{}".format(e)) 




@Documentos_devueltos.route('/p_devolver_documento_aprobado', methods=["POST"])
def p_devolver_documento_aprobado():
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
        cur.execute("INSERT INTO observaciones_documento(Id_observacion, Id_gestion_documento, Id_registro_url, Mensaje_revisor, Usuario_modifica, Maquina_modifica, Fecha_modifica) VALUES (%s, %s, %s, %s, %s, %s, %s)",  (Id_observacion, Id_gestion_documento, Id_registro_url, Mensaje_revisor, Usuario_graba, Maquina_graba, Fecha_graba,))
        mysql.connection.commit()
        cur.close()
        return json.dumps({'status':'OK'})
    except Exception as e:
            print ("This is an error message p_devolver_documento_aprobado !{}".format(e)) 



# @Documentos_devueltos.route('/f_tabla_onsevaciones_documento', methods=["POST"])
# def f_tabla_onsevaciones_documento():
#     try:
#         Id_registro_url_1 = int(request.form['Id_registro_url_1'])
#         cur = mysql.connection.cursor()
#         cur.execute('''SET @row_number = 0;''')
#         cur.execute('''SELECT 
#         (@row_number:=@row_number + 1) AS N°,
#             od.Id_observacion,
#             od.Mensaje_funcionario,
#             od.Mensaje_revisor,
#             od.Mensaje_z1,
# 			od.Fecha_graba
#         FROM
#             observaciones_documento od,
#             gestion_documentos gd,
#             registro_url url
#         WHERE
#             url.Id_registro_url = gd.Id_registro_url
#                 AND od.Id_registro_url = %s 
#                 AND url.Id_registro_url = od.Id_registro_url
#                 AND url.Estado = 1
#                 AND od.Estado = 1
#         ''',(Id_registro_url_1,))
#         mysql.connection.commit()
#         observaciones = cur.fetchall()
#         cur.close()
#         return json.dumps({'status':1, 'data':observaciones})
#     except Exception as e:
#         print("This is an error message f_tabla_onsevaciones_documento !{}".format(e))


