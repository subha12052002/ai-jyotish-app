from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory
)

from flask_cors import CORS

from kundli import calculate_kundli

import os
import traceback


# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

FRONTEND_DIR = os.path.abspath(
    os.path.join(
        BASE_DIR,
        "..",
        "frontend"
    )
)


# =========================================================
# FLASK APP
# =========================================================

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

CORS(app)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# =========================================================
# BIRTH FORM
# =========================================================

@app.route("/birth-form.html")
def birth_form():

    return send_from_directory(
        FRONTEND_DIR,
        "birth-form.html"
    )


# =========================================================
# KUNDLI PAGE
# =========================================================

@app.route("/kundli.html")
def kundli_page():

    return send_from_directory(
        FRONTEND_DIR,
        "kundli.html"
    )


# =========================================================
# KUNDLI API
# =========================================================

@app.route(
    "/api/kundli",
    methods=["POST"]
)
def create_kundli():

    print("\n")
    print("=" * 70)
    print("KUNDLI API REQUEST")
    print("=" * 70)

    try:

        # =================================================
        # GET JSON
        # =================================================

        data = request.get_json(
            silent=True
        )

        if not data:

            print("ERROR: No JSON data received.")

            return jsonify({
                "success": False,
                "error": "No JSON data received."
            }), 400


        print("Received data:")
        print(data)


        # =================================================
        # READ USER NAME
        # =================================================

        name = str(
            data.get(
                "name",
                ""
            )
        ).strip()


        # =================================================
        # READ DATE
        #
        # Accept BOTH:
        #
        # date
        # date_of_birth
        #
        # =================================================

        date = str(
            data.get(
                "date",
                data.get(
                    "date_of_birth",
                    ""
                )
            )
        ).strip()


        # =================================================
        # READ TIME
        #
        # Accept BOTH:
        #
        # time
        # time_of_birth
        #
        # =================================================

        time = str(
            data.get(
                "time",
                data.get(
                    "time_of_birth",
                    ""
                )
            )
        ).strip()


        # =================================================
        # READ PLACE
        # =================================================

        place = str(
            data.get(
                "place",
                data.get(
                    "birth_place",
                    ""
                )
            )
        ).strip()


        # =================================================
        # READ LATITUDE
        # =================================================

        latitude = data.get(
            "latitude"
        )


        # =================================================
        # READ LONGITUDE
        # =================================================

        longitude = data.get(
            "longitude"
        )


        # =================================================
        # READ TIMEZONE
        #
        # Accept BOTH:
        #
        # timezone
        # timezone_offset
        #
        # =================================================

        timezone_offset = data.get(
            "timezone",
            data.get(
                "timezone_offset",
                5.5
            )
        )


        # =================================================
        # PRINT NORMALIZED DATA
        # =================================================

        print("")
        print("Normalized data:")
        print(
            "Name:",
            name
        )
        print(
            "Date:",
            date
        )
        print(
            "Time:",
            time
        )
        print(
            "Place:",
            place
        )
        print(
            "Latitude:",
            latitude
        )
        print(
            "Longitude:",
            longitude
        )
        print(
            "Timezone:",
            timezone_offset
        )


        # =================================================
        # REQUIRED FIELDS
        # =================================================

        if not name:

            return jsonify({
                "success": False,
                "error": "Name is required."
            }), 400


        if not date:

            return jsonify({
                "success": False,
                "error": "Date of birth is required."
            }), 400


        if not time:

            return jsonify({
                "success": False,
                "error": "Time of birth is required."
            }), 400


        if not place:

            return jsonify({
                "success": False,
                "error": "Birth place is required."
            }), 400


        if latitude is None:

            return jsonify({
                "success": False,
                "error": "Latitude is required."
            }), 400


        if longitude is None:

            return jsonify({
                "success": False,
                "error": "Longitude is required."
            }), 400


        # =================================================
        # CONVERT NUMBERS
        # =================================================

        try:

            latitude = float(
                latitude
            )

            longitude = float(
                longitude
            )

            timezone_offset = float(
                timezone_offset
            )

        except (
            TypeError,
            ValueError
        ):

            return jsonify({
                "success": False,
                "error":
                    "Latitude, longitude and timezone must be numbers."
            }), 400


        # =================================================
        # VALIDATE LATITUDE
        # =================================================

        if latitude < -90 or latitude > 90:

            return jsonify({
                "success": False,
                "error":
                    "Latitude must be between -90 and 90."
            }), 400


        # =================================================
        # VALIDATE LONGITUDE
        # =================================================

        if longitude < -180 or longitude > 180:

            return jsonify({
                "success": False,
                "error":
                    "Longitude must be between -180 and 180."
            }), 400


        # =================================================
        # VALIDATE TIMEZONE
        # =================================================

        if timezone_offset < -14 or timezone_offset > 14:

            return jsonify({
                "success": False,
                "error":
                    "Timezone offset must be between -14 and +14."
            }), 400


        # =================================================
        # CALCULATE KUNDLI
        # =================================================

        print("")
        print("Calculating Kundli...")


        result = calculate_kundli(

            date_of_birth=date,

            time_of_birth=time,

            latitude=latitude,

            longitude=longitude,

            timezone_offset=timezone_offset

        )


        # =================================================
        # CHECK RESULT
        # =================================================

        if not result:

            raise ValueError(
                "Kundli calculation returned no data."
            )


        if "ascendant" not in result:

            raise ValueError(
                "Ascendant was not returned by calculation."
            )


        if not result["ascendant"]:

            raise ValueError(
                "Ascendant calculation failed."
            )


        # =================================================
        # ADD USER INFORMATION
        # =================================================

        result["success"] = True

        result["name"] = name

        result["birth_date"] = date

        result["birth_time"] = time

        result["birth_place"] = place

        result["latitude"] = latitude

        result["longitude"] = longitude

        result["timezone"] = timezone_offset


        # =================================================
        # LOG SUCCESS
        # =================================================

        print("")
        print("=" * 70)
        print("KUNDLI CALCULATED SUCCESSFULLY")
        print("=" * 70)

        print(
            "Name:",
            name
        )

        print(
            "Birth date:",
            date
        )

        print(
            "Birth time:",
            time
        )

        print(
            "Birth place:",
            place
        )

        print(
            "Ascendant:",
            result["ascendant"]
        )

        print(
            "Planets:",
            len(
                result.get(
                    "planets",
                    {}
                )
            )
        )

        print(
            "Houses:",
            len(
                result.get(
                    "houses",
                    []
                )
            )
        )

        print("=" * 70)


        # =================================================
        # RETURN JSON
        # =================================================

        return jsonify(
            result
        ), 200


    # =====================================================
    # VALUE ERROR
    # =====================================================

    except ValueError as error:

        print("")
        print("=" * 70)
        print("KUNDLI VALIDATION ERROR")
        print("=" * 70)

        print(
            str(error)
        )

        print("=" * 70)


        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 400


    # =====================================================
    # UNEXPECTED ERROR
    # =====================================================

    except Exception as error:

        print("")
        print("=" * 70)
        print("KUNDLI SERVER ERROR")
        print("=" * 70)

        print(
            str(error)
        )

        print("")
        print("FULL TRACEBACK:")

        traceback.print_exc()

        print("=" * 70)


        return jsonify({

            "success": False,

            "error":
                "Unable to calculate Kundli.",

            "details":
                str(error)

        }), 500


# =========================================================
# STATIC FILES
# =========================================================

@app.route(
    "/<path:path>"
)
def serve_static(path):

    requested_file = os.path.join(
        FRONTEND_DIR,
        path
    )


    if os.path.isfile(
        requested_file
    ):

        return send_from_directory(
            FRONTEND_DIR,
            path
        )


    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "success": True,

        "message":
            "AI Jyotish API is running.",

        "swisseph":
            "available"

    }), 200


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    print("")
    print("=" * 70)
    print("                         AI JYOTISH")
    print("                    Vedic Astrology Backend")
    print("=" * 70)

    print("")
    print(
        "Frontend:",
        FRONTEND_DIR
    )

    print("")
    print(
        "Server running at:"
    )

    print(
        "http://127.0.0.1:5000/"
    )

    print("")
    print(
        "Health check:"
    )

    print(
        "GET /api/health"
    )

    print("")
    print(
        "Kundli API:"
    )

    print(
        "POST /api/kundli"
    )

    print("")
    print("=" * 70)


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )