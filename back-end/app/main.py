from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Mesa, Pedido, Produto, PedidoProduto
from .utils import *
from .estabelecimento import *
from .auth import *
from werkzeug.security import generate_password_hash, check_password_hash
from .__init__ import *


main_bp = Blueprint('main', __name__)

# @main_bp.route('/')
# def index():
#     return render_template('index.html')

# @main_bp.route('/static/<path:path>')
# def static_proxy(path):
#     return main_bp.send_static_file(path)

# @main_bp.route('/<path:path>')
# def catch_all(path):
#     return render_template('index.html')

@main_bp.route('/homeestabelecimento')
@login_required
@estabelecimento_required
def homeestabelecimento():
    return "estabelecimento"

@main_bp.route('/homegarcom')
@login_required
@garcom_required
def homegarcom():
    return "garcom"

@main_bp.route('/homegerente')
@login_required
@gerente_required
def homegerente():
    return "gerente"

@main_bp.route('/homecaixa')
@login_required
@caixa_required
def homecaixa():
    return "caixa"



@main_bp.route('/cadastrar', methods=['GET'])
def cadastroget():
    return "fdsfs"


@main_bp.errorhandler(403)
def forbidden(error):
    return redirect(url_for('login'))



# @main_bp.route('/listausuarios', methods=['GET'])
# @login_required
# @estabelecimento_required
# def listagem():
#     return render_template('index.html')

# @main_bp.route('/listausuario')
# @login_required
# @estabelecimento_required
# def listausuario():
#     lista = obterListaFuncionarios(current_user.id)
#     return lista

# # fakedelet para usuario
# @main_bp.route('/excluirusuario/<id>')
# @login_required
# @estabelecimento_required
# def excluir_usuario(id):
#     x = excluirFuncionario(id)
#     if x :
#         return jsonify({'message': 'Usuario excluido com sucesso'}), 200
#     else:
#         return jsonify({'message': 'Usuario nao encontrado, ou ja se encontra excluido'}), 400

# # atualizar usuario com base no id
# @main_bp.route('/atualizarusuario/<id>', methods=['POST'])
# @login_required
# @estabelecimento_required
# def atualizarusuario(id):
#     data = request.get_json()
#     nome = data['nome']
#     usuario = data['usuario']
#     senha = generate_password_hash((data['senha']))
#     tipo = data['tipo']
#     x = atualizarFuncionario(id, nome,usuario,senha,tipo)
#     if x :
#         return jsonify({'message': 'Usuario atualizado com sucesso!'}), 200
#     else:
#         return jsonify({'message': 'Usuario nao encontrado!'}), 400

# @main_bp.route('/infusuario', methods=['GET'])
# @login_required
# def infusuario():
#     usuario = (current_user)
#     nome = usuario.nome
#     tipo = usuario.role
#     return jsonify({'nome': nome,'tipo':tipo}), 200





# @main_bp.route('/homeestabelecimento')
# @login_required
# @estabelecimento_required
# def homeestabelecimento():       
#     return "estabelecimento"

# @main_bp.route('/homegarcom')
# @login_required
# @garcom_required
# def homegarcom():       
#     return "garcom"

# @main_bp.route('/homegerente')
# @login_required
# @gerente_required
# def homegerente():
#     if current_user.is_gerente():       
#         return "gerente"
#     else:
#         return "nao é gerente"

# @main_bp.route('/homecaixa')
# @login_required
# @caixa_required
# def homecaixa():
#     if current_user.is_caixa():       
#         return "caixa"
#     else:
#         return "nao é caixa"


# def obterIdEst(usuario):
#     if usuario.role == "estabelecimento":
#         return usuario.id
#     else:
#         return usuario.estabelecimento_id


# @main_bp.route('/produto', methods=['POST'])
# @login_required
# @gerente_required
# def AddProd():
#     idEst = obterIdEst((current_user))
    
#     data = request.get_json()
#     nome = data['nome']
#     categoria = data['categoria']
#     valor = str_to_numeric(data['valor'])
#     try:
#         Produto.create(nome = nome, categoria = categoria, valor = valor, estabelecimento_id = idEst)
#         return jsonify({'message': 'Produto adicionado com sucesso'}), 200
#     except:
#         return jsonify({'message': 'erro ao inserir'}), 400

# @main_bp.route('/produto', methods=['GET'])
# @login_required
# def obterProdutos():
#     idEst =obterIdEst((current_user))
#     produtos = obterListaProdutos(idEst)
#     return produtos



# @main_bp.route('/pedido', methods=['POST'])
# @login_required
# def adicionarpedido():
#     usuario = (current_user)
#     if usuario.role == "estabelecimento":
#         idEst = usuario.id
#     else:
#         idEst = usuario.estabelecimento_id

#     data = request.get_json()
    
#     pedidos = data['pedidos']
#     mesa_id = data['pedidos'][0]['mesaId']
#     try:
#         mesa = Mesa.get(id = mesa_id)
#         mesa.status = "ocupada"
#         mesa.save()
#         pedido = Pedido(status = 'andamento', mesa = mesa, estabelecimento_id = idEst )
#         pedido.save()
#     except:
#         return jsonify({'message': 'Mesa se encontra fechada, solicite abertura!'}), 400
        
#     for lista in pedidos:
#         prato = lista['prato']
#         quantidade = lista['quantidade']
#         produto = Produto.get(nome = prato)
#         pedido.adicionar_produto(produto = produto, quantidade = quantidade, status = "preparando")
#     return jsonify({'message': 'Pedido adicionado com sucesso!'}), 200        

# @main_bp.route('/pedido', methods=['GET'])
# @login_required
# def obterPedidos():
#     usuario = (current_user)
#     if usuario.role == "estabelecimento":
#         idEst = usuario.id
#     else:
#         idEst = usuario.estabelecimento_id
#     consulta = PedidoProduto.select(PedidoProduto, Pedido, Produto, Mesa).where((Pedido.estabelecimento_id == idEst) & (PedidoProduto.status == "preparando")).join(Pedido, JOIN.INNER, on=(Pedido.id == PedidoProduto.pedido)).join(Produto, JOIN.INNER, on=(PedidoProduto.produto == Produto.id)).join(Mesa, JOIN.INNER, on=(Pedido.mesa_id == Mesa.id)).order_by(Pedido.id.asc())

#     listaPedido = []
#     for pedido in consulta:
#         pedido_data = {
#             "mesa" : pedido.pedido.mesa.numero,
#             "quantidade": pedido.quantidade,
#             "prato": pedido.produto.nome,
#             "pedido": pedido.pedido.id,
#             "idpedidoproduto" : pedido.id
  
#             # "status": pedido.pedidoproduto.status
#         }
#         listaPedido.append(pedido_data)
#     return listaPedido


# @main_bp.route('/marcarpedido', methods=['POST'])
# @login_required
# def marcarPedidoConcluido():
#     usuario = (current_user)
#     if usuario.role == "estabelecimento":
#         idEst = usuario.id
#     else:
#         idEst = usuario.estabelecimento_id

#     data = request.get_json()
#     # print('Data received:', data)  # Debugging line

#     # try:
#     idPedido = data['pedidoId']
#     idpedidoproduto = data['idpedidoproduto']
#     # except KeyError as e:
#     #     return jsonify({'message': f'Missing key: {str(e)}'}), 400

#     consulta = (PedidoProduto
#                 .select(PedidoProduto)
#                 .join(Pedido, on=(Pedido.id == PedidoProduto.pedido))
#                 .join(Produto, on=(PedidoProduto.produto == Produto.id))
#                 .where((PedidoProduto.pedido == idPedido) & (PedidoProduto.id == idpedidoproduto))
#                 .order_by(Pedido.id.asc())
#                 .first())

#     if consulta:
#         id_pedido_produto = consulta.id
#         produto = PedidoProduto.get(id=id_pedido_produto)
#         produto.status = "entregue"
#         produto.save()
#         return jsonify({'message': 'Pedido marcado com sucesso!'}), 200
#     else:
#         return jsonify({'message': 'Pedido não encontrado!'}), 400

    



    




# @main_bp.route('/abrirmesaespecifica', methods=['POST'])
# def abrirmesaespecifica():
#     data = request.get_json()
#     num = data['numero']
#     try: 
#         Mesa.create(numero = num, status = "ocupada")
#         return jsonify({'message': 'Mesa aberta com sucesso'}), 200
#     except IntegrityError as e:
#         mensagem = extrairErro(e)
#         return jsonify({'message': f"A inserção violou alguma chave: {mensagem}"}), 400

# @main_bp.route('/abrirmesa', methods=['POST'])
# def abrirmesa():
#     data = request.get_json()
#     num = data['numero']
#     try: 
#         mesa = Mesa.get(numero = num)
#         mesa.status = "ocupada"
#         mesa.save()
#         return jsonify({'message': 'Mesa aberta com sucesso'}), 200
#     except IntegrityError as e:
#         mensagem = extrairErro(e)
#         return jsonify({'message': f"A inserção violou alguma chave: {mensagem}"}), 400



# @main_bp.route('/fecharmesa', methods=['POST'])
# def fecharmesa():
#     data = request.get_json()
#     num = data['numero']
#     try: 
#         mesa = Mesa.get(numero = num)
#         mesa.status = "fechada"
#         mesa.save()
#         return jsonify({'message': 'Mesa fechada com sucesso'}), 200
#     except Mesa.DoesNotExist as e:
#         return jsonify({'message': f"Mesa nao encontrada"}), 400

# @main_bp.route('/calcularmesa', methods=['POST'])
# def calcularmesa():
#     data = request.get_json()
#     num = data['numero']
#     try: 
#         mesa = Mesa.get(numero = num)
#         if mesa.status == "aberta" or mesa.status == "livre":
#             return jsonify({'message': 'Mesa se encontra aberta, é necessario fechar para somar'}), 400
#         else:
#             total = calcularConta(mesa.id)
#             return jsonify({'message': f'total mesa = {total}'}), 200
#     except Mesa.DoesNotExist as e:
#         return jsonify({'message': f"Mesa nao encontrada"}), 400


# @main_bp.route('/mesas', methods=['GET'])
# @login_required
# def obterStatusMesas():
#     usuario = (current_user)
#     if usuario.role == "estabelecimento":
#         lista = obterListaMesas(usuario.id)
#         return lista 
#     else:
#         lista = obterListaMesas(usuario.estabelecimento_id)
#         return lista 

