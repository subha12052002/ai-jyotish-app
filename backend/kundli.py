# =========================================================
# AI JYOTISH
# kundli.py
#
# Main Kundli Calculation Orchestrator
#
# Uses:
#   - Swiss Ephemeris
#   - Sidereal Zodiac
#   - Lahiri Ayanamsha
#   - Whole Sign Houses
#   - Vimshottari Dasha
#   - Yoga Detection
#   - Navamsa / D9
# =========================================================


from datetime import datetime, timezone as dt_timezone


# =========================================================
# EPHEMERIS
# =========================================================

from ephemeris import (
    julian_day,
    calculate_planets,
    calculate_ascendant,
    house_from_sign,
    SIGNS,
)


# =========================================================
# DASHA
# =========================================================

from dasha import (
    get_current_dasha,
)


# =========================================================
# YOGA
# =========================================================

from yoga import (
    detect_yogas,
)


# =========================================================
# DIVISIONAL CHARTS
# =========================================================

from divisional_charts import (
    build_navamsa,
)


# =========================================================
# SAFE DICTIONARY GET
# =========================================================

def safe_get(value, key, default=None):
    """
    Safely get a value from a dictionary.

    Prevents crashes if a value is missing.
    """

    if not isinstance(value, dict):
        return default

    return value.get(
        key,
        default
    )


# =========================================================
# FIND PLANET
# =========================================================

def find_planet(
    planets,
    planet_name
):
    """
    Find a planet by name.
    """

    for planet in planets:

        if planet.get("name") == planet_name:

            return planet

    return None


# =========================================================
# BUILD WHOLE SIGN HOUSES
# =========================================================

def build_whole_sign_houses(
    ascendant_sign_index
):
    """
    Build all 12 Whole Sign houses.

    Ascendant sign = House 1.
    Next sign = House 2.
    etc.
    """

    houses = []

    ascendant_sign_index = int(
        ascendant_sign_index
    )

    for house_number in range(
        1,
        13
    ):

        sign_index = (
            ascendant_sign_index
            + house_number
            - 1
        ) % 12

        houses.append({

            "house":
                house_number,

            "sign_index":
                sign_index,

            "sign":
                SIGNS[sign_index],

        })

    return houses


# =========================================================
# ASSIGN PLANET HOUSES
# =========================================================

def assign_houses_to_planets(
    planets,
    ascendant_sign_index
):
    """
    Assign Whole Sign house to every planet.
    """

    for planet in planets:

        sign_index = planet.get(
            "sign_index"
        )

        if sign_index is None:
            continue

        planet["house"] = house_from_sign(

            sign_index,

            ascendant_sign_index

        )

    return planets


# =========================================================
# ASCENDANT DATA
# =========================================================

def build_ascendant_data(
    ascendant
):
    """
    Create a clean Ascendant dictionary.
    """

    return {

        "name":
            safe_get(
                ascendant,
                "sign"
            ),

        "sign":
            safe_get(
                ascendant,
                "sign"
            ),

        "sign_index":
            safe_get(
                ascendant,
                "sign_index"
            ),

        "degree":
            safe_get(
                ascendant,
                "degree"
            ),

        "degree_dms":
            safe_get(
                ascendant,
                "degree_dms"
            ),

        "longitude":
            safe_get(
                ascendant,
                "longitude"
            ),

        "longitude_dms":
            safe_get(
                ascendant,
                "longitude_dms"
            ),

    }


# =========================================================
# BASIC SUMMARY
# =========================================================

def build_basic_summary(
    planets,
    ascendant
):
    """
    Build basic chart summary.

    IMPORTANT:
    We intentionally use:

        ascendant_sign

    instead of:

        ascendant

    so that the complete Ascendant dictionary is
    never overwritten.
    """

    sun = find_planet(
        planets,
        "Sun"
    )

    moon = find_planet(
        planets,
        "Moon"
    )

    return {

        # IMPORTANT:
        # Do NOT use "ascendant" here.
        "ascendant_sign":
            safe_get(
                ascendant,
                "sign"
            ),

        "ascendant_degree":
            safe_get(
                ascendant,
                "degree"
            ),

        "ascendant_degree_dms":
            safe_get(
                ascendant,
                "degree_dms"
            ),

        "sun_sign":
            safe_get(
                sun,
                "sign"
            ),

        "sun_degree":
            safe_get(
                sun,
                "degree"
            ),

        "sun_degree_dms":
            safe_get(
                sun,
                "degree_dms"
            ),

        "moon_sign":
            safe_get(
                moon,
                "sign"
            ),

        "moon_degree":
            safe_get(
                moon,
                "degree"
            ),

        "moon_degree_dms":
            safe_get(
                moon,
                "degree_dms"
            ),

        "moon_nakshatra":
            safe_get(
                moon,
                "nakshatra"
            ),

        "moon_nakshatra_lord":
            safe_get(
                moon,
                "nakshatra_lord"
            ),

        "moon_pada":
            safe_get(
                moon,
                "pada"
            ),

    }


# =========================================================
# PLANET SUMMARY
# =========================================================

def build_planet_summary(
    planets
):
    """
    Create a compact summary of every planet.

    Used by:
        - Frontend
        - AI Astrologer
        - Future analysis modules
    """

    summary = {}

    for planet in planets:

        name = planet.get(
            "name"
        )

        if not name:
            continue

        summary[name] = {

            "name":
                name,

            "sign":
                planet.get(
                    "sign"
                ),

            "sign_english":
                planet.get(
                    "sign_english"
                ),

            "sign_index":
                planet.get(
                    "sign_index"
                ),

            "degree":
                planet.get(
                    "degree"
                ),

            "degree_dms":
                planet.get(
                    "degree_dms"
                ),

            "longitude":
                planet.get(
                    "longitude"
                ),

            "longitude_dms":
                planet.get(
                    "longitude_dms"
                ),

            "house":
                planet.get(
                    "house"
                ),

            "rashi_lord":
                planet.get(
                    "rashi_lord"
                ),

            "nakshatra":
                planet.get(
                    "nakshatra"
                ),

            "nakshatra_lord":
                planet.get(
                    "nakshatra_lord"
                ),

            "pada":
                planet.get(
                    "pada"
                ),

            "retrograde":
                planet.get(
                    "retrograde",
                    False
                ),

            "speed":
                planet.get(
                    "speed"
                ),

        }

    return summary


# =========================================================
# GENERATE KUNDLI
# =========================================================

def generate_kundli(
    name,
    birth_date,
    birth_time,
    place,
    latitude,
    longitude,
    timezone,
):
    """
    Generate a complete Vedic Kundli.

    Parameters
    ----------
    name:
        Person's name.

    birth_date:
        YYYY-MM-DD

    birth_time:
        HH:MM

    place:
        Birth place.

    latitude:
        Birth latitude.

    longitude:
        Birth longitude.

    timezone:
        Numeric UTC offset.

        Example:
            India = 5.5
    """

    # =====================================================
    # NORMALIZE INPUTS
    # =====================================================

    name = str(
        name
    ).strip()

    birth_date = str(
        birth_date
    ).strip()

    birth_time = str(
        birth_time
    ).strip()

    place = str(
        place
    ).strip()

    latitude = float(
        latitude
    )

    longitude = float(
        longitude
    )

    # IMPORTANT:
    #
    # This variable is a numeric UTC offset.
    #
    # Example:
    # India = 5.5
    #
    # We use dt_timezone for Python's timezone
    # class so there is no naming conflict.
    timezone = float(
        timezone
    )


    # =====================================================
    # VALIDATE NAME
    # =====================================================

    if not name:

        raise ValueError(
            "Name cannot be empty."
        )


    # =====================================================
    # VALIDATE PLACE
    # =====================================================

    if not place:

        raise ValueError(
            "Birth place cannot be empty."
        )


    # =====================================================
    # VALIDATE LATITUDE
    # =====================================================

    if not (
        -90.0
        <= latitude
        <= 90.0
    ):

        raise ValueError(
            "Latitude must be between "
            "-90 and 90."
        )


    # =====================================================
    # VALIDATE LONGITUDE
    # =====================================================

    if not (
        -180.0
        <= longitude
        <= 180.0
    ):

        raise ValueError(
            "Longitude must be between "
            "-180 and 180."
        )


    # =====================================================
    # VALIDATE TIMEZONE
    # =====================================================

    if not (
        -14.0
        <= timezone
        <= 14.0
    ):

        raise ValueError(
            "Timezone must be between "
            "-14 and +14."
        )


    # =====================================================
    # VALIDATE DATE
    # =====================================================

    try:

        datetime.strptime(
            birth_date,
            "%Y-%m-%d"
        )

    except ValueError:

        raise ValueError(
            "Invalid birth date. "
            "Expected YYYY-MM-DD."
        )


    # =====================================================
    # VALIDATE TIME
    # =====================================================

    try:

        datetime.strptime(
            birth_time,
            "%H:%M"
        )

    except ValueError:

        raise ValueError(
            "Invalid birth time. "
            "Expected HH:MM."
        )


    # =====================================================
    # JULIAN DAY
    # =====================================================

    jd = julian_day(

        birth_date,

        birth_time,

        timezone

    )


    # =====================================================
    # CALCULATE PLANETS
    # =====================================================

    planets = calculate_planets(
        jd
    )

    if not planets:

        raise RuntimeError(
            "Planet calculation failed."
        )


    # =====================================================
    # CALCULATE ASCENDANT
    # =====================================================

    ascendant_raw = calculate_ascendant(

        jd,

        latitude,

        longitude

    )

    if not ascendant_raw:

        raise RuntimeError(
            "Ascendant calculation failed."
        )


    # =====================================================
    # ASCENDANT SIGN
    # =====================================================

    ascendant_sign_index = int(

        ascendant_raw[
            "sign_index"
        ]

    )


    # =====================================================
    # ASSIGN PLANET HOUSES
    # =====================================================

    planets = assign_houses_to_planets(

        planets,

        ascendant_sign_index

    )


    # =====================================================
    # BUILD HOUSES
    # =====================================================

    houses = build_whole_sign_houses(

        ascendant_sign_index

    )


    # =====================================================
    # BUILD ASCENDANT
    # =====================================================

    ascendant = build_ascendant_data(

        ascendant_raw

    )


    # =====================================================
    # FIND SUN
    # =====================================================

    sun = find_planet(

        planets,

        "Sun"

    )

    if sun is None:

        raise RuntimeError(
            "Sun calculation failed."
        )


    # =====================================================
    # FIND MOON
    # =====================================================

    moon = find_planet(

        planets,

        "Moon"

    )

    if moon is None:

        raise RuntimeError(
            "Moon calculation failed."
        )


    # =====================================================
    # BASIC SUMMARY
    # =====================================================

    summary = build_basic_summary(

        planets,

        ascendant_raw

    )


    # =====================================================
    # PLANET SUMMARY
    # =====================================================

    planet_summary = build_planet_summary(

        planets

    )


    # =====================================================
    # BASE CHART
    #
    # Used by yoga.py.
    # =====================================================

    base_chart = {

        "name":
            name,

        "birth_date":
            birth_date,

        "birth_time":
            birth_time,

        "place":
            place,

        "latitude":
            latitude,

        "longitude":
            longitude,

        "timezone":
            timezone,

        "julian_day":
            jd,

        "ascendant":
            ascendant,

        "planets":
            planets,

        "houses":
            houses,

    }


    # =====================================================
    # VIMSHOTTARI DASHA
    # =====================================================

    try:

        dashas = get_current_dasha(
            jd
        )

    except Exception as error:

        dashas = {

            "available":
                False,

            "error":
                str(error)

        }


    # =====================================================
    # YOGAS
    # =====================================================

    try:

        yogas = detect_yogas(

            base_chart

        )

    except Exception as error:

        yogas = [

            {

                "name":
                    "Yoga calculation unavailable",

                "type":
                    "System",

                "description":
                    str(error)

            }

        ]


    # =====================================================
    # NAVAMSA / D9
    # =====================================================

    try:

        navamsa_planets = build_navamsa(

            planets

        )

        navamsa = {

            "available":
                True,

            "name":
                "Navamsa",

            "code":
                "D9",

            "planets":
                navamsa_planets

        }

    except Exception as error:

        navamsa = {

            "available":
                False,

            "name":
                "Navamsa",

            "code":
                "D9",

            "planets":
                [],

            "error":
                str(error)

        }


    # =====================================================
    # COMPLETE CHART
    # =====================================================

    chart = {

        # -------------------------------------------------
        # PERSONAL DETAILS
        # -------------------------------------------------

        "name":
            name,

        "birth_date":
            birth_date,

        "birth_time":
            birth_time,

        "place":
            place,

        "latitude":
            latitude,

        "longitude":
            longitude,

        "timezone":
            timezone,


        # -------------------------------------------------
        # JULIAN DAY
        # -------------------------------------------------

        "julian_day":
            jd,


        # -------------------------------------------------
        # ASCENDANT
        #
        # This remains a DICTIONARY.
        #
        # IMPORTANT:
        # summary contains "ascendant_sign",
        # NOT "ascendant".
        # -------------------------------------------------

        "ascendant":
            ascendant,


        # -------------------------------------------------
        # BASIC SUMMARY
        # -------------------------------------------------

        **summary,


        # -------------------------------------------------
        # PLANETS
        # -------------------------------------------------

        "planets":
            planets,


        # -------------------------------------------------
        # PLANET SUMMARY
        # -------------------------------------------------

        "planet_summary":
            planet_summary,


        # -------------------------------------------------
        # HOUSES
        # -------------------------------------------------

        "houses":
            houses,


        # -------------------------------------------------
        # DASHA
        # -------------------------------------------------

        "dashas":
            dashas,


        # -------------------------------------------------
        # YOGAS
        # -------------------------------------------------

        "yogas":
            yogas,


        # -------------------------------------------------
        # DIVISIONAL CHARTS
        # -------------------------------------------------

        "divisional_charts": {

            # ---------------------------------------------
            # D1
            # ---------------------------------------------

            "D1": {

                "name":
                    "Rashi",

                "code":
                    "D1",

                "planets":
                    planets

            },


            # ---------------------------------------------
            # D9
            # ---------------------------------------------

            "D9":
                navamsa

        },


        # -------------------------------------------------
        # CALCULATION INFORMATION
        # -------------------------------------------------

        "calculation": {

            "zodiac":
                "Sidereal",

            "ayanamsha":
                "Lahiri",

            "house_system":
                "Whole Sign",

            "dasha_system":
                "Vimshottari",

            "primary_chart":
                "D1",

            "navamsa":
                "D9",

        },


        # -------------------------------------------------
        # ENGINE
        # -------------------------------------------------

        "engine": {

            "name":
                "AI Jyotish",

            "version":
                "1.0",

            # IMPORTANT FIX:
            #
            # dt_timezone is Python's timezone class.
            #
            # timezone is the numeric birth UTC offset.
            #
            "generated_at":
                datetime.now(
                    dt_timezone.utc
                ).isoformat()

        }

    }


    # =====================================================
    # RETURN
    # =====================================================

    return chart


# =========================================================
# DIRECT TEST
# =========================================================

if __name__ == "__main__":

    print()

    print("=" * 70)

    print(
        "AI JYOTISH - KUNDLI ENGINE TEST"
    )

    print("=" * 70)


    try:

        # =================================================
        # TEST DATA
        # =================================================

        chart = generate_kundli(

            name="Test User",

            birth_date="2000-08-15",

            birth_time="10:30",

            place="Kolkata",

            latitude=22.5726,

            longitude=88.3639,

            timezone=5.5

        )


        # =================================================
        # SUCCESS
        # =================================================

        print()

        print(
            "✓ KUNDLI GENERATED SUCCESSFULLY"
        )


        # =================================================
        # PERSONAL DETAILS
        # =================================================

        print()

        print(
            "Name:",
            chart["name"]
        )

        print(
            "Birth Date:",
            chart["birth_date"]
        )

        print(
            "Birth Time:",
            chart["birth_time"]
        )

        print(
            "Place:",
            chart["place"]
        )


        # =================================================
        # ASCENDANT
        # =================================================

        print()

        print(
            "ASCENDANT"
        )

        print("-" * 70)

        print(
            "Sign:",
            chart["ascendant"].get(
                "sign"
            )
        )

        print(
            "Sign Index:",
            chart["ascendant"].get(
                "sign_index"
            )
        )

        print(
            "Degree:",
            chart["ascendant"].get(
                "degree"
            )
        )

        print(
            "Degree DMS:",
            chart["ascendant"].get(
                "degree_dms"
            )
        )

        print(
            "Longitude:",
            chart["ascendant"].get(
                "longitude"
            )
        )


        # =================================================
        # SUN
        # =================================================

        print()

        print(
            "SUN"
        )

        print("-" * 70)

        print(
            "Sign:",
            chart["sun_sign"]
        )

        print(
            "Degree:",
            chart["sun_degree_dms"]
        )


        # =================================================
        # MOON
        # =================================================

        print()

        print(
            "MOON"
        )

        print("-" * 70)

        print(
            "Sign:",
            chart["moon_sign"]
        )

        print(
            "Degree:",
            chart["moon_degree_dms"]
        )

        print(
            "Nakshatra:",
            chart["moon_nakshatra"]
        )

        print(
            "Nakshatra Lord:",
            chart["moon_nakshatra_lord"]
        )

        print(
            "Pada:",
            chart["moon_pada"]
        )


        # =================================================
        # PLANETS
        # =================================================

        print()

        print(
            "PLANETARY POSITIONS"
        )

        print("-" * 70)

        for planet in chart["planets"]:

            print(

                f'{planet.get("name", "-"):10} | '

                f'{planet.get("sign", "-"):15} | '

                f'House '
                f'{str(planet.get("house", "-")):2} | '

                f'{planet.get("degree_dms", "-"):15} | '

                f'{planet.get("nakshatra", "-"):18} | '

                f'Lord '
                f'{planet.get("nakshatra_lord", "-"):10} | '

                f'Pada '
                f'{str(planet.get("pada", "-")):2} | '

                f'R'
                f'{"YES" if planet.get("retrograde") else "NO"}'

            )


        # =================================================
        # HOUSES
        # =================================================

        print()

        print(
            "WHOLE SIGN HOUSES"
        )

        print("-" * 70)

        for house in chart["houses"]:

            print(

                f'House '
                f'{house["house"]:2} → '

                f'{house["sign"]}'

            )


        # =================================================
        # DASHA
        # =================================================

        print()

        print(
            "VIMSHOTTARI DASHA"
        )

        print("-" * 70)

        dasha = chart["dashas"]


        if dasha.get(
            "available",
            True
        ):

            print(

                "Starting Lord:",

                dasha.get(
                    "starting_lord"
                )

            )

            print(

                "Nakshatra:",

                dasha.get(
                    "nakshatra",
                    {}
                ).get(
                    "name",
                    "-"
                )

            )

            print(

                "Current Mahadasha:",

                dasha.get(
                    "current_mahadasha_lord"
                )

            )

            print(

                "Current Antardasha:",

                dasha.get(
                    "current_antardasha_lord"
                )

            )

            print()

            print(
                "Mahadasha Timeline:"
            )

            for period in dasha.get(
                "mahadasha_timeline",
                []
            ):

                print(

                    "  ",
                    period.get(
                        "lord",
                        "-"
                    ),

                    "|",

                    period.get(
                        "start",
                        "-"
                    ),

                    "→",

                    period.get(
                        "end",
                        "-"
                    )

                )

        else:

            print(

                "Dasha Error:",

                dasha.get(
                    "error"
                )

            )


        # =================================================
        # YOGAS
        # =================================================

        print()

        print(
            "YOGAS"
        )

        print("-" * 70)

        for yoga in chart["yogas"]:

            print(

                "-",

                yoga.get(
                    "name",
                    "Unknown Yoga"
                )

            )

            print(

                "  Type:",

                yoga.get(
                    "type",
                    "-"
                )

            )

            print(

                "  Description:",

                yoga.get(
                    "description",
                    "-"
                )

            )


        # =================================================
        # NAVAMSA / D9
        # =================================================

        print()

        print(
            "NAVAMSA / D9"
        )

        print("-" * 70)

        d9 = chart[
            "divisional_charts"
        ][
            "D9"
        ]

        print(

            "Available:",

            d9.get(
                "available"
            )

        )


        if d9.get(
            "available"
        ):

            for planet in d9.get(
                "planets",
                []
            ):

                print(

                    f'{planet.get("name", "-"):10} → '

                    f'{planet.get("sign", "-"):15} | '

                    f'Navamsa Part '
                    f'{planet.get("navamsa", "-")}'

                )

        else:

            print(

                "D9 Error:",

                d9.get(
                    "error"
                )

            )


        # =================================================
        # CALCULATION
        # =================================================

        print()

        print(
            "CALCULATION"
        )

        print("-" * 70)

        print(
            "Zodiac:",
            chart["calculation"]["zodiac"]
        )

        print(
            "Ayanamsha:",
            chart["calculation"]["ayanamsha"]
        )

        print(
            "House System:",
            chart["calculation"]["house_system"]
        )

        print(
            "Dasha System:",
            chart["calculation"]["dasha_system"]
        )

        print(
            "Julian Day:",
            chart["julian_day"]
        )


        # =================================================
        # ENGINE
        # =================================================

        print()

        print(
            "ENGINE"
        )

        print("-" * 70)

        print(
            "Name:",
            chart["engine"]["name"]
        )

        print(
            "Version:",
            chart["engine"]["version"]
        )

        print(
            "Generated:",
            chart["engine"]["generated_at"]
        )


        # =================================================
        # FINAL SUCCESS
        # =================================================

        print()

        print("=" * 70)

        print(
            "✓ TEST COMPLETED SUCCESSFULLY"
        )

        print("=" * 70)

        print()


    except Exception as error:

        # =================================================
        # ERROR
        # =================================================

        print()

        print("=" * 70)

        print(
            "✗ KUNDLI TEST FAILED"
        )

        print("=" * 70)

        print()

        print(
            type(error).__name__,
            ":",
            error
        )

        print()

        raise