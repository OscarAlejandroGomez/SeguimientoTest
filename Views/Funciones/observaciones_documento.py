from flask import Blueprint, Flask, render_template, request, json, session
from flask_mysqldb import MySQL
from datetime import datetime
import socket
import Views.Funciones.perfiles as perfil
import Views.Funciones.temas as temas
import Views.Funciones.funcionario as funcionario


app = Flask(__name__)
mysql = MySQL(app)

Observaciones_documento = Blueprint("observaciones_documento", __name__)


@Observaciones_documento.route('/f_tabla_onsevaciones_documento', methods=["POST"])
def f_tabla_onsevaciones_documento():
    try:
        Id_registro_url_1 = int(request.form['Id_registro_url_1'])
        cur = mysql.connection.cursor()
        cur.execute('''SET @row_number = 0;''')
        cur.execute('''SELECT 
        (@row_number:=@row_number + 1) AS N°,
            od.Id_observacion,
            od.Mensaje_funcionario,
            od.Mensaje_revisor,
            od.Mensaje_z1,
			od.Fecha_graba
        FROM
            observaciones_documento od,
            gestion_documentos gd,
            registro_url url
        WHERE
            url.Id_registro_url = gd.Id_registro_url
                AND od.Id_registro_url = %s 
                AND url.Id_registro_url = od.Id_registro_url
                AND url.Estado = 1
                AND od.Estado = 1
        ''',(Id_registro_url_1,))
        mysql.connection.commit()
        observaciones = cur.fetchall()
        cur.close()
        return json.dumps({'status':1, 'data':observaciones})
    except Exception as e:
        print("This is an error message f_tabla_onsevaciones_documento !{}".format(e))




