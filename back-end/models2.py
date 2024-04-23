from peewee import *

# Configurando a conexão com o banco de dados PostgreSQL
db = PostgresqlDatabase('projetogp2', user='postgres', password='postgres', host='localhost', port=5432)

# Definindo as classes de modelo usando Peewee
class BaseModel(Model):
    class Meta:
        database = db

# Classe para Categoria
class Categoria(BaseModel):
    nome = CharField(unique=True)  # Nome da categoria

# Classe para Produto
class Produto(BaseModel):
    nome = CharField()
    valor = DecimalField(max_digits=10, decimal_places=2)
    categoria = ForeignKeyField(Categoria, backref='produtos')  # Relacionamento com Categoria

# Classe para Mesa
class Mesa(BaseModel):
    numero = IntegerField(unique=True)
    status = CharField(choices=['livre', 'ocupada', 'fechada'])
    
# Classe para Pedido
class Pedido(BaseModel):
    mesa = ForeignKeyField(Mesa, backref='pedidos')  # Relacionamento com Mesa
    status = CharField(choices=['preparando', 'entregue'])

# Classe para os produtos em um Pedido (Muitos-para-Muitos)
class PedidoProduto(BaseModel):
    pedido = ForeignKeyField(Pedido, backref='itens_pedido')
    produto = ForeignKeyField(Produto)
    quantidade = IntegerField(default=1)

# Inicializando o banco de dados
def create_tables():
    with db:
        db.create_tables([Categoria, Produto, Mesa, Pedido, PedidoProduto])

# Exemplo de uso:
# if __name__ == '__main__':
#     # Criar as tabelas no banco de dados (executar apenas uma vez)
#     create_tables()