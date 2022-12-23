from flask import Blueprint, Flask, render_template, request, json, session, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
mysql = MySQL(app)



def visualiza_gestion_documento():
    try:
        identificacion = session['Identificacion']
        cur = mysql.connection.cursor()
        cur.execute('''SELECT 
            d.Id_estado_documento,
            cd.Descripcion_dominio,
            d.Numero_gepol,
            d.Contexto_documento
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
        return gestion
    except Exception as e:
        print("This is an error message visualiza_datos_funcionario !{}".format(e))