from flask import Blueprint, Flask, render_template, request, json, redirect, session
from flask_mysqldb import MySQL
#Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import socket
import Views.Funciones.perfiles as perfil
import Views.Funciones.gestion_documento as gestion
import Views.Funciones.temas as temas
import Views.Funciones.funcionario as funcionario

app = Flask(__name__)
mysql = MySQL(app)
Id_registro = 0

Carga_archivo = Blueprint("carga_archivo", __name__)

@Carga_archivo.route('/cargar_archivo')
def cargar_archivo():
    try:
        urls = consulta_urls()
        perfile = perfil.valida_perfiles()
        t = temas.visualiza_temas()
        f = funcionario.visualiza_datos_funcionario()
        #gestionn = gestion.visualiza_gestion_documento()
        i = 1
        p = []
        for i in perfile:
            p.extend(i) 
        if len(urls) == 0:
            return render_template('./Carga_documento/carga_archivo.html', perfiles = p, tema = t, funcionario = f )
        else:
            return render_template('./Carga_documento/carga_archivo.html', url = urls, perfiles = p, tema = t, funcionario = f )
    except Exception as e:
            print("This is an error message cargar_archivo !{}".format(e))
    


@Carga_archivo.route('/upload', methods=['POST'])
def upload():
    try:
        if request.method == 'POST':
            #Script para archivo
            file     = request.files['archivo']
            global filename 
            #basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
            filename = secure_filename(file.filename) #Nombre original del archivo
            #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
            global extension 
            extension           = os.path.splitext(filename)[1]
            #nuevoNombreFile     = stringAleatorio() + extension
            #nuevoNombreFile     = filename + extension
            global upload_path
           
            Id_registro = 0
            upload_path = os.path.join('./static/adjuntos', filename)
            # upload_path1 = upload_path.replace('\\','/') # cambia \\ por /
            # url = (upload_path1[1:]) # elimina el punto al inicio de la url, dejando inicio a partir del /
            file.save(upload_path)
            registro_datos_archivo(Id_registro)
            return redirect("/cargar_archivo")
    except Exception as e:
        print ("This is an error message upload!{}".format(e))


@Carga_archivo.route('/upload_new', methods=['POST'])
def upload_new():
    try:
        if request.method == 'POST':
            #Script para archivo
            file     = request.files['archivo']
            global filename 
            #basepath = os.path.dirname (__file__) #La ruta donde se encuentra el archivo actual
            filename = secure_filename(file.filename) #Nombre original del archivo
            #capturando extensión del archivo ejemplo: (.png, .jpg, .pdf ...etc)
            global extension 
            extension           = os.path.splitext(filename)[1]
            #nuevoNombreFile     = stringAleatorio() + extension
            #nuevoNombreFile     = filename + extension
            global upload_path
            global Id_registro
            upload_path = os.path.join ('./static/adjuntos', filename)
            file.save(upload_path)
            consulta_Id_registro_url()
            registro_datos_archivo(Id_registro)
            return redirect("/cargar_archivo")
    except Exception as e:
        print ("This is an error message upload!{}".format(e))
    

def registro_datos_archivo(Id_registro):
    try:
        Id_registro_url = Id_registro
        if Id_registro_url > 0:
            upload_path1 = upload_path.replace('\\','/') # cambia \\ por /
            url = (upload_path1[1:]) # elimina el punto al inicio de la url, dejando inicio a partir del /
            formato = (extension[1:])
            filename1 = filename
            Identificacion = session['Identificacion'] 
            Id_usuario = session['Id_usuario'] 
            Fecha = datetime.now()
            Fecha_graba = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            Maquina_graba = (s.getsockname()[0])
            Usuario_graba =  session['Usuario']
            Id_tema = session['Id_tema']
            Id_subtema =  session['Id_subtema']
            cur = mysql.connection.cursor()
            cur.execute('''UPDATE registro_url d 
            SET 
                d.url = %s,
                d.formato = %s,
                d.Id_usuario = %s,
                d.Id_tema = %s,
                d.Id_subtema  = %s,
                d.Usuario_modifica = %s,
                d.Maquina_modifica = %s,
                d.Fecha_modifica = %s,
                d.nombre_archivo = %s
            WHERE
                d.Id_registro_url = %s
                AND d.Identificacion = %s''',(url, formato, Id_usuario, Id_tema, Id_subtema, Usuario_graba, Maquina_graba, Fecha_graba, filename1, Id_registro_url, Identificacion,))
            mysql.connection.commit()
            cur.close()
            Id_registro = 0
            return redirect("/cargar_archivo")
        else:
            upload_path1 = upload_path.replace('\\','/') # cambia \\ por /
            url = (upload_path1[1:]) # elimina el punto al inicio de la url, dejando inicio a partir del /
            formato = (extension[1:])
            filename1 = filename
            Identificacion = session['Identificacion'] 
            Id_usuario = session['Id_usuario'] 
            Fecha = datetime.now()
            Fecha_graba = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            Maquina_graba = (s.getsockname()[0])
            Usuario_graba =  session['Usuario']
            Id_tema = session['Id_tema']
            Id_padre_tema =  session['Id_subtema']
            verifica_documento_activo()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO registro_url(Id_registro_url, url, formato, Identificacion, Id_usuario, Id_tema, Id_subtema, Usuario_graba, Maquina_graba, Fecha_graba, nombre_archivo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  (Id_registro_url, url, formato, Identificacion, Id_usuario, Id_tema, Id_padre_tema, Usuario_graba, Maquina_graba, Fecha_graba, filename1))
            mysql.connection.commit()
            cur.close()
            return redirect("/cargar_archivo")
    except Exception as e:
        print("This is an error message registro_datos_archivo !{}".format(e))
    finally:
        cur.close()


def consulta_urls():
    try:
        Identificacion = session['Identificacion'] 
        cur = mysql.connection.cursor()
        cur.execute('''SELECT 
            distinct(ru.Id_registro_url), ru.url
            FROM
                usuarios u,
                registro_url ru
               
            WHERE
                u.Identificacion = %s
                    AND u.Id_habilitar IN (1 , 2)
                    AND ru.Estado = 1
                    AND u.Id_tema = ru.Id_tema
                    AND u.Id_subtema = ru.Id_subtema
                   
                AND ru.Id_registro_url = (SELECT 
                    MAX(ru.Id_registro_url)
                FROM
                    usuarios u,
                    registro_url ru
                WHERE
                    u.Identificacion = ru.Identificacion
                        AND u.Identificacion = %s
                        AND u.Id_habilitar in (1,2)
                        AND ru.Estado = 1
                        AND u.Id_tema = ru.Id_tema
                        AND u.Id_tema = %s
                        AND u.Id_subtema = ru.Id_subtema
                        AND u.Id_subtema = %s)
        ORDER BY 1; 
        ''',(Identificacion, Identificacion, session['Id_tema'], session['Id_subtema']))
        mysql.connection.commit()
        urls = cur.fetchall()
        return urls
    except Exception as e:
        print("This is an error message consulta_urls !{}".format(e))
    finally:
        cur.close()
    

def consulta_Id_registro_url():
    try:
        global Id_registro
        Identificacion = session['Identificacion'] 
        cur = mysql.connection.cursor()
        cur.execute('''SELECT 
            MAX(ru.Id_registro_url)
        FROM
            usuarios u,
            registro_url ru
        WHERE
            u.Identificacion = ru.Identificacion
                AND u.Identificacion = %s
                AND u.Id_habilitar in (1,2)
                AND ru.Estado = 1
                AND u.Id_tema = ru.Id_tema
                AND u.Id_tema = %s
                AND u.Id_subtema = ru.Id_subtema
                AND u.Id_subtema = %s
        ORDER BY 1; 
        ''',(Identificacion, session['Id_tema'], session['Id_subtema']))
        mysql.connection.commit()
        Id_registro_url = cur.fetchall()
        Id_registro = Id_registro_url[0]
        for i in Id_registro_url[0]:
            Id_registro = i
        return Id_registro
    except Exception as e:
        print("This is an error message consulta_urls !{}".format(e))
    finally:
        cur.close()




@Carga_archivo.route('/p_eliminar_documento', methods=["POST"])
def p_eliminar_documento():
    try:
        Id_documento = int(request.form['Id_documento'])
        Fecha = datetime.now()
        Fecha_grab = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        Maquina_grab = (s.getsockname()[0])
        Usuario_grab = 'rr.zambrano002'
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE registro_url u
        SET 
            u.estado = 0,
            u.Usuario_modifica = %s,
            u.Maquina_modifica = %s,
            u.Fecha_modifica = %s
        WHERE
            u.Id_registro_url = %s ''',(Usuario_grab, Maquina_grab, Fecha_grab, Id_documento,))
        mysql.connection.commit()
        cur.close()
        return json.dumps({'status':'OK'})
    except Exception as e:
            print ("This is an error message p_eliminar_documento !{}".format(e))
    finally:
        cur.close()



def verifica_documento_activo():
    try:
        Identificacion = session['Identificacion'] 
        Fecha = datetime.now()
        Fecha_grab = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        Maquina_grab = (s.getsockname()[0])
        Usuario_grab = session['Usuario']
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE registro_url,
        (SELECT Y.MAXURL from
            (SELECT 
            MAX(ru.Id_registro_url) AS MAXURL
            FROM
            usuarios u,
            registro_url ru
            WHERE
            u.Identificacion = ru.Identificacion
            AND u.Identificacion = %s
            AND u.Id_habilitar = 1
            AND ru.Estado = 1
            AND u.Id_tema = ru.Id_tema
            AND u.Id_tema = %s
            AND u.Id_subtema = ru.Id_subtema
            AND u.Id_subtema = %s) as Y) as X
        SET registro_url.estado = 0,
        registro_url.Usuario_modifica = %s,
        registro_url.Maquina_modifica = %s,
        registro_url.Fecha_modifica = %s
        WHERE registro_url.Id_registro_url = X.MAXURL''',(Identificacion, session['Id_tema'], session['Id_subtema'], Usuario_grab, Maquina_grab, Fecha_grab))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print("This is an error message verifica_documento_activo !{}".format(e))
    finally:
        cur.close()


@Carga_archivo.route('/f_estado_documento', methods=["POST"])
def f_estado_documento():
    try:
        if request.method == 'POST':
            Estado = request.form['Estado']
            cur = mysql.connection.cursor()
            cur.execute('''SELECT 
                d.Id_dominio, d.Descripcion_dominio
            FROM
                ctrl_dominios d
            WHERE
                d.Id_padre = 3 AND d.Estado = %s''',(Estado,))
            mysql.connection.commit()
            Estado_documento = cur.fetchall()
            cur.close()
            return json.dumps({'status':'OK', 'data':Estado_documento })
    except Exception as e:
        print("This is an error message f_estado_documento !{}".format(e))


@Carga_archivo.route('/p_enviar_documento_a_SEPRI', methods=["POST"])
def p_enviar_documento_a_SEPRI():
    try:
        if request.method =='POST':
            array = request.form.to_dict()
            Id_gestion_documento  = int(array['obj[Id_gestion_documento]'])
            if Id_gestion_documento > 0:
                Id_estado_documento = 3
                Numero_gepol = array['obj[Numero_gepol]']
                Contexto_documento = array['obj[Contexto_documento]']
                Usuario_graba = session['Usuario']
                Fecha = datetime.now()
                Fecha_graba = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                Maquina_graba = (s.getsockname()[0])
                cur = mysql.connection.cursor()
                cur.execute('''UPDATE gestion_documentos d 
                SET 
                    d.Id_estado_documento = 3,
                    d.Numero_gepol = %s,
                    d.Contexto_documento = %s,
                    d.Usuario_modifica = %s,
                    d.Maquina_modifica = %s,
                    d.Fecha_modifica  = %s
                WHERE
                    d.Id_gestion_documento = %s
                    AND d.Identificacion = %s''',(Numero_gepol, Contexto_documento, Usuario_graba, Maquina_graba, Fecha_graba, Id_gestion_documento, session['Identificacion'],))
                mysql.connection.commit()
                cur.close()
                return json.dumps({'status':'2'})
            else:
                Id_gestion_documento = int(array['obj[Id_gestion_documento]'])
                Id_estado_documento = 3
                Numero_gepol = array['obj[Numero_gepol]']
                Contexto_documento = array['obj[Contexto_documento]']
                cur = mysql.connection.cursor()
                cur.execute('''SELECT 
                    url.Id_registro_url
                FROM
                    registro_url url
                WHERE
                    url.Identificacion = %s
                        AND url.Estado = 1''',(session['Identificacion'],))
                mysql.connection.commit()
                Id_registro = cur.fetchone()
                Id_registro_url = Id_registro[0]
                Fecha = datetime.now()
                Fecha_graba = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                Maquina_graba = (s.getsockname()[0])
                Identificacion = session['Identificacion']
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO gestion_documentos(Id_gestion_documento, Id_registro_url, Identificacion, Id_estado_documento, Numero_gepol, Contexto_documento, Usuario_graba, Maquina_graba, Fecha_graba) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",  (Id_gestion_documento, Id_registro_url, Identificacion, Id_estado_documento, Numero_gepol, Contexto_documento, session['Usuario'], Maquina_graba, Fecha_graba))
                mysql.connection.commit()
                cur.close()
                return json.dumps({'status':'OK' })
    except Exception as e:
        print("This is an error message p_enviar_documento_a_SEPRI !{}".format(e))



@Carga_archivo.route('/f_visualiza_gestion_documento', methods=["POST"])
def f_visualiza_gestion_documento():
    try:
        if request.method =='POST':
            identificacion = session['Identificacion']
            cur = mysql.connection.cursor()
            cur.execute('''SELECT 
                d.Id_gestion_documento,
                d.Id_estado_documento,
                cd.Descripcion_dominio,
                d.Numero_gepol,
                d.Contexto_documento,
                url.Id_registro_url 
            FROM
                gestion_documentos d,
                registro_url url,
                ctrl_dominios cd
            WHERE
                d.Id_registro_url = url.Id_registro_url
                    AND url.Estado = 1
                    AND url.Identificacion = %s
                    AND cd.Id_dominio = d.Id_estado_documento''',(identificacion,))
            mysql.connection.commit()
            gestion = cur.fetchall()
            cur.close()
            return json.dumps({'status':'OK', 'data':gestion})
    except Exception as e:
        print("This is an error message visualiza_datos_funcionario !{}".format(e))


@Carga_archivo.route('/p_enviar_mensaje', methods=["POST"])
def p_enviar_mensaje():
    try:
        if request.method =='POST':
            array = request.form.to_dict()
            Id_observacion = int(array['obj[Id_observacion]'])
            if Id_observacion>0:
                Mensaje_funcionario = array['obj[Mensaje_funcionario]']
            else:
                Mensaje_funcionario = array['obj[Mensaje_funcionario]']
                # Mensaje_revisor = array['obj[Mensaje_revisor]']  
                # Mensaje_z1 = array['obj[Mensaje_z1]']
                cur = mysql.connection.cursor()
                cur.execute('''SELECT 
                    url.Id_registro_url
                FROM
                    registro_url url
                WHERE
                    url.Identificacion = %s
                        AND url.Estado = 1''',(session['Identificacion'],))
                mysql.connection.commit()
                Id_registro = cur.fetchone()
                Id_registro_url = Id_registro[0]
                cur = mysql.connection.cursor()
                cur.execute('''SELECT 
                    MAX(gd.Id_gestion_documento) AS Id_gestion_documento
                FROM
                    registro_url url,
                    gestion_documentos gd
                WHERE
                    url.Identificacion = gd.Identificacion
                        AND url.Identificacion = %s
                        AND url.Estado = 1''',(session['Identificacion'],))
                mysql.connection.commit()
                Id_gestion_document = cur.fetchone()
                Id_gestion_documento = Id_gestion_document[0]
                Fecha = datetime.now()
                Fecha_graba = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                Maquina_graba = (s.getsockname()[0])
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO observaciones_documento(Id_observacion, Mensaje_funcionario, Id_registro_url, Id_gestion_documento, Usuario_graba, Maquina_graba, Fecha_graba) VALUES (%s, %s, %s, %s, %s, %s, %s)", (Id_observacion, Mensaje_funcionario, Id_registro_url, Id_gestion_documento, session['Usuario'], Maquina_graba, Fecha_graba))
                mysql.connection.commit()
                cur.close()
                return json.dumps({'status':'OK' })
    except Exception as e:
        print("This is an error message visualiza_datos_funcionario !{}".format(e))



# @Carga_archivo.route('/f_tabla_onsevaciones_documento', methods=["POST"])
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
#                 AND url.Identificacion = %s
#                 AND url.Estado = 1
#                 AND od.Estado = 1
#         ''',(Id_registro_url_1, session['Identificacion'],))
#         mysql.connection.commit()
#         observaciones = cur.fetchall()
#         cur.close()
#         return json.dumps({'status':1, 'data':observaciones})
#     except Exception as e:
#         print("This is an error message f_tabla_onsevaciones_documento !{}".format(e))



@Carga_archivo.route('/f_eliminar_observacion', methods=["POST"])
def f_eliminar_observacion():
    try:
        Id_observacion  = int(request.form['Id_observacion'])
        Fecha = datetime.now()
        Fecha_grab = (Fecha.strftime('%Y-%m-%d %H:%M:%S'))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        Maquina_grab = (s.getsockname()[0])
        Usuario_grab = 'rr.zambrano002'
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE observaciones_documento u
        SET 
            u.estado = 0,
            u.Usuario_modifica = %s,
            u.Maquina_modifica = %s,
            u.Fecha_modifica = %s
        WHERE
            u.Id_observacion  = %s
            AND u.Estado= 1''',(Usuario_grab, Maquina_grab, Fecha_grab, Id_observacion,))
        mysql.connection.commit()
        cur.close()
        return json.dumps({'status':'OK'})
    except Exception as e:
            print ("This is an error message f_eliminar_observacion !{}".format(e)) 

