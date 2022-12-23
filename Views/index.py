from flask import Blueprint, Flask, render_template, request, redirect, session, json
from flask_mysqldb import MySQL
import Views.Funciones.perfiles as perfil
import Views.Funciones.temas as temas
import Views.Funciones.funcionario as funcionario

app = Flask(__name__)
mysql = MySQL(app)

Index = Blueprint("index", __name__)

@Index.route('/index')
def index():
    perfile = perfil.valida_perfiles()
    t = temas.visualiza_temas()
    f = funcionario.visualiza_datos_funcionario()
    i = 1
    p = []
    if len(perfile)>0:
        for i in perfile:
            p.extend(i)
        return render_template('./Index/index.html', perfiles = p, tema = t, funcionario = f)
    else:
        return render_template('./Index/index.html')
    

