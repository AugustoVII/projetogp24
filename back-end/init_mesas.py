from main import *
from models import *

def criar_mesas():
    with app.app_context():
        # Popula o banco de dados com 100 mesas inicialmente abertas
        for i in range(1, 101):
            Mesa.create(numero = i+1, status = "livre")



if __name__ == '__main__':
    criar_mesas()
    print('Mesas criadas com sucesso!')