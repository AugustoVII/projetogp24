from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from .models import *
from .utils import *
from .estabelecimento import *
from werkzeug.security import generate_password_hash, check_password_hash

def create_app():
    app = Flask("__main__")
    app.config['SECRET_KEY'] = 'CHAVESECRETA'
    
    # Inicializar banco de dados
    database.connect()
    create_tables()
    CORS(app)
    print("Conexão com o banco de dados estabelecida.")

    # Configurações do Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id is not None:
            try:
                usuario = Usuario.get(Usuario.id == user_id)
                return usuario
            except Usuario.DoesNotExist:
                try:
                    estabelecimento = Estabelecimento.get(Estabelecimento.id == user_id)
                    return estabelecimento
                except Estabelecimento.DoesNotExist:
                    return None

    # Importar e registrar blueprints
    from .auth import auth_bp
    from .main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app

