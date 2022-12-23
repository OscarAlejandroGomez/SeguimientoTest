from flask import Blueprint, Flask, render_template, request, json, session, redirect
from flask_mysqldb import MySQL
from datetime import datetime
import socket


app = Flask(__name__)
mysql = MySQL(app)



def visualiza_datos_funcionario():
    try:
        identificacion = session['Identificacion']
        cur = mysql.connection.cursor()
        cur.execute('''SELECT DISTINCT
            (g.Funcionario), g.Cargo
        FROM
            usuarios g
        WHERE
            g.Identificacion = %s
                AND g.Estado = 1''',(identificacion,))
        mysql.connection.commit()
        funcionario = cur.fetchall()
        if len(funcionario)>0:
            return funcionario
        else:
            return render_template('./Index/index.html') 
    except Exception as e:
        print("This is an error message visualiza_datos_funcionario !{}".format(e))