from flask import Blueprint, Flask, render_template, request, json, session, redirect
from flask_mysqldb import MySQL
from datetime import datetime
import socket


app = Flask(__name__)
mysql = MySQL(app)


def valida_perfiles():
    try:
        identificacion = session['Identificacion']
        if identificacion == 1061702317:
            cur = mysql.connection.cursor()
            cur.execute('''SELECT 
                distinct(p.Id_perfil)
            FROM
                usuarios u,
                perfiles p
            WHERE
                u.Id_perfil = p.Id_perfil
                    AND u.Id_habilitar = 1
                    AND u.Estado = 1
                    AND p.Estado = 1
                    AND u.Identificacion = %s
            ORDER BY p.Id_perfil ASC''',(identificacion,))
            mysql.connection.commit()
            perfiles = cur.fetchall()
            if len(perfiles)>0:
                return perfiles
            else:
                return render_template('./Index/index.html')
        else:
            cur = mysql.connection.cursor()
            cur.execute('''SELECT 
                distinct(p.Id_perfil)
            FROM
                usuarios u,
                perfiles p
            WHERE
                u.Id_perfil = p.Id_perfil
                    AND u.Id_habilitar = 1
                    AND u.Estado = 1
                    AND p.Estado = 1
                    AND u.Fecha_fin_rol > SYSDATE()
                    AND u.Identificacion = %s
            ORDER BY p.Id_perfil ASC''',(identificacion,))
            mysql.connection.commit()
            perfiles = cur.fetchall()
            if len(perfiles)>0:
                return perfiles
            else:
                return render_template('./Index/index.html') 
    except Exception as e:
        print("This is an error message valida_perfiles !{}".format(e))