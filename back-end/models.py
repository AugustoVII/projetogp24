from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(256), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    excluido = db.Column(db.Boolean, default=False)
    
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