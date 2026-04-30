from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # import routes here to avoid circular imports
        from app.routes import public, auth, admin, citizen

        app.register_blueprint(public.bp)
        app.register_blueprint(auth.bp)
        app.register_blueprint(admin.bp)
        app.register_blueprint(citizen.bp)

        try:
            db.create_all()
        except Exception as e:
            print(f"Erro ao inicializar db: {e}")
    return app
