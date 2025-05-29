from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from app.config import Config

# Instância global do SQLAlchemy
db = SQLAlchemy()

# Instância global do LoginManager
login_manager = LoginManager()

# Instância global do CSRFProtect
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensões com a app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Registrar blueprints
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')

    from app.routes.painel import painel_bp
    app.register_blueprint(painel_bp, url_prefix='/')

    from app.routes.cliente import cliente_bp
    app.register_blueprint(cliente_bp, url_prefix='/')

    from app.routes.documentos import documentos_bp
    app.register_blueprint(documentos_bp, url_prefix='/')

    from app.routes.usuario import usuario_bp
    app.register_blueprint(usuario_bp, url_prefix='/usuarios')

    from app.routes.especialidade import especialidade_bp
    app.register_blueprint(especialidade_bp, url_prefix='/especialidades')

    from app.routes.csrf_teste import csrf_teste_bp
    app.register_blueprint(csrf_teste_bp)

    return app