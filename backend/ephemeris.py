import swisseph as swe
from datetime import datetime, timezone, timedelta


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
# HELPERS
# =========================================================

def normalize_degree(degree):
    return float(degree) % 360


def get_sign(longitude):

    longitude = normalize_degree(longitude)

    sign_index = int(longitude // 30)

    degree_in_sign = longitude % 30

    return {
        "name": ZODIAC_SIGNS[sign_index],
        "vedic_name": ZODIAC_SIGNS_HINDI[sign_index],
        "index": sign_index,
        "degree": round(degree_in_sign, 2)
    }


def get_nakshatra(longitude):

    longitude = normalize_degree(longitude)

    nakshatra_size = 360 / 27

    index = int(longitude // nakshatra_size)

    degree_inside = longitude % nakshatra_size

    pada_size = nakshatra_size / 4

    pada = int(degree_inside // pada_size) + 1

    if pada > 4:
        pada = 4

    return {
        "name": NAKSHATRAS[index],
        "index": index,
        "pada": pada
    }


# =========================================================
# PLANET POSITION
# =========================================================

def get_planet_position(planet_id, julian_day):

    flags = (
        swe.FLG_SWIEPH
        | swe.FLG_SIDEREAL
        | swe.FLG_SPEED
    )

    result = swe.calc_ut(
        julian_day,
        planet_id,
        flags
    )

    values = result[0]

    longitude = normalize_degree(values[0])

    speed = float(values[3])

    return longitude, speed


# =========================================================
# MAIN CALCULATION
# =========================================================

def calculate_kundli(
    date_of_birth,
    time_of_birth,
    latitude,
    longitude,
    timezone_offset
):

    swe.set_sid_mode(
        swe.SIDM_LAHIRI
    )

    # -----------------------------------------------------
    # LOCAL TIME
    # -----------------------------------------------------

    local_datetime = datetime.strptime(
        f"{date_of_birth} {time_of_birth}",
        "%Y-%m-%d %H:%M"
    )

    # -----------------------------------------------------
    # UTC
    # -----------------------------------------------------

    offset = timedelta(
        hours=float(timezone_offset)
    )

    utc_datetime = (
        local_datetime - offset
    )

    utc_datetime = utc_datetime.replace(
        tzinfo=timezone.utc
    )

    # -----------------------------------------------------
    # JULIAN DAY
    # -----------------------------------------------------

    hour_decimal = (
        utc_datetime.hour
        + utc_datetime.minute / 60
        + utc_datetime.second / 3600
    )

    julian_day = swe.julday(
        utc_datetime.year,
        utc_datetime.month,
        utc_datetime.day,
        hour_decimal
    )

    # -----------------------------------------------------
    # PLANETS
    # -----------------------------------------------------

    planets = {}

    for planet_name, planet_id in PLANETS.items():

        longitude_value, speed = (
            get_planet_position(
                planet_id,
                julian_day
            )
        )

        sign = get_sign(
            longitude_value
        )

        nakshatra = get_nakshatra(
            longitude_value
        )

        planets[planet_name] = {
            "longitude": round(
                longitude_value,
                4
            ),
            "degree": sign["degree"],
            "sign": sign["name"],
            "vedic_sign": sign["vedic_name"],
            "nakshatra": nakshatra["name"],
            "nakshatra_pada": nakshatra["pada"],
            "retrograde": speed < 0
        }

    # -----------------------------------------------------
    # KETU
    # -----------------------------------------------------

    rahu_longitude = planets["Rahu"]["longitude"]

    ketu_longitude = normalize_degree(
        rahu_longitude + 180
    )

    ketu_sign = get_sign(
        ketu_longitude
    )

    ketu_nakshatra = get_nakshatra(
        ketu_longitude
    )

    planets["Ketu"] = {
        "longitude": round(
            ketu_longitude,
            4
        ),
        "degree": ketu_sign["degree"],
        "sign": ketu_sign["name"],
        "vedic_sign": ketu_sign["vedic_name"],
        "nakshatra": ketu_nakshatra["name"],
        "nakshatra_pada": ketu_nakshatra["pada"],
        "retrograde": True
    }

    # -----------------------------------------------------
    # ASCENDANT
    # -----------------------------------------------------

    houses, ascmc = swe.houses_ex(
        julian_day,
        float(latitude),
        float(longitude),
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
        "longitude": round(
            ascendant_longitude,
            4
        ),
        "degree": ascendant_sign["degree"],
        "sign": ascendant_sign["name"],
        "vedic_sign": ascendant_sign["vedic_name"],
        "nakshatra": ascendant_nakshatra["name"],
        "nakshatra_pada": ascendant_nakshatra["pada"]
    }

    # -----------------------------------------------------
    # HOUSES
    # -----------------------------------------------------

    house_data = []

    for i in range(12):

        house_longitude = normalize_degree(
            houses[i]
        )

        house_sign = get_sign(
            house_longitude
        )

        house_data.append({
            "house": i + 1,
            "longitude": round(
                house_longitude,
                4
            ),
            "sign": house_sign["name"],
            "vedic_sign": house_sign["vedic_name"]
        })

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    return {
        "julian_day": julian_day,
        "utc_time": utc_datetime.isoformat(),
        "ascendant": ascendant,
        "planets": planets,
        "houses": house_data,
        "ayanamsa": "Lahiri"
    }