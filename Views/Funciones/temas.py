from flask import Blueprint, Flask, render_template, request, json, session, redirect
from flask_mysqldb import MySQL
from datetime import datetime
import socket


app = Flask(__name__)
mysql = MySQL(app)


def visualiza_temas():
    try:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT DISTINCT
            (t.Id_tema), t.Descripcion_tema AS Temas
        FROM
            temas t
        WHERE
            t.Id_padre_tema = 0 AND t.Estado = 1
        ORDER BY t.Id_tema ASC''')
        mysql.connection.commit()
        temas = cur.fetchall()
        if len(temas)>0:
            return temas
        else:
            return render_template('./Index/index.html') 
    except Exception as e:
        print("This is an error message visualiza_temas !{}".format(e))