from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid
from decimal import Decimal

bd = SQLAlchemy()


class Role:
    ESTABELECIMENTO = 'estabelecimento'
    GERENTE = 'gerente'
    GARCOM = 'garcom'
    CAIXA = 'caixa'


class Usuario(bd.Model, UserMixin):
    id = bd.Column(bd.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = bd.Column(bd.String(100), nullable=False)
    usuario = bd.Column(bd.String(100), unique=True, nullable=False)
    senha = bd.Column(bd.String(256), nullable=False)
    tipo = bd.Column(bd.String(50), nullable=False)
    excluido = bd.Column(bd.Boolean, default=False)
    estabelecimento_id = bd.Column(bd.String(36), bd.ForeignKey('estabelecimento.id'))
    estabelecimento = bd.relationship('Estabelecimento', backref=bd.backref('usuarios', lazy=True)) 
    role = bd.Column(bd.String(50), nullable=False, default=Role.GARCOM)
    
    def __repr__(self):
        return f"Usuario: {self}"
    
    def __init__(self, nome, usuario, senha, tipo, estabelecimento_id):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.usuario = usuario
        self.senha = senha
        self.tipo = tipo
        self.estabelecimento_id = estabelecimento_id
        self.role = tipo

    def is_gerente(self):
        return self.role == Role.GERENTE

    def is_caixa(self):
        return self.role == Role.CAIXA

    def is_garcom(self):
        return self.role == Role.GARCOM
    
    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False

    

def format_usuario(usuario):
    return {
        "nome": usuario.nome,
        "usuario": usuario.usuario,
        "tipo": usuario.tipo,
        "senha": usuario.senha
    }

class Estabelecimento(bd.Model , UserMixin):
    id = bd.Column(bd.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = bd.Column(bd.String(100), nullable=False)
    cnpj = bd.Column(bd.String(18), unique=True, nullable=False)
    senha = bd.Column(bd.String(256), nullable=False)
    email = bd.Column(bd.String(256), nullable=False)
    cidade = bd.Column(bd.String(256), nullable=False)
    bairro = bd.Column(bd.String(256), nullable=False)
    rua = bd.Column(bd.String(256), nullable=False)
    numero = bd.Column(bd.String(15), nullable=False)
    excluido = bd.Column(bd.Boolean, default=False)
    role = bd.Column(bd.String(50), nullable=False, default=Role.ESTABELECIMENTO)

    def is_estabelecimento(self):
        return self.role == Role.ESTABELECIMENTO
    
    
    def __repr__(self):
        return f"Estabelecimento: {self}"
    
    def __init__(self, nome, cnpj, senha, cidade, bairro, rua, numero, email):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.cnpj = cnpj
        self.senha = senha
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        self.email = email

    def is_active(self):
        return True
    
    def get_id(self):
        return str(self.id)
     
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False


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


class Categoria(bd.Model):
    id = bd.Column(bd.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = bd.Column(bd.String(100), nullable=False, unique=True)

    def __init__(self, nome):
        self.id = str(uuid.uuid4())
        self.nome = nome

    def __repr__(self):
        return f"Categoria: {self.nome}"

    

class Produto(bd.Model):
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(100), nullable=False,unique=True)
    valor = bd.Column(bd.Numeric(precision=10, scale=2), nullable=False)
    categoria_id = bd.Column(bd.String(36), bd.ForeignKey('categoria.id'))
    categoria = bd.relationship('Categoria', backref=bd.backref('produto', lazy=True)) 

    def __init__(self, nome, categoriaid, valor):
        self.nome = nome
        self.categoria_id = categoriaid
        self.valor = valor
    
    def __repr__(self):
        return f"Produto : {self.nome}"
    

def str_to_numeric(value_str):
    try:
        # Tenta converter a string para Decimal (Numeric)
        return Decimal(value_str)
    except ValueError:
        # Trate a exceção se a conversão falhar (por exemplo, string inválida)
        return None


class Mesa(bd.Model):
    id = bd.Column(bd.Integer, primary_key=True)
    numero = bd.Column(bd.Integer, unique=True, nullable=False)
    status = bd.Column(bd.String, default='LIVRE', nullable=False)
    pedidos = bd.relationship("Pedido", secondary= 'mesa_pedido_association', back_populates="mesa")

    def __repr__(self):
        return f"<Mesa(id={self.id}, numero={self.numero}, status='{self.status}')>"
    
    def __init__(self, numero):
        self.status = 'LIVRE'
        self.numero = numero
        self.pedidos = []  # Inicializa a lista de pedidos como vazia

    def adicionar_pedido(self, pedido):
        self.pedidos.append(pedido)

    def fechar_mesa(self):
        self.status = 'fechada'
    



class Pedido(bd.Model):
    id = id = bd.Column(bd.Integer, primary_key=True)
    numero = bd.Column(bd.Integer, nullable=False)
    mesa_id = bd.Column(bd.Integer, bd.ForeignKey('mesa.id')) 
    mesa = bd.relationship("Mesa", back_populates="pedidos")
    produtos = bd.relationship("Produto", secondary='pedido_produto_association', backref="pedidos")
    status = bd.Column(bd.String, default='PREPARANDO', nullable=False)
    
    def __init__(self, numero, status, mesaid):
        self.status = status
        self.numero = numero
        self.produtos = []
        self.mesa_id = mesaid

    def adicionar_produto(self, produto):
        self.produtos.append(produto)


    def __repr__(self):
        return f"<Pedido(id={self.id}, numero={self.numero}, status={self.status})>"

pedido_produto_association = bd.Table(
    'pedido_produto_association',
    bd.metadata,
    bd.Column('pedido_id', bd.Integer, bd.ForeignKey('pedido.id')),
    bd.Column('produto_id', bd.Integer, bd.ForeignKey('produto.id'))
)

mesa_pedido_association = bd.Table(
    'mesa_pedido_association',
    bd.metadata,
    bd.Column('mesa_id', bd.Integer, bd.ForeignKey('mesa.id')),
    bd.Column('pedido_id', bd.Integer, bd.ForeignKey('pedido.id'))
)