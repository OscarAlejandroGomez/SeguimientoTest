from flask import Blueprint, Flask, render_template, request, json, redirect, session
from flask_mysqldb import MySQL
from datetime import datetime
import socket
import Views.Funciones.perfiles as perfil
import Views.Funciones.temas as temas
import Views.Funciones.funcionario as funcionario


app = Flask(__name__)
mysql = MySQL(app)

Eliminar_informacion = Blueprint("eliminar_informacion", __name__)


@Eliminar_informacion.route('/documento_registrado')
def documento_registrado():
    try:
        Identificacion = session['Identificacion']
        perfile = perfil.valida_perfiles()
        f = funcionario.visualiza_datos_funcionario()
        i = 1
        p = []
        for i in perfile:
            p.extend(i)
        cur = mysql.connection.cursor()
        cur.execute('''SET @row_number = 0;''')
        cur.execute('''SELECT 
            (@row_number:=@row_number + 1) AS N°,
            ru.Id_registro_url,
            ru.Nombre_archivo,
            ru.Fecha_graba
        FROM
            usuarios u,
            registro_url ru
        WHERE
            u.Identificacion = ru.Identificacion
                AND u.Identificacion = %s
                AND u.Id_habilitar IN (1)
                AND ru.Estado = 1
                AND u.Id_tema = ru.Id_tema
                AND u.Estado = 1
                AND u.Id_subtema = ru.Id_subtema
                order by 1''',(Identificacion,)) 
        documentos = cur.fetchall()
        cur.close()
        return render_template('./Carga_documento/eliminar_informacion.html', documentos = documentos, perfiles = p, funcionario = f)
    except Exception as e:
            print("This is an error message documento_registrado !{}".format(e))
