from flask import render_template, Blueprint
from datetime import datetime

views = Blueprint("views", __name__)

@views.route("/")
def index():
    data_hora = datetime.now().strftime("%B %d, %Y %I:%M %p")
    return render_template("index.html", data_hora=data_hora)

@views.route("/professores")
def professores():
    return render_template("professores.html")

@views.route("/disciplinas")
def disciplinas():
    return render_template("disciplinas.html")

@views.route("/alunos")
def alunos():
    return render_template("alunos.html")

@views.route("/cursos")
def cursos():
    return render_template("cursos.html")

@views.route("/ocorrencias")
def ocorrencias():
    return render_template("ocorrencias.html")
