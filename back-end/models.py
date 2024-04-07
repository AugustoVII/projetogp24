from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    excluido = db.Column(db.Boolean, default=False)
    estabelecimento_id = db.Column(db.Integer, db.ForeignKey('estabelecimento.id'))
    estabelecimento = db.relationship('Estabelecimento', backref=db.backref('usuarios', lazy=True))
    
    def __repr__(self):
        return f"Usuario: {self}"
    
    def __init__(self, nome, usuario, senha, tipo):
        self.nome = nome
        self.usuario = usuario
        self.senha = senha
        self.tipo = tipo

def format_usuario(usuario):
    return {
        "nome": usuario.nome,
        "usuario": usuario.usuario,
        "tipo": usuario.tipo,
        "senha": usuario.senha
    }

class Estabelecimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    cidade = db.Column(db.String(256), nullable=False)
    bairro = db.Column(db.String(256), nullable=False)
    rua = db.Column(db.String(256), nullable=False)
    numero = db.Column(db.String(15), nullable=False)
    excluido = db.Column(db.Boolean, default=False)
    
    
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