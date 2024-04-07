from flask import Flask, render_template, redirect, url_for , request, jsonify, session
from models import *
from werkzeug.security import generate_password_hash, check_password_hash

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        
        # Verificar se é um usuário
        user = Usuario.query.filter_by(usuario=username).first()
        if user and check_password_hash(user.senha, password):
            session['user_id'] = user.id
            if user.tipo == 'user':
                return redirect(url_for('dashboard_user'))
            elif user.tipo == 'cnpj':
                return redirect(url_for('dashboard_cnpj'))
        
        # Verificar se é um estabelecimento
        estabelecimento = Estabelecimento.query.filter_by(cnpj=username).first()
        if estabelecimento and check_password_hash(estabelecimento.senha, password):
            session['estabelecimento_id'] = estabelecimento.id
            return redirect(url_for('dashboard_estabelecimento'))
        
        # Se nenhum usuário ou estabelecimento correspondente for encontrado
        error = 'Credenciais inválidas. Verifique o usuário, CNPJ ou senha.'
        return render_template('login.html', error=error)
    
    return render_template('login.html')












#cadastro usuario
# @app.route('/cadastrousuario', methods = ['POST'])
# def cadastroUsuario():
#     nome = request.json['nome']
#     usuario = request.json['usuario']
#     senha = request.json['senha']
#     tipo = request.json['tipo']
#     senha_hash = generate_password_hash(senha)
#     user = Usuario(nome, usuario, senha_hash, tipo)
#     db.session.add(user)
#     db.session.commit()
#     return format_usuario(user)



if __name__ == '__main__':
    app.run(debug=True)