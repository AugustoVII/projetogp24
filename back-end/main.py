from flask import Flask, render_template, redirect, url_for , request, jsonify, session
from models import *
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask("__main__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/projetogp'
db.init_app(app)

app.secret_key = 'CHAVESECRETA'


with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Estabelecimento.query.get(int(user_id))

@app.route("/")
def index():
    return redirect(url_for('cadastro'))

@app.route("/cadastro")
def cadastro():
    return render_template("index.html")


# cadastro empresa
@app.route('/cadastrar', methods=['POST'])
def cadastrar_estabelecimento():
    data = request.get_json()

    nome = data['nome']
    cnpj = data['cnpj']
    senha = generate_password_hash((data['senha']))
    cidade = data['cidade']
    bairro= data['bairro']
    rua = data['rua']
    numero  = data['numero']
    email = data['email']
    conf_email = data['confirmarEmail']
    if email == conf_email:
    
        estabelecimento = Estabelecimento(nome, cnpj, senha, cidade, bairro, rua, numero, email)
        db.session.add(estabelecimento)
        db.session.commit()
        # Exemplo de como você pode processar os dados
        # (aqui você pode realizar operações de banco de dados, validações, etc.)
        # Retornando uma resposta (por exemplo, um status de sucesso)
        return jsonify({'message': 'Estabelecimento cadastrado com sucesso'}), 200

# cadastro usuario
@app.route('/cadastrarusuario', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    nome = data['nome']
    usuario = data['usuario']
    senha = generate_password_hash((data['senha']))
    tipo = data['tipo']
    estabelecimento_id = 1

    usuarioaux = Usuario(nome, usuario,senha,tipo, estabelecimento_id)
    db.session.add(usuarioaux)
    db.session.commit()
    return jsonify({'message': 'Usuario cadastrado com sucesso'}), 200





@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
            
        # Verificar se é um usuário
    user = Estabelecimento.query.filter_by(cnpj=username).first()
    if user and check_password_hash(user.senha, password):
        session['user_id'] = user.id
        login_user(user)
        return jsonify({'message': 'estabelecimento'})
    else:
        user = Usuario.query.filter_by(usuario=username).first()
        if user and check_password_hash(user.senha, password):
            login_user(user)
            return jsonify({'message': 'usuario'})

        




if __name__ == '__main__':
    app.run(debug=True)