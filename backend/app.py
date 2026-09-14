# =========================================================
# AI JYOTISH - FLASK BACKEND
# app.py
# =========================================================

import os
import json
import traceback

from datetime import datetime
from functools import wraps

from dotenv import load_dotenv

from flask import (
    Flask,
    jsonify,
    request,
    send_from_directory,
    session
)

from flask_cors import CORS

from database import db

from models import (
    User,
    BirthProfile,
    SavedChart
)

from auth import (
    hash_password,
    verify_password
)

from kundli import (
    generate_kundli
)

from analysis_engine import (
    attach_complete_analysis
)

from ai_astrologer import (
    answer_question
)


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# PATHS
# =========================================================

BACKEND_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BASE_DIR = os.path.dirname(
    BACKEND_DIR
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)

INSTANCE_DIR = os.path.join(
    BACKEND_DIR,
    "instance"
)


os.makedirs(
    INSTANCE_DIR,
    exist_ok=True
)


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)


# =========================================================
# SECRET KEY
# =========================================================

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key"
)


# =========================================================
# DATABASE
# =========================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


if DATABASE_URL:

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = DATABASE_URL

else:

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = (
        "sqlite:///"
        + os.path.join(
            INSTANCE_DIR,
            "ai_jyotish.db"
        )
    )


app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False


# =========================================================
# SESSION SETTINGS
# =========================================================

app.config[
    "SESSION_COOKIE_HTTPONLY"
] = True

app.config[
    "SESSION_COOKIE_SAMESITE"
] = "Lax"

# Local development.
# Change to True when using HTTPS in production.

app.config[
    "SESSION_COOKIE_SECURE"
] = False


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

db.init_app(
    app
)


# =========================================================
# CORS
# =========================================================

CORS(
    app,
    supports_credentials=True
)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

with app.app_context():

    db.create_all()


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required(function):

    @wraps(function)
    def wrapper(
        *args,
        **kwargs
    ):

        if not session.get(
            "user_id"
        ):

            return jsonify({

                "error":
                    "Authentication required"

            }), 401


        return function(
            *args,
            **kwargs
        )


    return wrapper


# =========================================================
# FRONTEND - HOME
# =========================================================

@app.get("/")
def index():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# =========================================================
# FRONTEND - ALL FILES
# =========================================================

@app.get("/<path:filename>")
def frontend_file(
    filename
):

    full_path = os.path.join(
        FRONTEND_DIR,
        filename
    )


    if os.path.isfile(
        full_path
    ):

        return send_from_directory(
            FRONTEND_DIR,
            filename
        )


    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.post("/api/register")
def register():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


    name = str(
        data.get(
            "name",
            ""
        )
    ).strip()


    email = str(
        data.get(
            "email",
            ""
        )
    ).strip().lower()


    password = data.get(
        "password",
        ""
    )


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if (
        not name
        or not email
        or not isinstance(
            password,
            str
        )
        or len(password) < 6
    ):

        return jsonify({

            "error":
                (
                    "Name, valid email and "
                    "password of at least "
                    "6 characters are required."
                )

        }), 400


    # -----------------------------------------------------
    # CHECK EXISTING USER
    # -----------------------------------------------------

    existing_user = (

        User.query

        .filter_by(
            email=email
        )

        .first()

    )


    if existing_user:

        return jsonify({

            "error":
                (
                    "An account with this "
                    "email already exists."
                )

        }), 409


    # -----------------------------------------------------
    # CREATE USER
    # -----------------------------------------------------

    user = User(

        name=name,

        email=email,

        password_hash=
            hash_password(
                password
            )

    )


    db.session.add(
        user
    )

    db.session.commit()


    # -----------------------------------------------------
    # LOGIN SESSION
    # -----------------------------------------------------

    session[
        "user_id"
    ] = user.id

    session[
        "user_name"
    ] = user.name


    return jsonify({

        "message":
            "Registration successful",

        "user":
            user.to_dict()

    }), 201


# =========================================================
# LOGIN
# =========================================================

@app.post("/api/login")
def login():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


    email = str(
        data.get(
            "email",
            ""
        )
    ).strip().lower()


    password = data.get(
        "password",
        ""
    )


    # -----------------------------------------------------
    # FIND USER
    # -----------------------------------------------------

    user = (

        User.query

        .filter_by(
            email=email
        )

        .first()

    )


    # -----------------------------------------------------
    # VERIFY PASSWORD
    # -----------------------------------------------------

    if (
        not user
        or not verify_password(
            password,
            user.password_hash
        )
    ):

        return jsonify({

            "error":
                "Invalid email or password."

        }), 401


    # -----------------------------------------------------
    # SESSION
    # -----------------------------------------------------

    session[
        "user_id"
    ] = user.id

    session[
        "user_name"
    ] = user.name


    return jsonify({

        "message":
            "Login successful",

        "user":
            user.to_dict()

    })


# =========================================================
# LOGOUT
# =========================================================

@app.post("/api/logout")
def logout():

    session.clear()


    return jsonify({

        "message":
            "Logged out"

    })


# =========================================================
# CURRENT USER
# =========================================================

@app.get("/api/me")
@login_required
def me():

    user = db.session.get(
        User,
        session[
            "user_id"
        ]
    )


    if not user:

        session.clear()


        return jsonify({

            "error":
                "User not found"

        }), 404


    return jsonify({

        "user":
            user.to_dict()

    })


# =========================================================
# CREATE KUNDLI
# =========================================================

@app.post("/api/kundli")
@login_required
def create_kundli():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


    # =====================================================
    # REQUIRED FIELDS
    # =====================================================

    required_fields = [

        "name",

        "date",

        "time",

        "place",

        "latitude",

        "longitude",

        "timezone"

    ]


    missing = [

        field

        for field in required_fields

        if data.get(field)
        in (
            None,
            ""
        )

    ]


    if missing:

        return jsonify({

            "error":
                (
                    "Missing fields: "
                    + ", ".join(
                        missing
                    )
                )

        }), 400


    # =====================================================
    # INPUT VALIDATION
    # =====================================================

    try:

        latitude = float(
            data["latitude"]
        )

        longitude = float(
            data["longitude"]
        )

        timezone_hours = float(
            data["timezone"]
        )


        datetime.strptime(

            str(
                data["date"]
            ),

            "%Y-%m-%d"

        )


        datetime.strptime(

            str(
                data["time"]
            ),

            "%H:%M"

        )


    except (
        ValueError,
        TypeError
    ):

        return jsonify({

            "error":
                (
                    "Invalid date, time, "
                    "latitude, longitude "
                    "or timezone."
                )

        }), 400


    # =====================================================
    # LATITUDE VALIDATION
    # =====================================================

    if not (
        -90
        <= latitude
        <= 90
    ):

        return jsonify({

            "error":
                "Latitude is out of range."

        }), 400


    # =====================================================
    # LONGITUDE VALIDATION
    # =====================================================

    if not (
        -180
        <= longitude
        <= 180
    ):

        return jsonify({

            "error":
                "Longitude is out of range."

        }), 400


    # =====================================================
    # TIMEZONE VALIDATION
    # =====================================================

    if not (
        -14
        <= timezone_hours
        <= 14
    ):

        return jsonify({

            "error":
                "Timezone is out of range."

        }), 400


    # =====================================================
    # CLEAN INPUT
    # =====================================================

    name = str(
        data["name"]
    ).strip()


    place = str(
        data["place"]
    ).strip()


    birth_date = str(
        data["date"]
    )


    birth_time = str(
        data["time"]
    )


    if not name:

        return jsonify({

            "error":
                "Name cannot be empty."

        }), 400


    if not place:

        return jsonify({

            "error":
                "Birth place cannot be empty."

        }), 400


    # =====================================================
    # GENERATE CHART
    # =====================================================

    try:

        print()
        print("=" * 80)

        print(
            "GENERATING KUNDLI"
        )

        print("=" * 80)


        print(
            f"Name      : {name}"
        )

        print(
            f"Date      : {birth_date}"
        )

        print(
            f"Time      : {birth_time}"
        )

        print(
            f"Place     : {place}"
        )

        print(
            f"Latitude  : {latitude}"
        )

        print(
            f"Longitude : {longitude}"
        )

        print(
            f"Timezone  : UTC {timezone_hours:+g}"
        )


        print("=" * 80)


        # =================================================
        # BASIC KUNDLI
        # =================================================

        chart = generate_kundli(

            name=name,

            birth_date=birth_date,

            birth_time=birth_time,

            place=place,

            latitude=latitude,

            longitude=longitude,

            timezone=timezone_hours

        )


        print()
        print(
            "✓ Basic Kundli generated"
        )


        # =================================================
        # COMPLETE ANALYSIS
        # =================================================

        print()
        print("=" * 80)

        print(
            "RUNNING COMPLETE ASTROLOGY ANALYSIS"
        )

        print("=" * 80)


        chart = attach_complete_analysis(
            chart
        )


        # =================================================
        # ANALYSIS STATUS
        # =================================================

        analysis = chart.get(
            "analysis",
            {}
        )


        summary = analysis.get(
            "summary",
            {}
        )


        successful_modules = summary.get(
            "successful_modules",
            0
        )


        total_modules = summary.get(
            "total_modules",
            0
        )


        completion = summary.get(
            "completion_percentage",
            0
        )


        print()
        print(
            "✓ Complete analysis generated"
        )


        print(
            f"✓ Modules: "
            f"{successful_modules}/"
            f"{total_modules}"
        )


        print(
            f"✓ Completion: "
            f"{completion}%"
        )


        # =================================================
        # SAVE BIRTH PROFILE
        # =================================================

        profile = BirthProfile(

            user_id=
                session[
                    "user_id"
                ],

            name=name,

            birth_date=birth_date,

            birth_time=birth_time,

            place=place,

            latitude=latitude,

            longitude=longitude,

            timezone=timezone_hours

        )


        db.session.add(
            profile
        )


        db.session.flush()


        # =================================================
        # SAVE COMPLETE CHART
        # =================================================

        saved = SavedChart(

            user_id=
                session[
                    "user_id"
                ],

            birth_profile_id=
                profile.id,

            chart_json=
                json.dumps(
                    chart,
                    ensure_ascii=False
                )

        )


        db.session.add(
            saved
        )


        db.session.commit()


        # =================================================
        # SAVE LAST CHART
        # =================================================

        session[
            "last_chart_id"
        ] = saved.id


        print()
        print(
            "✓ Complete chart saved to database"
        )


        print("=" * 80)

        print(
            "✓ KUNDLI GENERATED SUCCESSFULLY"
        )

        print("=" * 80)

        print()


        # =================================================
        # RESPONSE
        # =================================================

        return jsonify({

            "success":
                True,

            "chart":
                chart,

            "chart_id":
                saved.id,

            "analysis_complete":
                summary.get(
                    "complete",
                    False
                ),

            "analysis_modules":
                successful_modules,

            "analysis_total":
                total_modules,

            "analysis_completion":
                completion

        })


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as exc:

        db.session.rollback()


        print()
        print("=" * 80)

        print(
            "🔥 KUNDLI GENERATION ERROR"
        )

        print("=" * 80)


        print(
            f"ERROR TYPE: "
            f"{type(exc).__name__}"
        )


        print(
            f"ERROR: "
            f"{str(exc)}"
        )


        print()
        print(
            "FULL TRACEBACK:"
        )


        traceback.print_exc()


        print("=" * 80)
        print()


        return jsonify({

            "success":
                False,

            "error":
                (
                    "Could not generate "
                    "the chart: "
                    f"{type(exc).__name__}: "
                    f"{str(exc)}"
                )

        }), 500


# =========================================================
# GET LATEST KUNDLI
# =========================================================

@app.get("/api/kundli/latest")
@login_required
def latest_kundli():

    saved = (

        SavedChart.query

        .filter_by(

            user_id=
                session[
                    "user_id"
                ]

        )

        .order_by(
            SavedChart.created_at.desc()
        )

        .first()

    )


    if not saved:

        return jsonify({

            "chart":
                None

        })


    try:

        chart = json.loads(
            saved.chart_json
        )


    except (
        TypeError,
        json.JSONDecodeError
    ):

        return jsonify({

            "error":
                "Saved chart data is corrupted."

        }), 500


    return jsonify({

        "chart":
            chart,

        "chart_id":
            saved.id

    })


# =========================================================
# AI ASTROLOGER
# =========================================================

@app.post("/api/ai/ask")
@login_required
def ai_ask():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


    question = str(
        data.get(
            "question",
            ""
        )
    ).strip()


    if not question:

        return jsonify({

            "error":
                "Please enter a question."

        }), 400


    # =====================================================
    # GET LATEST CHART
    # =====================================================

    saved = (

        SavedChart.query

        .filter_by(

            user_id=
                session[
                    "user_id"
                ]

        )

        .order_by(
            SavedChart.created_at.desc()
        )

        .first()

    )


    if not saved:

        return jsonify({

            "error":
                "Create a Kundli first."

        }), 400


    # =====================================================
    # LOAD CHART
    # =====================================================

    try:

        chart = json.loads(
            saved.chart_json
        )


    except (
        TypeError,
        json.JSONDecodeError
    ):

        return jsonify({

            "error":
                "Saved chart data is corrupted."

        }), 500


    # =====================================================
    # CHECK COMPLETE ANALYSIS
    # =====================================================

    if "analysis" not in chart:

        try:

            print(
                "Complete analysis missing."
            )

            print(
                "Generating analysis for AI..."
            )


            chart = attach_complete_analysis(
                chart
            )


        except Exception as exc:

            print(
                "Analysis generation failed:"
            )

            traceback.print_exc()


    # =====================================================
    # GEMINI
    # =====================================================

    try:

        # answer_question() already returns a dictionary
        # containing success, answer and optional error.
        result = answer_question(
            question,
            chart
        )

        # Make sure we always return a proper JSON object.
        if not isinstance(result, dict):

            return jsonify({
                "success": False,
                "answer": "Invalid response received from AI Jyotish.",
                "error": "Gemini returned an invalid response."
            }), 500

        return jsonify({

            "success":
                result.get(
                    "success",
                    True
                ),

            "answer":
                result.get(
                    "answer",
                    "No answer was returned."
                ),

            "error":
                result.get(
                    "error"
                )

        })


    except Exception as exc:

        print()
        print("=" * 80)

        print(
            "🔥 AI ASTROLOGER ERROR"
        )

        print("=" * 80)

        traceback.print_exc()

        print("=" * 80)

        return jsonify({

            "success":
                False,

            "answer":
                "Something went wrong while generating your AI Jyotish response.",

            "error":
                str(exc)

        }), 500

# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/api/health")
def health():

    return jsonify({

        "status":
            "ok",

        "service":
            "AI Jyotish"

    })


# =========================================================
# DEBUG INFORMATION
# =========================================================

@app.get("/api/debug")
def debug_info():

    return jsonify({

        "application":
            "AI Jyotish",

        "backend":
            "Flask",

        "frontend_directory":
            FRONTEND_DIR,

        "database":
            "SQLite",

        "gemini_configured":
            bool(

                os.getenv(
                    "GEMINI_API_KEY"
                )

                or

                os.getenv(
                    "GOOGLE_API_KEY"
                )

            ),

        "gemini_model":
            os.getenv(
                "GEMINI_MODEL",
                "gemini-3.5-flash"
            ),

        "analysis_engine":
            True

    })


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    host = os.getenv(
        "HOST",
        "127.0.0.1"
    )


    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )


    debug = (
        os.getenv(
            "FLASK_DEBUG",
            "1"
        )
        == "1"
    )


    print()
    print("=" * 60)
    print(
        "        AI JYOTISH"
    )
    print("=" * 60)


    print(
        f"Server: "
        f"http://{host}:{port}"
    )


    print(
        f"Frontend: "
        f"{FRONTEND_DIR}"
    )


    print(
        f"Debug: "
        f"{debug}"
    )


    print(
        "Gemini Model: "
        + os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash"
        )
    )


    print(
        "Gemini API: "
        + (
            "Configured"
            if (
                os.getenv(
                    "GEMINI_API_KEY"
                )
                or os.getenv(
                    "GOOGLE_API_KEY"
                )
            )
            else
            "Not Configured"
        )
    )


    print(
        "Complete Analysis Engine: ENABLED"
    )


    print("=" * 60)
    print()


    app.run(

        host=host,

        port=port,

        debug=debug

    )