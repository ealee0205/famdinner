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
    return render_template("main/index.html")

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