from models import *



def obterListaFuncionarios(id):
    estabelecimento_idaux = id
    
    # Consulta utilizando Peewee para obter usuários pelo estabelecimento_id
    usuarios = Usuario.select().where(
        (Usuario.estabelecimento_id == estabelecimento_idaux) &
        (Usuario.excluido != True)  # Considerando excluido como um campo booleano
    ).order_by(Usuario.id.asc())  # Ordenar por ID ascendente
    
    # Construir a lista de usuários a ser retornada
    usuario_list = []
    for usuario in usuarios:
        usuario_data = {
            'id': usuario.id,
            'nome': usuario.nome,
            'tipo': usuario.tipo
        }
        usuario_list.append(usuario_data)
    
    return {'usuarios': usuario_list}


def excluirFuncionario(id):
    try:
        # Tenta obter o usuário pelo ID
        usuario = Usuario.get_by_id(id)
        
        # Verifica se o usuário foi encontrado
        if usuario:
            # Verifica se o usuário não está excluído
            if not usuario.excluido:
                # Marca o usuário como excluído
                usuario.excluido = True
                usuario.save()  # Salva as alterações no banco de dados
                return True  # Indica que o usuário foi excluído com sucesso
            else:
                return False  # O usuário já está excluído
        else:
            return False  # Usuário não encontrado
    except Usuario.DoesNotExist:
        return False  # Usuário não encontrado

def criarMesas(cnpj):
    try: 
        x = Estabelecimento.get(cnpj=cnpj)
        for i in range(1,101):
            Mesa.create(numero = i, status = "livre", estabelecimento_id = x.id)
    except Estabelecimento.DoesNotExist :
        return 'estabelecimento não encontrado' 
    
def obterListaMesas(idEstabelecimento):
    try:
        mesas = Mesa.select().where(Mesa.estabelecimento_id == idEstabelecimento).order_by(Mesa.numero.asc())
        lista_mesas = []
        for mesa in mesas:
            mesa_data = {
                'id' : mesa.id,
                'numero' : mesa.numero,
                'status' : mesa.status
            }
            lista_mesas.append(mesa_data)
        return {'mesas': lista_mesas}
    except :
        return 'estabelecimento não encontrado'

def obterListaProdutos(idEstab):
    try:
        produtos = Produto.select().where(Produto.estabelecimento_id == idEstab).order_by(Produto.nome.asc())
        listaProdutos = []
        for produto in produtos:
            produto_data = {
                    'id' : produto.id,
                    'nome' : produto.nome,
                    'valor': produto.valor,
                    'categoria' : produto.categoria
                    }
            listaProdutos.append(produto_data)
        return {'produtos': listaProdutos}
    except:
        return "ocorreu algum erro ao processar"

    
        





def atualizarFuncionario(id, nome, username,senha, tipo):
    try:
        # Tenta obter o usuário pelo ID
        usuario = Usuario.get_by_id(id)
        
        # Verifica se o usuário foi encontrado
        if usuario:
            usuario.nome = nome
            usuario.usuario = username
            usuario.senha = senha
            usuario.tipo = tipo
            usuario.role = tipo
            usuario.save()
            return True  # Indica que o usuário foi alterado com sucesso
           
        else:
            return False  # Usuário não encontrado
    except Usuario.DoesNotExist:
        return False  # Usuário não encontrado