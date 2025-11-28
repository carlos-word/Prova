from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask
from views import views

app = Flask(__name__)
app.register_blueprint(views)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///professores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    disciplina = db.Column(db.String(30), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

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
    hora = datetime.now().strftime('%d/%m/%Y %H:%M')

    return render_template(
        'professores.html',
        professores=todos_professores,
        hora=hora
    )

@app.route('/disciplinas')
@app.route('/alunos')
@app.route('/cursos')
@app.route('/ocorrencias')
def nao_disponivel():
    hora = datetime.now().strftime('%d/%m/%Y %H:%M')
    return render_template("nao_disponivel.html", hora=hora)


if __name__ == '__main__':
    app.run()
