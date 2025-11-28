from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz # Certifique-se de ter instalado: pip install pytz

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///professores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    disciplina = db.Column(db.String(30), nullable=False)


# ---------------------- INDEX ----------------------
@app.route('/')
def index():
    # Configura o fuso horário (São Paulo)
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso_horario)
    
    # MUDANÇA 1: Formato "Estilo Fabio" (Mês Dia, Ano Hora AM/PM)
    hora_formatada = agora.strftime('%B %d, %Y %I:%M %p')
    
    # MUDANÇA 2: A variável deve se chamar 'hora' para funcionar com {{ hora }} no HTML
    return render_template('index.html', hora=hora_formatada)


# ----------------- PROFESSORES ---------------------
@app.route('/professores', methods=['GET', 'POST'])
def professores():
    if request.method == 'POST':
        nome = request.form['nome']
        disciplina = request.form['disciplina']

        novo = Professor(nome=nome, disciplina=disciplina)
        db.session.add(novo)
        db.session.commit()

        return redirect('/professores')

    todos_professores = Professor.query.all()
    
    # Aqui mantivemos o formato padrão PT-BR para a lista, se preferir
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    hora = datetime.now(fuso_horario).strftime('%d/%m/%Y %H:%M')

    return render_template(
        'professores.html',
        professores=todos_professores,
        hora=hora
    )


# ------------- PÁGINAS NÃO DISPONÍVEIS --------------
@app.route('/disciplinas')
@app.route('/alunos')
@app.route('/cursos')
@app.route('/ocorrencias')
def nao_disponivel():
    fuso_horario = pytz.timezone('America/Sao_Paulo')
    # Usando o formato completo aqui também para ficar bonito
    hora = datetime.now(fuso_horario).strftime('%B %d, %Y %I:%M %p')
    
    # MUDANÇA 3: O template nao_disponivel.html espera 'now', não 'hora'
    return render_template("nao_disponivel.html", now=hora)


if __name__ == '__main__':
    # Garante que as tabelas existam antes de rodar
    with app.app_context():
        db.create_all()
    app.run(debug=True)
