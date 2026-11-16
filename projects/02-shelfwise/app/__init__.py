from flask import Flask
from flask_login import current_user
from config import Config
from .extensions import csrf, db, login_manager

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    from . import models
    from .auth import auth_bp
    from .shop import shop_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    @app.cli.command("create-admin")
    def create_admin():
        import click
        from .models import User
        username = click.prompt("Admin username")
        if User.query.filter_by(username=username).first():
            raise click.ClickException("That username already exists.")
        password = click.prompt("Admin password", hide_input=True, confirmation_prompt=True)
        if len(password) < 12:
            raise click.ClickException("Use a password with at least 12 characters.")
        user = User(username=username, role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo("Administrator account created.")
    @app.context_processor
    def inject_current_user():
        return {"current_user": current_user}
    with app.app_context():
        db.create_all()
    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return db.session.get(User, int(user_id))
