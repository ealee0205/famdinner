from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash

# Things to import at the beginning
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

import flask_login

from . import db
from . import model

from datetime import datetime

bp = Blueprint("admin", __name__)


# Declarations to insert before the create_app function:
class Base(DeclarativeBase):
  pass


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
