from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid

db = SQLAlchemy()


class Role:
    ESTABELECIMENTO = 'estabelecimento'
    GERENTE = 'gerente'
    GARCOM = 'garcom'
    CAIXA = 'caixa'


class Usuario(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    excluido = db.Column(db.Boolean, default=False)
    estabelecimento_id = db.Column(db.String(36), db.ForeignKey('estabelecimento.id'))
    estabelecimento = db.relationship('Estabelecimento', backref=db.backref('usuarios', lazy=True)) 
    role = db.Column(db.String(50), nullable=False, default=Role.GARCOM)
    
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

class Estabelecimento(db.Model , UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    cidade = db.Column(db.String(256), nullable=False)
    bairro = db.Column(db.String(256), nullable=False)
    rua = db.Column(db.String(256), nullable=False)
    numero = db.Column(db.String(15), nullable=False)
    excluido = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), nullable=False, default=Role.ESTABELECIMENTO)

    def is_estabelecimento(self):
        return self.role == Role.ESTABELECIMENTO
    
    
    def __repr__(self):
        return f"Estabelecimento: {self}"
    
    def __init__(self, nome, cnpj, senha, cidade, bairro, rua, numero, email):
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