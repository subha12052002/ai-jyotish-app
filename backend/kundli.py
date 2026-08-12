import swisseph as swe

from datetime import datetime, timezone, timedelta


# =========================================================
# AI JYOTISH
# VEDIC KUNDLI CALCULATION ENGINE
# =========================================================


# =========================================================
# ZODIAC
# =========================================================

ZODIAC_SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces"
]


ZODIAC_SIGNS_HINDI = [
    "Mesha",
    "Vrishabha",
    "Mithuna",
    "Karka",
    "Simha",
    "Kanya",
    "Tula",
    "Vrishchika",
    "Dhanu",
    "Makara",
    "Kumbha",
    "Meena"
]


# =========================================================
# NAKSHATRAS
# =========================================================

NAKSHATRAS = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati"
]


# =========================================================
# NAKSHATRA LORDS
# =========================================================

NAKSHATRA_LORDS = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury"
]


# =========================================================
# VIMSHOTTARI DASHA
# =========================================================

DASHA_YEARS = {

    "Ketu": 7,

    "Venus": 20,

    "Sun": 6,

    "Moon": 10,

    "Mars": 7,

    "Rahu": 18,

    "Jupiter": 16,

    "Saturn": 19,

    "Mercury": 17

}


DASHA_SEQUENCE = [
    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury"
]


# =========================================================
# PLANETS
# =========================================================

PLANETS = {

    "Sun": swe.SUN,

    "Moon": swe.MOON,

    "Mars": swe.MARS,

    "Mercury": swe.MERCURY,

    "Jupiter": swe.JUPITER,

    "Venus": swe.VENUS,

    "Saturn": swe.SATURN,

    "Rahu": swe.MEAN_NODE

}


# =========================================================
# HOUSE LORDS
# =========================================================

HOUSE_LORDS = {

    "Aries": "Mars",

    "Taurus": "Venus",

    "Gemini": "Mercury",

    "Cancer": "Moon",

    "Leo": "Sun",

    "Virgo": "Mercury",

    "Libra": "Venus",

    "Scorpio": "Mars",

    "Sagittarius": "Jupiter",

    "Capricorn": "Saturn",

    "Aquarius": "Saturn",

    "Pisces": "Jupiter"

}


# =========================================================
# NORMALIZE DEGREE
# =========================================================

def normalize_degree(degree):

    return float(degree) % 360.0


# =========================================================
# GET ZODIAC SIGN
# =========================================================

def get_sign(longitude):

    longitude = normalize_degree(
        longitude
    )

    sign_index = int(
        longitude // 30
    )

    degree_in_sign = (
        longitude % 30
    )

    return {

        "name":
            ZODIAC_SIGNS[sign_index],

        "vedic_name":
            ZODIAC_SIGNS_HINDI[sign_index],

        "index":
            sign_index,

        "degree":
            round(
                degree_in_sign,
                2
            )

    }


# =========================================================
# GET NAKSHATRA
# =========================================================

def get_nakshatra(longitude):

    longitude = normalize_degree(
        longitude
    )

    nakshatra_size = (
        360.0 / 27.0
    )

    nakshatra_index = int(
        longitude //
        nakshatra_size
    )

    degree_inside = (
        longitude %
        nakshatra_size
    )

    pada_size = (
        nakshatra_size / 4.0
    )

    pada = int(
        degree_inside /
        pada_size
    ) + 1

    pada = max(
        1,
        min(
            4,
            pada
        )
    )

    return {

        "name":
            NAKSHATRAS[
                nakshatra_index
            ],

        "index":
            nakshatra_index,

        "pada":
            pada,

        "lord":
            NAKSHATRA_LORDS[
                nakshatra_index % 9
            ]

    }


# =========================================================
# PLANET POSITION
# =========================================================

def get_planet_position(
    planet_id,
    julian_day
):

    flags = (
        swe.FLG_SWIEPH
        |
        swe.FLG_SIDEREAL
        |
        swe.FLG_SPEED
    )

    result = swe.calc_ut(
        julian_day,
        planet_id,
        flags
    )

    values = result[0]

    longitude = normalize_degree(
        values[0]
    )

    speed = float(
        values[3]
    )

    return (
        longitude,
        speed
    )


# =========================================================
# BUILD PLANET
# =========================================================

def build_planet(
    planet_name,
    planet_id,
    julian_day
):

    longitude, speed = (
        get_planet_position(
            planet_id,
            julian_day
        )
    )

    sign = get_sign(
        longitude
    )

    nakshatra = get_nakshatra(
        longitude
    )

    return {

        "planet":
            planet_name,

        "name":
            planet_name,

        "longitude":
            round(
                longitude,
                4
            ),

        "degree":
            round(
                sign["degree"],
                2
            ),

        "sign":
            sign["name"],

        "vedic_sign":
            sign["vedic_name"],

        "sign_index":
            sign["index"],

        "nakshatra":
            nakshatra["name"],

        "nakshatra_pada":
            nakshatra["pada"],

        "nakshatra_lord":
            nakshatra["lord"],

        "retrograde":
            speed < 0

    }


# =========================================================
# WHOLE SIGN HOUSE
#
# Vedic astrology commonly uses whole-sign houses:
#
# Ascendant sign = House 1
# Next sign       = House 2
# ...
# =========================================================

def get_whole_sign_house(
    planet_longitude,
    ascendant_longitude
):

    planet_sign = int(
        normalize_degree(
            planet_longitude
        ) // 30
    )

    ascendant_sign = int(
        normalize_degree(
            ascendant_longitude
        ) // 30
    )

    house = (
        planet_sign
        -
        ascendant_sign
    ) % 12 + 1

    return house


# =========================================================
# BUILD HOUSES
# =========================================================

def build_whole_sign_houses(
    ascendant_longitude
):

    ascendant_sign_index = int(
        normalize_degree(
            ascendant_longitude
        ) // 30
    )

    houses = []

    for house_number in range(
        1,
        13
    ):

        sign_index = (
            ascendant_sign_index
            +
            house_number
            -
            1
        ) % 12

        sign_name = (
            ZODIAC_SIGNS[
                sign_index
            ]
        )

        vedic_name = (
            ZODIAC_SIGNS_HINDI[
                sign_index
            ]
        )

        lord = HOUSE_LORDS.get(
            sign_name
        )

        houses.append({

            "house":
                house_number,

            "number":
                house_number,

            "sign":
                sign_name,

            "vedic_sign":
                vedic_name,

            "sign_index":
                sign_index,

            "lord":
                lord

        })

    return houses


# =========================================================
# BUILD HOUSE → PLANETS
# =========================================================

def build_house_planets(
    planets
):

    house_planets = {

        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
        12: []

    }

    for planet_name, planet in (
        planets.items()
    ):

        house = planet.get(
            "house"
        )

        if house in house_planets:

            house_planets[
                house
            ].append(
                planet_name
            )

    return house_planets


# =========================================================
# BUILD VIMSHOTTARI DASHA
# =========================================================

def calculate_vimshottari_dasha(
    moon_longitude
):

    nakshatra = get_nakshatra(
        moon_longitude
    )

    starting_lord = (
        nakshatra["lord"]
    )

    starting_index = (
        DASHA_SEQUENCE.index(
            starting_lord
        )
    )

    nakshatra_size = (
        360.0 / 27.0
    )

    pada_size = (
        nakshatra_size / 4.0
    )

    position_in_nakshatra = (
        normalize_degree(
            moon_longitude
        )
        %
        nakshatra_size
    )

    fraction_completed = (
        position_in_nakshatra
        /
        nakshatra_size
    )

    fraction_remaining = (
        1.0 -
        fraction_completed
    )

    first_duration = (
        DASHA_YEARS[
            starting_lord
        ]
        *
        fraction_remaining
    )

    durations = {}

    for i in range(9):

        lord = DASHA_SEQUENCE[
            (
                starting_index
                +
                i
            ) % 9
        ]

        if i == 0:

            years = first_duration

        else:

            years = DASHA_YEARS[
                lord
            ]

        durations[lord] = round(
            years,
            2
        )

    return {

        "system":
            "Vimshottari",

        "starting_planet":
            starting_lord,

        "nakshatra":
            nakshatra["name"],

        "nakshatra_pada":
            nakshatra["pada"],

        "durations":
            durations

    }


# =========================================================
# BASIC YOGAS
# =========================================================

def calculate_yogas(
    planets,
    houses
):

    yogas = []

    # -----------------------------------------------------
    # Gaja Kesari Yoga
    # Jupiter in kendra from Moon
    # -----------------------------------------------------

    moon = planets.get(
        "Moon"
    )

    jupiter = planets.get(
        "Jupiter"
    )

    if moon and jupiter:

        moon_house = moon.get(
            "house"
        )

        jupiter_house = jupiter.get(
            "house"
        )

        if moon_house and jupiter_house:

            difference = (
                jupiter_house
                -
                moon_house
            ) % 12 + 1

            if difference in [
                1,
                4,
                7,
                10
            ]:

                yogas.append({

                    "name":
                        "Gaja Kesari Yoga",

                    "description":
                        "Jupiter is positioned in a Kendra from the Moon."

                })

    # -----------------------------------------------------
    # Budha Aditya Yoga
    # Sun + Mercury same house
    # -----------------------------------------------------

    sun = planets.get(
        "Sun"
    )

    mercury = planets.get(
        "Mercury"
    )

    if sun and mercury:

        if (
            sun.get("house")
            ==
            mercury.get("house")
        ):

            yogas.append({

                "name":
                    "Budha Aditya Yoga",

                "description":
                    "Sun and Mercury are placed together."

            })

    return yogas


# =========================================================
# MAIN KUNDLI CALCULATION
# =========================================================

def calculate_kundli(
    date_of_birth,
    time_of_birth,
    latitude,
    longitude,
    timezone_offset
):

    # =====================================================
    # VALIDATION
    # =====================================================

    if not date_of_birth:

        raise ValueError(
            "Date of birth is required."
        )

    if not time_of_birth:

        raise ValueError(
            "Time of birth is required."
        )

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

        raise ValueError(
            "Latitude, longitude and timezone must be numbers."
        )


    if (
        latitude < -90
        or
        latitude > 90
    ):

        raise ValueError(
            "Latitude must be between -90 and 90."
        )


    if (
        longitude < -180
        or
        longitude > 180
    ):

        raise ValueError(
            "Longitude must be between -180 and 180."
        )


    # =====================================================
    # LAHIRI AYANAMSA
    # =====================================================

    swe.set_sid_mode(
        swe.SIDM_LAHIRI
    )


    # =====================================================
    # LOCAL DATE + TIME
    # =====================================================

    try:

        local_datetime = datetime.strptime(
            f"{date_of_birth} {time_of_birth}",
            "%Y-%m-%d %H:%M"
        )

    except ValueError:

        raise ValueError(
            "Date/time must use YYYY-MM-DD and HH:MM format."
        )


    # =====================================================
    # LOCAL → UTC
    # =====================================================

    offset = timedelta(
        hours=timezone_offset
    )

    utc_datetime = (
        local_datetime -
        offset
    )

    utc_datetime = (
        utc_datetime.replace(
            tzinfo=timezone.utc
        )
    )


    # =====================================================
    # UTC DECIMAL HOUR
    # =====================================================

    hour_decimal = (

        utc_datetime.hour

        +

        utc_datetime.minute / 60.0

        +

        utc_datetime.second / 3600.0

    )


    # =====================================================
    # JULIAN DAY
    # =====================================================

    julian_day = swe.julday(

        utc_datetime.year,

        utc_datetime.month,

        utc_datetime.day,

        hour_decimal

    )


    # =====================================================
    # PLANETS
    # =====================================================

    planets = {}


    for (
        planet_name,
        planet_id
    ) in PLANETS.items():

        planets[
            planet_name
        ] = build_planet(

            planet_name,

            planet_id,

            julian_day

        )


    # =====================================================
    # KETU
    # =====================================================

    rahu_longitude = (
        planets[
            "Rahu"
        ][
            "longitude"
        ]
    )


    ketu_longitude = normalize_degree(

        rahu_longitude
        +
        180.0

    )


    ketu_sign = get_sign(
        ketu_longitude
    )


    ketu_nakshatra = get_nakshatra(
        ketu_longitude
    )


    planets["Ketu"] = {

        "planet":
            "Ketu",

        "name":
            "Ketu",

        "longitude":
            round(
                ketu_longitude,
                4
            ),

        "degree":
            round(
                ketu_sign["degree"],
                2
            ),

        "sign":
            ketu_sign["name"],

        "vedic_sign":
            ketu_sign["vedic_name"],

        "sign_index":
            ketu_sign["index"],

        "nakshatra":
            ketu_nakshatra["name"],

        "nakshatra_pada":
            ketu_nakshatra["pada"],

        "nakshatra_lord":
            ketu_nakshatra["lord"],

        "retrograde":
            True

    }


    # =====================================================
    # ASCENDANT
    # =====================================================

    houses_raw, ascmc = swe.houses_ex(

        julian_day,

        latitude,

        longitude,

        b"P",

        swe.FLG_SIDEREAL

    )


    ascendant_longitude = normalize_degree(

        ascmc[0]

    )


    ascendant_sign = get_sign(

        ascendant_longitude

    )


    ascendant_nakshatra = get_nakshatra(

        ascendant_longitude

    )


    ascendant = {

        "longitude":
            round(
                ascendant_longitude,
                4
            ),

        "degree":
            round(
                ascendant_sign["degree"],
                2
            ),

        "sign":
            ascendant_sign["name"],

        "vedic_sign":
            ascendant_sign["vedic_name"],

        "sign_index":
            ascendant_sign["index"],

        "nakshatra":
            ascendant_nakshatra["name"],

        "nakshatra_pada":
            ascendant_nakshatra["pada"],

        "nakshatra_lord":
            ascendant_nakshatra["lord"]

    }


    # =====================================================
    # WHOLE SIGN HOUSES
    # =====================================================

    houses = build_whole_sign_houses(

        ascendant_longitude

    )


    # =====================================================
    # ASSIGN PLANETS TO HOUSES
    # =====================================================

    for (
        planet_name,
        planet
    ) in planets.items():

        planet_longitude = (
            planet[
                "longitude"
            ]
        )


        house = get_whole_sign_house(

            planet_longitude,

            ascendant_longitude

        )


        planet["house"] = house


    # =====================================================
    # HOUSE → PLANETS
    # =====================================================

    house_planets = build_house_planets(

        planets

    )


    # =====================================================
    # ADD PLANETS TO HOUSE DATA
    # =====================================================

    for house in houses:

        number = house[
            "house"
        ]

        house[
            "planets"
        ] = house_planets.get(

            number,

            []

        )


    # =====================================================
    # DASHA
    # =====================================================

    moon_longitude = (
        planets[
            "Moon"
        ][
            "longitude"
        ]
    )


    dasha = calculate_vimshottari_dasha(

        moon_longitude

    )


    # =====================================================
    # YOGAS
    # =====================================================

    yogas = calculate_yogas(

        planets,

        houses

    )


    # =====================================================
    # FINAL RESULT
    # =====================================================

    result = {

        "julian_day":
            julian_day,

        "utc_time":
            utc_datetime.isoformat(),

        "ayanamsa":
            "Lahiri",

        "ayanamsa_system":
            "Lahiri",

        "ascendant":
            ascendant,

        "planets":
            planets,

        "houses":
            houses,

        "house_planets":
            house_planets,

        "dasha":
            dasha,

        "yogas":
            yogas

    }


    # =====================================================
    # SAFETY CHECK
    # =====================================================

    if not result.get(
        "ascendant"
    ):

        raise ValueError(
            "Ascendant calculation failed."
        )


    if not result.get(
        "planets"
    ):

        raise ValueError(
            "Planet calculation failed."
        )


    if len(
        result["planets"]
    ) < 9:

        raise ValueError(
            "Not all planets were calculated."
        )


    return result


# =========================================================
# COMPATIBILITY WRAPPER
# =========================================================

def build_kundli(
    date_of_birth,
    time_of_birth,
    latitude,
    longitude,
    timezone_offset
):

    return calculate_kundli(

        date_of_birth=
            date_of_birth,

        time_of_birth=
            time_of_birth,

        latitude=
            latitude,

        longitude=
            longitude,

        timezone_offset=
            timezone_offset

    )