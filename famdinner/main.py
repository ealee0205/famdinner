import datetime
import dateutil.tz
from datetime import datetime, timedelta
import pathlib

import flask_login

from . import db
from . import model

from flask import Blueprint, abort, render_template, request, redirect, url_for, flash, jsonify, current_app


bp = Blueprint("main", __name__)

@bp.route("/")
@flask_login.login_required
def home():
    current_time = datetime.now(dateutil.tz.tzlocal())
    # ongoing_events = model.Event.query.filter(
    #     model.Event.start_date <= current_time,
    #     model.Event.end_date >= current_time
    # ).all()
    ongoing_events = model.Event.query.all()
    return render_template("main/index.html", ongoing_events=ongoing_events)

@bp.route("/profile")
@flask_login.login_required
def profile():
    user = flask_login.current_user
    if not user:
        abort(404)
    return render_template("main/profile-page.html", user=user)

@bp.route("/saveprofile", methods=["post"])
def save_profile():
    user = flask_login.current_user
    user.name = request.form.get("name")
    user.gender = request.form.get("gender")
    user.gender_preference = request.form.get("genderPref")
    user.age = request.form.get("age")
    user.min_age_preference = request.form.get("ageprefmin")
    user.max_age_preference = request.form.get("ageprefmax")
    user.description = request.form.get("description")
    user.mailing_list = request.form.get("mailing_list") == 'on'  # Assuming a checkbox for mailing list
    db.session.commit()
    flash("Profile updated", "success")

    uploaded_file = request.files.get('photo')
    if uploaded_file and uploaded_file.filename != '':
        content_type = uploaded_file.content_type
        if content_type == "image/png":
            file_extension = "png"
        elif content_type == "image/jpeg":
            file_extension = "jpg"
        else:
            abort(400, f"Unsupported file type {content_type}")
        
        photo = model.Photo(
            file_extension=file_extension
        )
        db.session.add(photo)
        
        old_photo = user.photo
        if old_photo is not None:
            path = photo_filename(old_photo)
            path.unlink()
            db.session.delete(old_photo)

        user.photo = photo
        path = photo_filename(photo)
        uploaded_file.save(path)
        db.session.commit()

    return redirect(url_for(
        "main.profile",
        user=user
    ))

def photo_filename(photo):
    path = (
        pathlib.Path(current_app.root_path)
        / "static"
        / "images"
        / f"photo-{photo.id}.{photo.file_extension}"
    )
    return path

@bp.route("/create_event")
@flask_login.login_required
def create_event():
    user = flask_login.current_user
    return render_template("main/create_event.html")

@bp.route("/create_event", methods=["POST"])
def create_event_post():
    user = flask_login.current_user
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
    
    return render_template("main/create_event.html")

@bp.route("/events")
@flask_login.login_required
def events():
    user = flask_login.current_user
    events = model.Event.query.filter(
        model.Event.organizer_id != user.id,
        model.Event.end_date > datetime.now(dateutil.tz.tzlocal())
    ).all()
    return render_template("eventview/eventview.html", events=events)