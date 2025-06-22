import datetime
from typing import List, Optional

from sqlalchemy import String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import flask_login
import pathlib
from flask import current_app

from . import db


class User(flask_login.UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    name: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String(256))
    mailing_list: Mapped[bool] = mapped_column(Boolean, default=False)
    photo_id: Mapped[Optional[int]] = mapped_column(ForeignKey("photo.id"))
    photo: Mapped[Optional["Photo"]] = relationship(back_populates="user")
    admin: Mapped[bool] = mapped_column(Boolean, default=False)

class Photo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="photo")
    file_extension: Mapped[str] = mapped_column(String(8))

class Event(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    location: Mapped[str] = mapped_column(String(256), nullable=False)
    start_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    organizer_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)