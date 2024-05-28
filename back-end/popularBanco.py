from models import *
from werkzeug.security import generate_password_hash
from estabelecimento import *

def popularBanco():
    cnpj1 = "41.794.641/0001-42"
    cnpj2 = "11.111.111/1111-11"   

    Estabelecimento.create(nome = "Divino tempero", cnpj = cnpj1, senha = generate_password_hash("12345678"), email = "divino@gmail.com", cidade = "sao mamede", bairro = "centro", rua = "honorina", numero = "15"  )
    Estabelecimento.create(nome = "Mormaço", cnpj = cnpj2, senha = generate_password_hash("12345678"), email = "mormaço@gmail.com", cidade = "sao mamede", bairro = "centro", rua = "januncio", numero = "15"  )

    est1 = Estabelecimento.get(cnpj = cnpj1)
    criarMesas(cnpj1,14 )
    idest1 = est1.id
    est2 = Estabelecimento.get(cnpj = cnpj2)
    criarMesas(cnpj2,15)
    idest2 = est2.id

    garcom1 = Usuario.create(nome = "joaogarcom", usuario = "joaogarcom",senha = generate_password_hash("12345678"), tipo = "garcom", estabelecimento_id = idest1, role = "garcom" )
    gerente1 = Usuario.create(nome = "josegerente", usuario = "josegerente",senha = generate_password_hash("12345678"), tipo = "gerente", estabelecimento_id = idest1, role = "gerente" )
    caixa1 = Usuario.create(nome = "mariacaixa", usuario = "mariacaixa",senha = generate_password_hash("12345678"), tipo = "caixa", estabelecimento_id = idest1, role = "caixa" )
    cozinheira1 = Usuario.create(nome = "josefa ozinheira", usuario = "josefacozinheira",senha = generate_password_hash("12345678"), tipo = "cozinheiro", estabelecimento_id = idest1, role = "cozinheiro" )
    garcom2 = Usuario.create(nome = "jonasgarcom", usuario = "jonasgarcom",senha = generate_password_hash("12345678"), tipo = "garcom", estabelecimento_id = idest1, role = "garcom" )
    gerente2 = Usuario.create(nome = "vanessagerente", usuario = "vanessagerente",senha = generate_password_hash("12345678"), tipo = "gerente", estabelecimento_id = idest1, role = "gerente" )
    caixa2 = Usuario.create(nome = "manoelcaixa", usuario = "manoelcaixa",senha = generate_password_hash("12345678"), tipo = "caixa", estabelecimento_id = idest1, role = "caixa" )
    cozinheira2 = Usuario.create(nome = "andrecozinheira", usuario = "andre cozinheira",senha = generate_password_hash("12345678"), tipo = "cozinheiro", estabelecimento_id = idest1, role = "cozinheiro" )


    prod3 = Produto.create(nome = "Sopa de Lentilha com Bacon", valor = 12, categoria = "sopas", estabelecimento_id = idest1)
    prod4 = Produto.create(nome = "Caldo Verde com Linguiça", valor = 15, categoria = "sopas", estabelecimento_id = idest1)
    prod5 = Produto.create(nome = "Creme de Abóbora e Gengibre", valor = 13, categoria = "sopas", estabelecimento_id = idest1)
    prod6 = Produto.create(nome = "Sopa de Frango com Legumes", valor = 14, categoria = "sopas", estabelecimento_id = idest1)
    prod7 = Produto.create(nome = "Caldo de Feijão Preto", valor = 11, categoria = "sopas", estabelecimento_id = idest1)

    prod8 = Produto.create(nome = "Salada Caesar", valor = 18, categoria = "saladas", estabelecimento_id = idest1)
    prod9 = Produto.create(nome = "Salada Grega", valor = 17, categoria = "saladas", estabelecimento_id = idest1)
    prod10 = Produto.create(nome = "Salada de Frutas Tropicais", valor = 16, categoria = "saladas", estabelecimento_id = idest1)

    prod11 = Produto.create(nome = "Sanduíche de Frango", valor = 20, categoria = "sanduíches", estabelecimento_id = idest1)
    prod12 = Produto.create(nome = "Sanduíche Vegetariano", valor = 18, categoria = "sanduíches", estabelecimento_id = idest1)
    prod13 = Produto.create(nome = "Sanduíche de Atum", valor = 19, categoria = "sanduíches", estabelecimento_id = idest1)

    prod14 = Produto.create(nome = "Suco de Laranja Natural", valor = 7, categoria = "bebidas", estabelecimento_id = idest1)
    prod15 = Produto.create(nome = "Suco de Abacaxi com Hortelã", valor = 8, categoria = "bebidas", estabelecimento_id = idest1)
    prod16 = Produto.create(nome = "Smoothie de Morango e Banana", valor = 10, categoria = "bebidas", estabelecimento_id = idest1)


    prod17 = Produto.create(nome = "Sopa de Cebola Gratinada", valor = 16, categoria = "sopas", estabelecimento_id = idest2)
    prod18 = Produto.create(nome = "Creme de Espinafre com Queijo", valor = 15, categoria = "sopas", estabelecimento_id = idest2)
    prod19 = Produto.create(nome = "Caldo de Mocotó", valor = 14, categoria = "sopas", estabelecimento_id = idest2)
    prod20 = Produto.create(nome = "Sopa de Aspargos com Limão", valor = 17, categoria = "sopas", estabelecimento_id = idest2)
    prod21 = Produto.create(nome = "Sopa de Peixe com Coentro", valor = 18, categoria = "sopas", estabelecimento_id = idest2)

    prod22 = Produto.create(nome = "Salada de Quinoa com Legumes", valor = 19, categoria = "saladas", estabelecimento_id = idest2)
    prod23 = Produto.create(nome = "Salada Caprese", valor = 20, categoria = "saladas", estabelecimento_id = idest2)
    prod24 = Produto.create(nome = "Salada de Grão-de-Bico", valor = 18, categoria = "saladas", estabelecimento_id = idest2)

    prod25 = Produto.create(nome = "Sanduíche de Pastrami", valor = 22, categoria = "sanduíches", estabelecimento_id = idest2)
    prod26 = Produto.create(nome = "Sanduíche de Peru com Cranberry", valor = 21, categoria = "sanduíches", estabelecimento_id = idest2)
    prod27 = Produto.create(nome = "Sanduíche de Queijo Brie e Damasco", valor = 23, categoria = "sanduíches", estabelecimento_id = idest2)

    prod28 = Produto.create(nome = "Chá Gelado de Hibisco", valor = 9, categoria = "bebidas", estabelecimento_id = idest2)
    prod29 = Produto.create(nome = "Limonada Suíça", valor = 8, categoria = "bebidas", estabelecimento_id = idest2)
    prod30 = Produto.create(nome = "Milkshake de Baunilha", valor = 12, categoria = "bebidas", estabelecimento_id = idest2)



if __name__ == '__main__':
    popularBanco()
    print('Banco de dados populado com sucesso!')

