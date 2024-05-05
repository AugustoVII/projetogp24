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
                elif usuario.is_cozinha():
                    return jsonify({'tipoUsuario': 'cozinha'})
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
        criarMesas(cnpj)

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

    Usuario.create(nome = nome, usuario = usuario, senha = senha ,tipo = tipo, role = tipo, estabelecimento_id =  estabelecimento_id)
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

# fakedelet para usuario
@app.route('/excluirusuario/<id>')
@login_required
@estabelecimento_required
def excluir_usuario(id):
    x = excluirFuncionario(id)
    if x :
        return jsonify({'message': 'Usuario excluido com sucesso'}), 200
    else:
        return jsonify({'message': 'Usuario nao encontrado, ou ja se encontra excluido'}), 200

# atualizar usuario com base no id
@app.route('/atualizarusuario/<id>', methods=['POST'])
@login_required
@estabelecimento_required
def atualizarusuario(id):
    data = request.get_json()
    nome = data['nome']
    usuario = data['usuario']
    senha = generate_password_hash((data['senha']))
    tipo = data['tipo']
    x = atualizarFuncionario(id, nome,usuario,senha,tipo)
    if x :
        return jsonify({'message': 'Usuario atualizado com sucesso!'}), 200
    else:
        return jsonify({'message': 'Usuario nao encontrado!'}), 200

@app.route('/infusuario', methods=['GET'])
@login_required
def infusuario():
    usuario = load_user(current_user.id)
    nome = usuario.nome
    tipo = usuario.role
    return jsonify({'nome': nome,'tipo':tipo}), 200





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


@app.route('/produto', methods=['POST'])
@login_required
@estabelecimento_or_gerente_required
def adicionarproduto():
    usuario = load_user(current_user.id)
    data = request.get_json()
    nome = data['nome']
    categoria = data['categoria']
    valor = str_to_numeric(data['valor'])
    if usuario.role == "gerente": #gerente logado
        try:
            Produto.create(nome = nome, categoria = categoria, valor = valor, estabelecimento_id = usuario.estabelecimento_id)
            return jsonify({'message': 'Produto adicionado com sucesso'}), 200
        except:
            return jsonify({'message': f"A inserção violou alguma chave"}), 400

    if usuario.role == "estabelecimento": # estabelecimento logado
        try:
            Produto.create(nome = nome, categoria = categoria, valor = valor, estabelecimento_id = usuario.id)
            return jsonify({'message': 'Produto adicionado com sucesso'}), 200
        except:
            return jsonify({'message': f"A inserção violou alguma chave"}), 400


@app.route('/produto', methods=['GET'])
@login_required
def obterProdutos():
    usuario = load_user(current_user.id)
    if usuario.role == "estabelecimento":
        produtos = obterListaProdutos(usuario.id)
        return produtos
    else:
        produtos = obterListaProdutos(usuario.estabelecimento_id)
        return produtos






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


@app.route('/mesas', methods=['GET'])
@login_required
def obterStatusMesas():
    usuario = load_user(current_user.id)
    if usuario.role == "estabelecimento":
        lista = obterListaMesas(usuario.id)
        return lista
    else:
        lista = obterListaMesas(usuario.estabelecimento_id)
        return lista






if __name__ == '__main__':
    initialize_app()
    app.run(debug=True)