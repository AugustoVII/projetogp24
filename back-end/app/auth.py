from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Usuario, Estabelecimento, Mesa
from .utils import *


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    estabelecimento = Estabelecimento.get_or_none(cnpj=username)
    if estabelecimento and check_password_hash(estabelecimento.senha, password):
        session['user_id'] = estabelecimento.id
        login_user(estabelecimento)
        return jsonify({'tipoUsuario': 'estabelecimento'})
    else:
        usuario = Usuario.get_or_none(usuario=username)
        if usuario and check_password_hash(usuario.senha, password):
            session['user_id'] = usuario.id
            login_user(usuario)
            if usuario.is_gerente():
                return jsonify({'tipoUsuario': 'gerente'})
            elif usuario.is_garcom():
                return jsonify({'tipoUsuario': 'garcom'})
            elif usuario.is_caixa():
                return jsonify({'tipoUsuario': 'caixa'})
            elif usuario.is_cozinheiro():
                return jsonify({'tipoUsuario': 'cozinheiro'})
        return jsonify({'error': 'Usuário não encontrado ou senha incorreta'}), 404

@auth_bp.route('/logout')
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso'}), 200

@auth_bp.route('/cadastrar', methods=['POST'])
def cadastrar_estabelecimento():
    data = request.get_json()
    nome = data['nome']
    cnpj = data['cnpj']
    senha = generate_password_hash(data['senha'])
    cidade = data['cidade']
    bairro = data['bairro']
    rua = data['rua']
    numero = data['numero']
    email = data['email']
    quantMesas = int(data['quantMesas'])

    try:
        estabelecimento = Estabelecimento.create(nome=nome, cnpj=cnpj, senha=senha, cidade=cidade, bairro=bairro, rua=rua, numero=numero, email=email)
        for i in range(quantMesas):
            Mesa.create(numero=i+1, status="livre", estabelecimento_id=estabelecimento.id, active=True)
        return jsonify({'message': 'Estabelecimento cadastrado com sucesso'}), 200
    except Exception as e:
        return jsonify({'message': f'Aconteceu algum erro: {str(e)}'}), 400

@auth_bp.route('/cadastrarusuario', methods=['POST'])
@login_required
@estabelecimento_required
def cadastrar_usuario():
    data = request.get_json()
    nome = data['nome']
    usuario = data['usuario']
    senha = generate_password_hash(data['senha'])
    tipo = data['tipoUsuario']
    estabelecimento_id = current_user.id

    Usuario.create(nome=nome, usuario=usuario, senha=senha, tipo=tipo, role=tipo, estabelecimento_id=estabelecimento_id)
    return jsonify({'message': 'Usuário cadastrado com sucesso'}), 200
