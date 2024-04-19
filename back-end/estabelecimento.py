from models import *



def obterListaFuncionarios(id):
    estabelecimento_idaux = id
    usuarios = Usuario.query.filter_by(estabelecimento_id=estabelecimento_idaux).order_by(Usuario.id.asc()).all()
    usuario_list = []
    for usuario in usuarios:
        if usuario.excluido != True:
            usuario_data = {
                'id': usuario.id,
                'nome': usuario.nome,
                'tipo': usuario.tipo
            }
            usuario_list.append(usuario_data)
    return {'usuarios': usuario_list}

def excluirFuncionario(id):
    usuario = Usuario.query.filter_by(id=id).one()
    if usuario:
        if usuario.excluido != True:
            usuario.excluido = True
            bd.session.commit()
            return True
        else:
            return False
    else:
        return False