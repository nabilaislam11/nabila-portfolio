from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    from app.models import User, DetectionRecord
    from app.auth import auth_bp
    from app.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    with app.app_context():
        db.create_all()
    return app
