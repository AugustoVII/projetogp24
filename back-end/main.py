from flask import Flask, render_template, redirect, url_for , request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask("__main__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/projetogp'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Usuario: {self}"
    
    def __init__(self, nome, usuario, senha, tipo):
        self.nome = nome
        self.usuario = usuario
        self.senha = senha
        self.tipo = tipo

def format_usuario(usuario):
    return {
        "nome": usuario.nome,
        "usuario": usuario.usuario,
        "tipo": usuario.tipo,
        "senha": usuario.senha
    }

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return redirect(url_for('cadastro'))

@app.route("/cadastro")
def cadastro():
    return render_template("index.html")



@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()

    # Aqui você pode acessar os dados enviados pelo React
    nome = data['nome']
    usuario = data['usuario']
    senha = data['senha']
    tipoUsuario = data['tipoUsuario']
    user = Usuario(nome, usuario, senha, tipoUsuario)
    db.session.add(user)
    db.session.commit()
    # Exemplo de como você pode processar os dados
    # (aqui você pode realizar operações de banco de dados, validações, etc.)
    print(f"Nome: {nome}, Usuário: {usuario}, Senha: {senha}, Tipo de Usuário: {tipoUsuario}")

    # Retornando uma resposta (por exemplo, um status de sucesso)
    return jsonify({'message': 'Usuário cadastrado com sucesso'}), 200



#cadastro usuario
@app.route('/cadastrousuario', methods = ['POST'])
def cadastroUsuario():
    nome = request.json['nome']
    usuario = request.json['usuario']
    senha = request.json['senha']
    tipo = request.json['tipo']
    user = Usuario(nome, usuario, senha, tipo)
    db.session.add(user)
    db.session.commit()
    return format_usuario(user)



if __name__ == '__main__':
    app.run(debug=True)