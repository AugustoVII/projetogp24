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