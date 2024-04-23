from flask import Flask, render_template, redirect, url_for , request, jsonify, session
from models import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from utils import *
from flask_cors import CORS
from estabelecimento import *


app = Flask("__main__")


def initialize_app():
    app.config['SECRET_KEY'] = 'CHAVESECRETA'
    database.connect()
    CORS(app)
    create_tables()  # Cria tabelas se não existirem
    print("Conexão com o banco de dados estabelecida.")

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/projetogp3'
# bd.init_app(app)
# CORS(app)
# app.secret_key = 'CHAVESECRETA'

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

# with app.app_context():
#     database.create_all()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        try:
            # Tente buscar o usuário como um Usuario
            usuario = Usuario.get(Usuario.id == user_id)
            return usuario
        except Usuario.DoesNotExist:
            try:
                # Se não for encontrado como Usuario, tente buscar como Estabelecimento
                estabelecimento = Estabelecimento.get(Estabelecimento.id == user_id)
                return estabelecimento
            except Estabelecimento.DoesNotExist:
                return None  # Se nenhum usuário for encontrado, retorne None


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
            
    # Verificar se é um estabelecimento
    # Verificar se é um estabelecimento
    estabelecimento = Estabelecimento.get_or_none(cnpj=username)
    if estabelecimento:
        if check_password_hash(estabelecimento.senha, password):
            session['user_id'] = estabelecimento.id
            login_user(estabelecimento)
            return jsonify({'tipoUsuario': 'estabelecimento'})
        else:
            return jsonify({'error': 'Senha incorreta'}), 401
    else:
        # Caso contrário, verificar se é um usuário
        usuario = Usuario.get_or_none(usuario=username)
        if usuario:
            if check_password_hash(usuario.senha, password):
                session['user_id'] = usuario.id
                login_user(usuario)
                if usuario.is_gerente():
                    return jsonify({'tipoUsuario': 'gerente'})
                elif usuario.is_garcom():
                    return jsonify({'tipoUsuario': 'garcom'})
                elif usuario.is_caixa():
                    return jsonify({'tipoUsuario': 'caixa'})
            else:
                return jsonify({'error': 'Senha incorreta'}), 401

        # Se nenhum estabelecimento ou usuário corresponderem
        return jsonify({'error': 'Usuário não encontrado'}), 404


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
        Estabelecimento.create(nome = nome, cnpj = cnpj, senha = senha, cidade = cidade, bairro = bairro, rua = rua, numero = numero, email = email)
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

    Usuario.create(nome = nome, usuario = usuario, senha = senha ,tipo = tipo ,estabelecimento_id =  estabelecimento_id)
    return jsonify({'message': 'Usuario cadastrado com sucesso'}), 200

@app.route('/cadastro', methods=['GET'])
@login_required
@estabelecimento_required
def cadastro():
    return render_template('index.html')

@app.errorhandler(403)
def forbidden(error):
    return redirect(url_for('login'))


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
    try:
        x = Categoria.get(nome = nome)
        return jsonify({'message': 'Ja existe categoria com esse nome'}), 200
    except Categoria.DoesNotExist:
            Categoria.create(nome = nome)
            return jsonify({'message': 'Categoria adicionada com sucesso'}), 200


@app.route('/adicionarproduto', methods=['POST'])
def adicionarproduto():
    data = request.get_json()
    nome = data['nome']
    categoria = data['categoria']
    valor = str_to_numeric(data['valor'])
    try:
        categoriaaux = Categoria.get(nome = categoria)
        Produto.create(nome = nome, categoria = categoriaaux, valor = valor)

        return jsonify({'message': 'Produto adicionado com sucesso'}), 200
    except IntegrityError as e:
        mensagem = extrairErro(e)
        return jsonify({'message': f"A inserção violou alguma chave: {mensagem}"}), 200



@app.route('/adicionarpedido', methods=['POST'])
def adicionarpedido():
    data = request.get_json()
    mesa_id = data['mesa_id']
    produtos = data['produtos']
    
    mesa = Mesa.get(id = mesa_id)
    if not mesa:
        return jsonify({'message': 'Mesa não encontrada.'}), 404
    
    if mesa.status == "ocupada":

        pedido = Pedido(status = 'preparando', mesa = mesa)
        pedido.save()

        for produto_inf in produtos:
            produto_id = produto_inf['id']
            quantidade = produto_inf['quantidade']
            produto = Produto.get_or_none(id = produto_id)
            pedido.adicionar_produto(produto = produto, quantidade = quantidade)
        
        return jsonify({'message': 'Pedido adicionado com sucesso!'}), 200
    else:
        return jsonify({'message': 'Mesa se encontra fechada, solicite abertura!'}), 200


@app.route('/abrirmesaespecifica', methods=['POST'])
def abrirmesaespecifica():
    data = request.get_json()
    num = data['numero']
    try: 
        Mesa.create(numero = num, status = "ocupada")
        return jsonify({'message': 'Mesa aberta com sucesso'}), 200
    except IntegrityError as e:
        mensagem = extrairErro(e)
        return jsonify({'message': f"A inserção violou alguma chave: {mensagem}"}), 200

@app.route('/abrirmesa', methods=['POST'])
def abrirmesa():
    data = request.get_json()
    num = data['numero']
    try: 
        mesa = Mesa.get(numero = num)
        mesa.status = "ocupada"
        mesa.save()
        return jsonify({'message': 'Mesa aberta com sucesso'}), 200
    except IntegrityError as e:
        mensagem = extrairErro(e)
        return jsonify({'message': f"A inserção violou alguma chave: {mensagem}"}), 200



@app.route('/fecharmesa', methods=['POST'])
def fecharmesa():
    data = request.get_json()
    num = data['numero']
    try: 
        mesa = Mesa.get(numero = num)
        mesa.status = "fechada"
        mesa.save()
        return jsonify({'message': 'Mesa fechada com sucesso'}), 200
    except Mesa.DoesNotExist as e:
        return jsonify({'message': f"Mesa nao encontrada"}), 200

@app.route('/calcularmesa', methods=['POST'])
def calcularmesa():
    data = request.get_json()
    num = data['numero']
    try: 
        mesa = Mesa.get(numero = num)
        if mesa.status == "aberta" or mesa.status == "livre":
            return jsonify({'message': 'Mesa se encontra aberta, é necessario fechar para somar'}), 404
        else:
            total = calcularConta(mesa.id)
            return jsonify({'message': f'total mesa = {total}'}), 404
    except Mesa.DoesNotExist as e:
        return jsonify({'message': f"Mesa nao encontrada"}), 200





if __name__ == '__main__':
    initialize_app()
    app.run(debug=True)