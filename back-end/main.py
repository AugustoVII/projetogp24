from flask import Flask, render_template, redirect, url_for , request, jsonify, session
from models import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from utils import *
from flask_cors import CORS
from estabelecimento import *


app = Flask("__main__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/projetogp'
bd.init_app(app)
CORS(app)
app.secret_key = 'CHAVESECRETA'

@app.route('/')
def index():
    return render_template('index.html')

# Rota para servir os arquivos estáticos
@app.route('/static/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)

# Rota para lidar com todas as outras rotas do lado do cliente
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')

with app.app_context():
    bd.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Verifica se o ID de usuário é um número
    if user_id is not None:
        # Tenta buscar o usuário como um Usuario
        usuario = Usuario.query.get((user_id))
        if usuario:
            return usuario
        else:
            # Se não for encontrado como Usuario, tenta buscar como Estabelecimento
            estabelecimento = Estabelecimento.query.get((user_id))
            if estabelecimento:
                return estabelecimento
    return None


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
        bd.session.add(estabelecimento)
        bd.session.commit()
        # Exemplo de como você pode processar os dados
        # (aqui você pode realizar operações de banco de dados, validações, etc.)
        # Retornando uma resposta (por exemplo, um status de sucesso)
        # return redirect(url_for('login'))
        return jsonify({'message': 'Estabelecimento cadastrado com sucesso'}), 200

# cadastro funcionario
@app.route('/cadastrarusuario', methods=['POST'])
@login_required
@estabelecimento_required
def cadastrarUsuario():
    data = request.get_json()
    nome = data['nome']
    usuario = data['usuario']
    senha = generate_password_hash((data['senha']))
    tipo = data['tipoUsuario']
    estabelecimento_id = current_user.id

    usuarioaux = Usuario(nome, usuario,senha,tipo, estabelecimento_id)
    bd.session.add(usuarioaux)
    bd.session.commit()
    return jsonify({'message': 'Usuario cadastrado com sucesso'}), 200

@app.route('/cadastro', methods=['GET'])
@login_required
@estabelecimento_required
def cadastro():
    return render_template('index.html')

@app.errorhandler(403)
def forbidden(error):
    return redirect(url_for('login'))

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
        return jsonify({'tipoUsuario': "estabelecimento"})
    else:
        useraux = Usuario.query.filter_by(usuario=username).first()
        if useraux and check_password_hash(useraux.senha, password):
            login_user(useraux)
            # enviar tipo de usuario para o front apos o login
            if current_user.is_gerente():
                return jsonify({'tipoUsuario': "gerente"})
            elif current_user.is_garcom():
                return jsonify({'tipoUsuario': "garcom"})
            elif current_user.is_caixa():
                return jsonify({'tipoUsuario': "caixa"})
        else:
            return "usuario ou senha errado"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/listausuarios', methods=['GET'])
@login_required
@estabelecimento_required
def listagem():
    return render_template('index.html')

@app.route('/listausuario')
@login_required
@estabelecimento_required
def listausuario():
    lista = obterListaFuncionarios(current_user.id)
    return lista


@app.route('/excluirusuario/<id>')
@login_required
@estabelecimento_required
def excluir_usuario(id):
    x = excluirFuncionario(id)
    if x :
        return "Usuario excluido com sucesso!"
    else:
        return "Usuario nao encontrado, ou ja se encontra excluido "


@app.route('/homeestabelecimento')
@login_required
@estabelecimento_required
def homeestabelecimento():       
    return "estabelecimento"

@app.route('/homegarcom')
@login_required
@garcom_required
def homegarcom():       
    return "garcom"

@app.route('/homegerente')
@login_required
@gerente_required
def homegerente():
    if current_user.is_gerente():       
        return "gerente"
    else:
        return "nao é gerente"

@app.route('/homecaixa')
@login_required
@caixa_required
def homecaixa():
    if current_user.is_caixa():       
        return "caixa"
    else:
        return "nao é caixa"




@app.route('/adicionarcategoria', methods=['POST'])
def adicionarcategoria():
    data = request.get_json()
    nome = data['nome']
    categoria = Categoria(nome)
    if categoria:
        bd.session.add(categoria)
        bd.session.commit()
        return "categoria adicionada"
    else:
        return "ocorreu algum erro tente novamente"


@app.route('/adicionarproduto', methods=['POST'])
def adicionarproduto():
    data = request.get_json()
    nome = data['nome']
    categoria = data['categoria']
    valor = str_to_numeric(data['valor'])
    produto = Produto(nome,categoria,valor)
    if produto:
        bd.session.add(produto)
        bd.session.commit()
        return "produto adicionado com sucesso!"
    else:
        return "ocorreu algum erro, tente novamente"


@app.route('/adicionarpedido', methods=['POST'])
def adicionarpedido():
    data = request.get_json()
    produto_id = data['produto']
    mesa_id = data['mesa']
    pedido = Pedido(1,"PREPARANDO", mesa_id)
    produto = Produto.query.get(produto_id)
    mesa = Mesa(mesa_id)
    pedido.adicionar_produto(produto)
    mesa.adicionar_pedido(pedido)
    bd.session.add(pedido)
    bd.session.commit()
    return "ok"

@app.route('/abrirmesa', methods=['POST'])
def abrirmesa():
    data = request.get_json()
    num = data['numero']
    mesa = Mesa(num)
    bd.session.add(mesa)
    bd.session.commit()
    return "mesa aberta"












if __name__ == '__main__':
    app.run(debug=True)