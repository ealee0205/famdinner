from flask import Flask

import click
from flask.cli import with_appcontext

# Things to import at the beginning
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.security import generate_password_hash



# Declarations to insert before the create_app function:
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

def create_app(test_config=None):
    app = Flask(__name__)

    # A secret for signing session cookies
    app.config["SECRET_KEY"] = "93220d9b340cf9a6c39bac99cce7daf220167498f91fa"
    # Code to place inside create_app, after the other app.config assignment
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:///famdinner.db"

    db.init_app(app)

    # Activate flask's builtin login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from . import model

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(model.User, int(user_id))

    # Register blueprints
    # (we import main from here to avoid circular imports in the next lab)
    from . import main
    from . import auth
    from . import admin

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    return app

@click.command()
@with_appcontext
def create_admin():
    password = "admin"
    password_hash = generate_password_hash(password)
    
    from . import model

    admin_user = model.User(
        email="ealee0205@gmail.com",
        name="Ethan",
        password=password_hash,
        mailing_list=True,
        admin=True
        )
    db.session.add(admin_user)
    db.session.commit()