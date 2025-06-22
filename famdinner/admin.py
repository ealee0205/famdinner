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

@bp.route("/create_event")
@flask_login.login_required
def create_event():
    user = flask_login.current_user
    if not user.admin:
        flash("You do not have permission to create events.", "error")
        return redirect(url_for("main.home"))
    return render_template("admin/create_event.html")

@bp.route("/create_event", methods=["POST"])
def create_event_post():
    user = flask_login.current_user
    if not user.admin:
        flash("You do not have permission to create events.", "error")
        return redirect(url_for("main.home"))
    title = request.form.get("title")
    location = request.form.get("location")
    start_date_str = request.form.get("start-date")
    start_time_str = request.form.get("start-time")

    # Parse the start date and time
    combined_start_str = f"{start_date_str} {start_time_str}"
    try:
        start_datetime = datetime.strptime(combined_start_str, "%B %d, %Y %I:%M %p")
    except ValueError:
        flash(f"Invalid start date or time format. {combined_start_str}", "error")
        return redirect(url_for("admin.create_event"))

    end_date_str = request.form.get("end-date")
    end_date_time_str = request.form.get("end-time")

    # Parse the end date and time
    combined_end_str = f"{end_date_str} {end_date_time_str}"
    try:
        end_datetime = datetime.strptime(combined_end_str, "%B %d, %Y %I:%M %p")
    except ValueError:
        flash("Invalid end date or time format.", "error")
        return redirect(url_for("admin.create_event"))
    
    new_event = model.Event(
        title=title,
        location=location,
        start_date=start_datetime,
        end_date=end_datetime,
        organizer_id=user.id
    )
    db.session.add(new_event)
    db.session.commit()
    flash("Event created successfully!", "success")
    
    return render_template("admin/create_event.html")