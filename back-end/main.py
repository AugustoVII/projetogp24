from flask import Flask, render_template, redirect, url_for , request, jsonify
from models import db, Usuario, format_usuario
from werkzeug.security import generate_password_hash

app = Flask("__main__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/projetogp'
db.init_app(app)

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
    senha_hash = generate_password_hash(senha)

    user = Usuario(nome, usuario, senha_hash, tipoUsuario)
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
    senha_hash = generate_password_hash(senha)
    user = Usuario(nome, usuario, senha_hash, tipo)
    db.session.add(user)
    db.session.commit()
    return format_usuario(user)



if __name__ == '__main__':
    app.run(debug=True)