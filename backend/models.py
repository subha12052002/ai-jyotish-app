from datetime import datetime

from database import db


# =========================================================
# USER
# =========================================================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    profiles = db.relationship(

        "BirthProfile",

        backref="user",

        lazy=True,

        cascade="all, delete-orphan"
    )


    charts = db.relationship(

        "SavedChart",

        backref="user",

        lazy=True,

        cascade="all, delete-orphan"
    )


    def to_dict(self):

        return {

            "id": self.id,

            "name": self.name,

            "email": self.email,

            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )

        }


# =========================================================
# BIRTH PROFILE
# =========================================================

class BirthProfile(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(

        db.Integer,

        db.ForeignKey(
            "user.id"
        ),

        nullable=False
    )


    name = db.Column(
        db.String(120),
        nullable=False
    )


    birth_date = db.Column(
        db.String(20),
        nullable=False
    )


    birth_time = db.Column(
        db.String(20),
        nullable=False
    )


    place = db.Column(
        db.String(180),
        nullable=False
    )


    latitude = db.Column(
        db.Float,
        nullable=False
    )


    longitude = db.Column(
        db.Float,
        nullable=False
    )


    timezone = db.Column(
        db.Float,
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================================================
# SAVED CHART
# =========================================================

class SavedChart(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    user_id = db.Column(

        db.Integer,

        db.ForeignKey(
            "user.id"
        ),

        nullable=False
    )


    birth_profile_id = db.Column(

        db.Integer,

        db.ForeignKey(
            "birth_profile.id"
        ),

        nullable=False
    )


    chart_json = db.Column(
        db.Text,
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )