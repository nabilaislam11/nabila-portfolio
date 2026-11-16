from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.models import User
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    from app.students import bp as students_bp
    from app.academics import bp as academics_bp
    from app.finance import bp as finance_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(academics_bp, url_prefix="/academics")
    app.register_blueprint(finance_bp, url_prefix="/finance")

    @app.cli.command("init-db")
    def init_db():
        """Create database tables."""
        db.create_all()
        print("Database tables created.")

    @app.cli.command("create-admin")
    def create_admin():
        """Create the first administrator interactively."""
        import getpass
        username = input("Username: ").strip()
        email = input("Email: ").strip().lower()
        password = getpass.getpass("Password (minimum 12 characters): ")
        if len(password) < 12:
            raise SystemExit("Password must contain at least 12 characters.")
        if User.query.filter((User.username == username) | (User.email == email)).first():
            raise SystemExit("Username or email already exists.")
        user = User(username=username, email=email, role="admin", is_active=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print("Administrator created.")

    with app.app_context():
        db.create_all()

    return app
