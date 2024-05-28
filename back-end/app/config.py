

class Config:
    SECRET_KEY = 'CHAVESECRETA'
    # Other configurations such as database URI, CORS, etc.

def init_config(app):
    app.config.from_object(Config)