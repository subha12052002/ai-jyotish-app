# =========================================================
# AI JYOTISH
# ephemeris.py
#
# Swiss Ephemeris
# Lahiri Sidereal Zodiac
# Whole Sign House Support
# =========================================================

from datetime import datetime, timedelta, timezone

import swisseph as swe


# =========================================================
# SIDEREAL SETTINGS
# =========================================================

swe.set_sid_mode(swe.SIDM_LAHIRI)


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
    "Rahu": swe.MEAN_NODE,
}


# =========================================================
# VEDIC SIGNS
# =========================================================

SIGNS = [
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
    "Meena",
]


# =========================================================
# LOCAL TIME → UTC
# =========================================================

def utc_datetime(
    date_string,
    time_string,
    timezone_hours
):
    """
    Convert local birth date/time into UTC.

    Example:
        India UTC+5:30
        14:30 local
        becomes 09:00 UTC
    """

    local_datetime = datetime.strptime(
        f"{date_string} {time_string}",
        "%Y-%m-%d %H:%M"
    )

    offset = timezone(
        timedelta(
            hours=float(timezone_hours)
        )
    )

    local_datetime = local_datetime.replace(
        tzinfo=offset
    )

    return local_datetime.astimezone(
        timezone.utc
    )


# =========================================================
# JULIAN DAY
# =========================================================

def julian_day(
    date_string,
    time_string,
    timezone_hours
):
    """
    Convert birth date/time to Julian Day.
    """

    utc = utc_datetime(
        date_string,
        time_string,
        timezone_hours
    )

    hour = (
        utc.hour
        + utc.minute / 60.0
        + utc.second / 3600.0
        + utc.microsecond / 3600000000.0
    )

    return swe.julday(
        utc.year,
        utc.month,
        utc.day,
        hour
    )


# =========================================================
# LONGITUDE → VEDIC SIGN
# =========================================================

def sign_from_longitude(
    longitude
):
    """
    Convert 0–360 degree longitude into
    Vedic sidereal sign information.
    """

    longitude = float(longitude) % 360.0

    sign_index = int(
        longitude // 30.0
    )

    degree = (
        longitude
        - sign_index * 30.0
    )

    return {
        "sign": SIGNS[sign_index],

        "sign_index": sign_index,

        "degree": round(
            degree,
            4
        ),

        "longitude": round(
            longitude,
            4
        )
    }


# =========================================================
# SAFE SWISS EPHEMERIS CALCULATION
# =========================================================

def calculate_planet_position(
    jd,
    planet_id,
    flags
):
    """
    Calculate a planet using Swiss Ephemeris.

    Important:
    Different pyswisseph versions can return:

        (values, return_flags)

    OR:

        (values, return_flags, warning)

    The version installed on your computer is returning
    three values, which caused:

        too many values to unpack (expected 2)

    Therefore we read the first item as the planetary
    values and safely ignore any additional items.
    """

    result = swe.calc_ut(
        jd,
        planet_id,
        flags
    )

    # -----------------------------------------------------
    # Normal Swiss Ephemeris result
    #
    # Example:
    #
    # (
    #     (
    #         longitude,
    #         latitude,
    #         distance,
    #         speed_longitude,
    #         speed_latitude,
    #         speed_distance
    #     ),
    #     return_flags,
    #     warning
    # )
    # -----------------------------------------------------

    if (
        isinstance(result, tuple)
        and len(result) >= 1
        and isinstance(
            result[0],
            (tuple, list)
        )
    ):
        values = result[0]

        return_flags = None

        if len(result) >= 2:
            return_flags = result[1]

        return values, return_flags

    # -----------------------------------------------------
    # Fallback if the library directly returns values
    # -----------------------------------------------------

    if (
        isinstance(
            result,
            (tuple, list)
        )
        and len(result) >= 4
        and all(
            isinstance(
                value,
                (int, float)
            )
            for value in result
        )
    ):
        return result, None

    # -----------------------------------------------------
    # Unknown format
    # -----------------------------------------------------

    raise RuntimeError(
        "Unexpected Swiss Ephemeris "
        f"calc_ut() result format: {result!r}"
    )


# =========================================================
# CALCULATE PLANETS
# =========================================================

def calculate_planets(
    jd
):
    """
    Calculate all major Vedic planets.

    Uses:
        - Sidereal zodiac
        - Lahiri ayanamsha
        - Moshier ephemeris
        - Planetary speed for retrograde detection
    """

    # -----------------------------------------------------
    # Make sure Lahiri is active
    # -----------------------------------------------------

    swe.set_sid_mode(
        swe.SIDM_LAHIRI
    )

    result = []

    # -----------------------------------------------------
    # FLAGS
    #
    # FLG_MOSEPH avoids requiring external .se1
    # ephemeris files such as sepl_18.se1.
    # -----------------------------------------------------

    flags = (
        swe.FLG_MOSEPH
        | swe.FLG_SIDEREAL
        | swe.FLG_SPEED
    )

    # -----------------------------------------------------
    # PLANETS
    # -----------------------------------------------------

    for name, planet_id in PLANETS.items():

        values, return_flags = (
            calculate_planet_position(
                jd,
                planet_id,
                flags
            )
        )

        # -------------------------------------------------
        # LONGITUDE
        # -------------------------------------------------

        longitude = float(
            values[0]
        )

        # -------------------------------------------------
        # SPEED
        # -------------------------------------------------

        if len(values) >= 4:

            speed = float(
                values[3]
            )

        else:

            speed = 0.0

        # -------------------------------------------------
        # SIGN INFORMATION
        # -------------------------------------------------

        item = sign_from_longitude(
            longitude
        )

        # -------------------------------------------------
        # PLANET INFORMATION
        # -------------------------------------------------

        item.update({

            "name": name,

            "retrograde": (
                speed < 0
            ),

            "speed": round(
                speed,
                6
            )

        })

        result.append(
            item
        )

    # =====================================================
    # KETU
    # =====================================================

    rahu = next(
        planet
        for planet in result
        if planet["name"] == "Rahu"
    )

    # Ketu is exactly opposite Rahu
    ketu_longitude = (
        rahu["longitude"]
        + 180.0
    ) % 360.0

    ketu = sign_from_longitude(
        ketu_longitude
    )

    ketu.update({

        "name": "Ketu",

        # Lunar nodes are normally treated as retrograde
        "retrograde": True,

        "speed": rahu["speed"]

    })

    result.append(
        ketu
    )

    return result


# =========================================================
# ASCENDANT
# =========================================================

def calculate_ascendant(
    jd,
    latitude,
    longitude
):
    """
    Calculate sidereal Ascendant using Swiss Ephemeris.
    """

    # -----------------------------------------------------
    # Lahiri
    # -----------------------------------------------------

    swe.set_sid_mode(
        swe.SIDM_LAHIRI
    )

    # -----------------------------------------------------
    # Houses
    #
    # W = Whole Sign style reference for this application.
    #
    # We use the Ascendant longitude from ascmc[0].
    # -----------------------------------------------------

    result = swe.houses_ex(
        jd,
        float(latitude),
        float(longitude),
        b"W",
        swe.FLG_SIDEREAL
    )

    # -----------------------------------------------------
    # houses_ex normally returns:
    #
    # (cusps, ascmc)
    # -----------------------------------------------------

    if (
        isinstance(result, tuple)
        and len(result) >= 2
    ):

        cusps = result[0]

        ascmc = result[1]

    else:

        raise RuntimeError(
            "Unexpected Swiss Ephemeris "
            "houses_ex() result format."
        )

    # -----------------------------------------------------
    # Ascendant
    # -----------------------------------------------------

    if (
        not isinstance(
            ascmc,
            (tuple, list)
        )
        or len(ascmc) == 0
    ):

        raise RuntimeError(
            "Swiss Ephemeris did not return "
            "a valid Ascendant."
        )

    ascendant_longitude = (
        float(ascmc[0])
        % 360.0
    )

    return sign_from_longitude(
        ascendant_longitude
    )


# =========================================================
# PLANET HOUSE
# =========================================================

def house_from_sign(
    planet_sign_index,
    asc_sign_index
):
    """
    Whole Sign house calculation.

    Ascendant sign = 1st house.
    Next sign = 2nd house.
    etc.
    """

    return (
        (
            int(planet_sign_index)
            - int(asc_sign_index)
        ) % 12
    ) + 1


# =========================================================
# GET PLANET
# =========================================================

def get_planet(
    planets,
    name
):
    """
    Find a planet from the calculated planet list.
    """

    for planet in planets:

        if planet["name"] == name:

            return planet

    return None


# =========================================================
# GET SIGN LORD
# =========================================================

def get_sign_lord(
    sign_index
):
    """
    Traditional Vedic sign lord.
    """

    lords = {

        0: "Mars",       # Mesha

        1: "Venus",      # Vrishabha

        2: "Mercury",    # Mithuna

        3: "Moon",       # Karka

        4: "Sun",        # Simha

        5: "Mercury",    # Kanya

        6: "Venus",      # Tula

        7: "Mars",       # Vrishchika

        8: "Jupiter",    # Dhanu

        9: "Saturn",     # Makara

        10: "Saturn",    # Kumbha

        11: "Jupiter"    # Meena

    }

    return lords.get(
        int(sign_index)
    )


# =========================================================
# GET HOUSE SIGN
# =========================================================

def get_house_sign(
    asc_sign_index,
    house_number
):
    """
    Return the sign occupying a particular
    Whole Sign house.
    """

    sign_index = (
        int(asc_sign_index)
        + int(house_number)
        - 1
    ) % 12

    return {
        "house": int(house_number),

        "sign_index": sign_index,

        "sign": SIGNS[sign_index]
    }


# =========================================================
# GET ALL HOUSES
# =========================================================

def calculate_whole_sign_houses(
    asc_sign_index
):
    """
    Generate all 12 Whole Sign houses.
    """

    houses = []

    for house_number in range(
        1,
        13
    ):

        houses.append(
            get_house_sign(
                asc_sign_index,
                house_number
            )
        )

    return houses