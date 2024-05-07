from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid
from decimal import Decimal
from peewee import *
import re



DATABASE = {
    'name': 'projetogp3',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',  # ou o endereço do seu servidor PostgreSQL
    'port': 5432,          # a porta padrão do PostgreSQL é 5432
}

database = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)


class BaseModel(Model):
    class Meta:
        database = database

class Role:
    ESTABELECIMENTO = 'estabelecimento'
    GERENTE = 'gerente'
    GARCOM = 'garcom'
    CAIXA = 'caixa'
    COZINHA = 'cozinha'

class Estabelecimento(BaseModel, UserMixin):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    nome = CharField(max_length=100)
    cnpj = CharField(max_length=18, unique=True)
    senha = CharField(max_length=256)
    email = CharField(max_length=256)
    cidade = CharField(max_length=256)
    bairro = CharField(max_length=256)
    rua = CharField(max_length=256)
    numero = CharField(max_length=15)
    excluido = BooleanField(default=False)
    role = CharField(max_length=50, default=Role.ESTABELECIMENTO)

    def is_estabelecimento(self):
        return self.role == Role.ESTABELECIMENTO

    def __repr__(self):
        return f"Estabelecimento: {self}"


class Usuario(BaseModel, UserMixin):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    nome = CharField(max_length=100)
    usuario = CharField(max_length=100, unique=True)
    senha = CharField(max_length=256)
    tipo = CharField(max_length=50)
    excluido = BooleanField(default=False)
    estabelecimento_id = ForeignKeyField(Estabelecimento, backref='usuarios')
    role = CharField(max_length=50, default=Role.GARCOM)

    def is_gerente(self):
        return self.role == Role.GERENTE

    def is_caixa(self):
        return self.role == Role.CAIXA

    def is_garcom(self):
        return self.role == Role.GARCOM
    
    def is_cozinha(self):
        return self.role == Role.COZINHA

    def __repr__(self):
        return f"Usuario: {self}"
    
    def getNome(self):
        return self.nome

# Inicialize o banco de dados e crie tabelas
def create_tables():
    with database:
        database.create_tables([Estabelecimento, Usuario, Produto, Mesa, Pedido, PedidoProduto])

# Funções de formatação
def format_usuario(usuario):
    return {
        "nome": usuario.nome,
        "usuario": usuario.usuario,
        "tipo": usuario.tipo,
        "senha": usuario.senha
    }

def format_estabelecimento(estabelecimento):
    return {
        "nome": estabelecimento.nome,
        "cnpj": estabelecimento.cnpj,
        "cidade": estabelecimento.cidade,
        "bairro": estabelecimento.bairro
    }

def formatar_cnpj(cnpj):
    cnpj_formatado = "{}.{}.{}/{}-{}".format(
        cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:]
    )
    return cnpj_formatado


 

# Classe para Produto
class Produto(BaseModel):
    nome = CharField(unique = True)
    valor = DecimalField(max_digits=10, decimal_places=2)
    categoria = CharField(max_length=50)
    estabelecimento_id = ForeignKeyField(Estabelecimento, backref='produtos')  # Relacionamento com Categoria

# Classe para Mesa
class Mesa(BaseModel):
    numero = IntegerField()
    status = CharField(choices=['livre', 'ocupada', 'fechada'])
    estabelecimento_id = ForeignKeyField(Estabelecimento, backref='mesas')

    def listar_pedidos(self):
        # Retornar todos os pedidos associados a esta mesa
        return self.pedidos
    
# Classe para Pedido
class Pedido(BaseModel):
    mesa = ForeignKeyField(Mesa, backref='pedidos')  # Relacionamento com Mesa
    status = CharField(choices=['preparando', 'entregue', "pago"])
    estabelecimento_id = ForeignKeyField(Estabelecimento, backref='pedidos')


    def adicionar_produto(self, produto, quantidade):
        # Criar uma nova entrada na tabela PedidoProduto
        PedidoProduto.create(pedido=self, produto=produto, quantidade=quantidade)

    def remover_produto(self, produto):
        try:
            # Encontrar a entrada na tabela PedidoProduto que corresponde ao produto a ser removido
            pedido_produto = PedidoProduto.get(pedido=self, produto=produto)
            pedido_produto.delete_instance()  # Deletar a entrada associada
            return True  # Produto removido com sucesso
        except PedidoProduto.DoesNotExist:
            return False  # Produto não encontrado no pedido
        
    def listar_produtos(self):
        # Retornar todos os produtos associados a este pedido
        return [item.produto for item in self.itens_pedido]
    
def proximo_numero_pedido():
    query = Pedido.select(fn.MAX(Pedido.id))
    maior_id = query.scalar() or 0
    return maior_id + 1

# Classe para os produtos em um Pedido (Muitos-para-Muitos)
class PedidoProduto(BaseModel):
    pedido = ForeignKeyField(Pedido, backref='itens_pedido')
    produto = ForeignKeyField(Produto)
    quantidade = IntegerField(default=1)



def str_to_numeric(value_str):
    try:
        # Tenta converter a string para Decimal (Numeric)
        return Decimal(value_str)
    except ValueError:
        # Trate a exceção se a conversão falhar (por exemplo, string inválida)
        return None


def extrairErro(mensagem):
    mensagem_erro = str(mensagem)
    match = re.search(r'Chave \(nome\)=\((.*?)\)', mensagem_erro)
    if match:
        valorExtraido = match.group(1)
        return (f"chave violada: {valorExtraido}")
    else:
        return("nao foi possivel identificar o erro!")

def calcularConta(idmesa):
    consulta = (PedidoProduto.select(PedidoProduto.produto , PedidoProduto.quantidade, Produto.valor)
                    .join(Pedido)
                    .join(Produto, on=(PedidoProduto.produto == Produto.id))
                    .where(Pedido.mesa == idmesa and Pedido.status != "pago"))
    total = 0
    if consulta:
        for item in consulta:
            nome_produto = item.produto.nome
            quantidade = item.quantidade
            valor_produto = item.produto.valor
            total_item = quantidade * valor_produto
            total = total + total_item
        return (f"total = {total} ")
    else: 
        print("nao foi encontrado pedidos")