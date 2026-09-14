"""
AI Jyotish - Classical Shadbala Engine

Seven classical planets:
    Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn

Six-fold Shadbala:
    1. Sthana Bala
       - Uccha Bala
       - Saptavargaja Bala
       - Ojayugma Rasyamsha Bala
       - Kendradi Bala
       - Drekkana Bala

    2. Dig Bala

    3. Kala Bala
       - Nathonnatha Bala
       - Paksha Bala
       - Tribhaga Bala
       - Vara Bala
       - Hora Bala
       - Masa Bala
       - Abda Bala
       - Ayana Bala

    4. Cheshta Bala

    5. Naisargika Bala

    6. Drik Bala

All internal strength values are in Shashtiamsas (Virupas).

60 Virupas = 1 Rupa.

This module intentionally keeps the existing public API used
by AI Jyotish so that the frontend/backend integration does
not need to be rewritten.
"""

from datetime import datetime, date
from math import fabs


# ============================================================
# PLANETS
# ============================================================

SHADBALA_PLANETS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
]


# ============================================================
# NATURAL BALA
# ============================================================

NAISARGIKA_BALA = {
    "Sun": 60.00,
    "Moon": 51.43,
    "Mars": 17.14,
    "Mercury": 25.71,
    "Jupiter": 34.29,
    "Venus": 42.86,
    "Saturn": 8.57,
}


# Common classical minimum required Rupas.
#
# These are reference values used for strength-ratio reporting.
# The ranking itself does NOT depend on these values.
MINIMUM_RUPAS = {
    "Sun": 5.0,
    "Moon": 6.0,
    "Mars": 5.0,
    "Mercury": 7.0,
    "Jupiter": 6.5,
    "Venus": 5.5,
    "Saturn": 5.0,
}


# ============================================================
# ZODIAC
# ============================================================

SIGN_NAMES = [
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
    "Pisces",
]


# Exaltation signs.
EXALTATION_SIGNS = {
    "Sun": 0,
    "Moon": 1,
    "Mars": 9,
    "Mercury": 5,
    "Jupiter": 3,
    "Venus": 11,
    "Saturn": 6,
}


# Exact/approximate exaltation degrees.
EXALTATION_DEGREES = {
    "Sun": 10.0,
    "Moon": 33.0,
    "Mars": 298.0,
    "Mercury": 165.0,
    "Jupiter": 95.0,
    "Venus": 357.0,
    "Saturn": 200.0,
}


DEBILITATION_SIGNS = {
    "Sun": 6,
    "Moon": 7,
    "Mars": 3,
    "Mercury": 11,
    "Jupiter": 9,
    "Venus": 5,
    "Saturn": 0,
}


OWN_SIGNS = {
    "Sun": [4],
    "Moon": [3],
    "Mars": [0, 7],
    "Mercury": [2, 5],
    "Jupiter": [8, 11],
    "Venus": [1, 6],
    "Saturn": [9, 10],
}


# Moolatrikona signs.
MOOLATRIKONA_SIGNS = {
    "Sun": 4,
    "Moon": 1,
    "Mars": 0,
    "Mercury": 5,
    "Jupiter": 8,
    "Venus": 6,
    "Saturn": 10,
}


# ============================================================
# TEMPORAL / DIRECTIONAL TABLES
# ============================================================

# Dig Bala strongest point.
DIG_BALA_HOUSE = {
    "Sun": 10,
    "Mars": 10,
    "Moon": 4,
    "Venus": 4,
    "Jupiter": 1,
    "Mercury": 1,
    "Saturn": 7,
}


# Day/night benefic classification used by several Kala
# calculations.
DAY_PLANETS = {
    "Sun",
    "Jupiter",
    "Venus",
}


NIGHT_PLANETS = {
    "Moon",
    "Mars",
    "Saturn",
}


# Hora lords follow the classical Chaldean sequence.
HORA_SEQUENCE = [
    "Sun",
    "Venus",
    "Mercury",
    "Moon",
    "Saturn",
    "Jupiter",
    "Mars",
]


# Vara lords.
WEEKDAY_LORDS = {
    0: "Moon",       # Monday
    1: "Mars",       # Tuesday
    2: "Mercury",    # Wednesday
    3: "Jupiter",    # Thursday
    4: "Venus",      # Friday
    5: "Saturn",     # Saturday
    6: "Sun",        # Sunday
}


# Masa lord sequence used for solar-month style calculation.
# This is kept deterministic when the backend provides a month
# but not a dedicated solar-month lord.
MONTH_LORDS = [
    "Mars",
    "Venus",
    "Mercury",
    "Moon",
    "Sun",
    "Mercury",
    "Venus",
    "Mars",
    "Jupiter",
    "Saturn",
    "Saturn",
    "Jupiter",
]


# Ayana support.
# Sun's northern/southern declination direction is preferred
# differently by different planets.
AYANA_DAY = {
    "Sun",
    "Mars",
    "Jupiter",
    "Mercury",
    "Venus",
}


# ============================================================
# FRIENDSHIP
# ============================================================

PLANETARY_FRIENDS = {
    "Sun": {"Moon", "Mars", "Jupiter"},
    "Moon": {"Sun", "Mercury"},
    "Mars": {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus": {"Mercury", "Saturn"},
    "Saturn": {"Mercury", "Venus"},
}


PLANETARY_ENEMIES = {
    "Sun": {"Venus", "Saturn"},
    "Moon": set(),
    "Mars": {"Mercury"},
    "Mercury": {"Moon"},
    "Jupiter": {"Mercury", "Venus"},
    "Venus": {"Sun", "Moon"},
    "Saturn": {"Sun", "Moon", "Mars"},
}


# ============================================================
# BASIC HELPERS
# ============================================================

def normalize_planet_name(name):
    """Normalize planet names."""

    if not name:
        return None

    aliases = {
        "sun": "Sun",
        "surya": "Sun",

        "moon": "Moon",
        "chandra": "Moon",

        "mars": "Mars",
        "mangal": "Mars",

        "mercury": "Mercury",
        "budha": "Mercury",

        "jupiter": "Jupiter",
        "guru": "Jupiter",

        "venus": "Venus",
        "shukra": "Venus",

        "saturn": "Saturn",
        "shani": "Saturn",
    }

    return aliases.get(str(name).strip().lower())


def clamp(value, minimum=0.0, maximum=60.0):
    """Clamp a value."""

    try:
        value = float(value)
    except (TypeError, ValueError):
        value = minimum

    return max(minimum, min(maximum, value))


def clamp_signed(value, minimum=-60.0, maximum=60.0):
    """Clamp a signed value, useful for Drik Bala."""

    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0.0

    return max(minimum, min(maximum, value))


def normalize_degree(degree):
    """Normalize longitude to 0-360 degrees."""

    try:
        return float(degree) % 360.0
    except (TypeError, ValueError):
        return 0.0


def angular_distance(longitude1, longitude2):
    """Shortest angular distance."""

    a = normalize_degree(longitude1)
    b = normalize_degree(longitude2)

    difference = abs(a - b)

    return min(difference, 360.0 - difference)


def get_house_from_planet(planet):
    """Get house number."""

    if not isinstance(planet, dict):
        return None

    value = planet.get("house")

    if value is None:
        value = planet.get("house_number")

    try:
        value = int(value)
    except (TypeError, ValueError):
        return None

    if 1 <= value <= 12:
        return value

    return None


def get_sign_index(planet):
    """Get 0-based sign index."""

    if not isinstance(planet, dict):
        return None

    value = planet.get("sign_index")

    try:
        value = int(value)
    except (TypeError, ValueError):
        return None

    if 0 <= value <= 11:
        return value

    return None


def get_longitude(planet):
    """Get planetary longitude."""

    if not isinstance(planet, dict):
        return None

    for key in (
        "longitude",
        "sidereal_longitude",
        "degree",
        "absolute_degree",
    ):
        value = planet.get(key)

        if value is not None:
            try:
                return normalize_degree(value)
            except (TypeError, ValueError):
                pass

    return None


def get_speed(planet):
    """Get daily motion/speed if supplied."""

    if not isinstance(planet, dict):
        return None

    for key in (
        "speed",
        "longitude_speed",
        "daily_motion",
        "motion_speed",
    ):
        value = planet.get(key)

        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                pass

    return None


def is_retrograde(planet):
    """Get retrograde state."""

    if not isinstance(planet, dict):
        return False

    value = planet.get("retrograde")

    if isinstance(value, str):
        return value.lower() in (
            "true",
            "yes",
            "retrograde",
            "vakri",
        )

    return bool(value)


# ============================================================
# CHART HELPERS
# ============================================================

def get_chart_value(chart, *keys):
    """Return first available chart value."""

    if not isinstance(chart, dict):
        return None

    for key in keys:
        if key in chart and chart[key] is not None:
            return chart[key]

    return None


def get_chart_datetime(chart):
    """
    Try to obtain birth datetime from common project fields.
    """

    if not isinstance(chart, dict):
        return None

    candidates = [
        chart.get("datetime"),
        chart.get("birth_datetime"),
        chart.get("birthDateTime"),
        chart.get("date_time"),
    ]

    date_value = get_chart_value(
        chart,
        "birth_date",
        "date",
        "dob",
    )

    time_value = get_chart_value(
        chart,
        "birth_time",
        "time",
        "tob",
    )

    if date_value and time_value:
        candidates.append(
            f"{date_value} {time_value}"
        )

    for value in candidates:
        if isinstance(value, datetime):
            return value

        if isinstance(value, str):
            text = value.strip()

            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M",
                "%d-%m-%Y %H:%M:%S",
                "%d-%m-%Y %H:%M",
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(text, fmt)
                except ValueError:
                    pass

    return None


def chart_is_day(chart):
    """Determine day/night when backend already supplies it."""

    if not isinstance(chart, dict):
        return None

    value = get_chart_value(
        chart,
        "is_day",
        "day_birth",
        "dayBirth",
    )

    if value is not None:
        return bool(value)

    return None


# ============================================================
# PLANETARY RELATIONSHIP
# ============================================================

def relationship(planet1, planet2):
    """
    Natural planetary relationship.

    Returns:
        friend
        enemy
        neutral
    """

    if planet1 == planet2:
        return "own"

    if planet2 in PLANETARY_FRIENDS.get(planet1, set()):
        return "friend"

    if planet2 in PLANETARY_ENEMIES.get(planet1, set()):
        return "enemy"

    return "neutral"


def sign_lord(sign_index):
    """Return classical sign lord."""

    if sign_index is None:
        return None

    lords = [
        "Mars",
        "Venus",
        "Mercury",
        "Moon",
        "Sun",
        "Mercury",
        "Venus",
        "Mars",
        "Jupiter",
        "Saturn",
        "Saturn",
        "Jupiter",
    ]

    return lords[sign_index]


# ============================================================
# STHANA BALA
# ============================================================

def calculate_uccha_bala(planet):
    """
    Uccha Bala.

    Maximum = 60.

    Exact exaltation point = 60.
    Debilitation point = 0.
    The value changes according to angular distance from the
    exaltation point.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    if name not in SHADBALA_PLANETS:
        return 0.0

    longitude = get_longitude(planet)

    if longitude is None:
        sign = get_sign_index(planet)

        if sign is None:
            return 30.0

        if sign == EXALTATION_SIGNS[name]:
            return 60.0

        if sign == DEBILITATION_SIGNS[name]:
            return 0.0

        return 30.0

    exaltation_point = EXALTATION_DEGREES[name]

    distance = angular_distance(
        longitude,
        exaltation_point,
    )

    return clamp(
        60.0 - (distance / 180.0 * 60.0)
    )


# ------------------------------------------------------------
# VARGA CALCULATIONS
# ------------------------------------------------------------

def drekkana_sign(sign_index, degree_in_sign):
    """
    D3 sign.

    0-10 degrees:
        same sign

    10-20:
        5th sign from sign

    20-30:
        9th sign from sign
    """

    if sign_index is None:
        return None

    if degree_in_sign < 10.0:
        return sign_index

    if degree_in_sign < 20.0:
        return (sign_index + 4) % 12

    return (sign_index + 8) % 12


def hora_sign(sign_index, degree_in_sign):
    """
    D2/Hora sign.

    Odd signs:
        first half Sun
        second half Moon

    Even signs:
        first half Moon
        second half Sun
    """

    if sign_index is None:
        return None

    odd_sign = (sign_index % 2) == 0

    if odd_sign:
        return 4 if degree_in_sign < 15 else 3

    return 3 if degree_in_sign < 15 else 4


def dwadasamsa_sign(sign_index, degree_in_sign):
    """D12 sign."""

    if sign_index is None:
        return None

    part = int(degree_in_sign / 2.5)

    return (sign_index + part) % 12


def navamsa_sign(sign_index, degree_in_sign):
    """
    D9 sign.

    Movable signs start from same sign.
    Fixed signs start from 9th.
    Dual signs start from 5th.
    """

    if sign_index is None:
        return None

    part = int(degree_in_sign / (30.0 / 9.0))

    movable = {0, 3, 6, 9}
    fixed = {1, 4, 7, 10}

    if sign_index in movable:
        start = sign_index

    elif sign_index in fixed:
        start = (sign_index + 8) % 12

    else:
        start = (sign_index + 4) % 12

    return (start + part) % 12


def saptamsa_sign(sign_index, degree_in_sign):
    """D7 sign."""

    if sign_index is None:
        return None

    part = int(degree_in_sign / (30.0 / 7.0))

    if sign_index % 2 == 0:
        start = sign_index
    else:
        start = (sign_index + 6) % 12

    return (start + part) % 12


def trimsamsa_sign(sign_index, degree_in_sign):
    """
    D30 approximation using classical odd/even sign divisions.
    """

    if sign_index is None:
        return None

    odd = sign_index % 2 == 0

    if odd:
        limits = [
            (5, 0),
            (10, 10),
            (18, 8),
            (25, 6),
            (30, 2),
        ]
    else:
        limits = [
            (5, 1),
            (12, 5),
            (20, 9),
            (25, 3),
            (30, 11),
        ]

    for limit, target in limits:
        if degree_in_sign < limit:
            return target

    return limits[-1][1]


def get_varga_signs(planet):
    """
    Return D1, D2, D3, D7, D9, D12, D30.
    """

    longitude = get_longitude(planet)

    sign_index = get_sign_index(planet)

    if longitude is not None:
        sign_index = int(longitude / 30.0)
        degree_in_sign = longitude % 30.0

    else:
        degree_in_sign = 15.0

    if sign_index is None:
        return []

    return [
        sign_index,
        hora_sign(sign_index, degree_in_sign),
        drekkana_sign(sign_index, degree_in_sign),
        saptamsa_sign(sign_index, degree_in_sign),
        navamsa_sign(sign_index, degree_in_sign),
        dwadasamsa_sign(sign_index, degree_in_sign),
        trimsamsa_sign(sign_index, degree_in_sign),
    ]


def calculate_saptavargaja_bala(planet):
    """
    Saptavargaja Bala.

    Evaluates planetary dignity across the seven Vargas.

    This implementation awards:
        own sign       -> high
        friendly sign -> moderate
        neutral        -> low
        enemy          -> negative
        exaltation     -> maximum
        debilitation   -> minimum

    Maximum contribution is normalized to the traditional
    7-varga positional-strength scale.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    if name not in SHADBALA_PLANETS:
        return 0.0

    vargas = get_varga_signs(planet)

    if not vargas:
        return 30.0

    total = 0.0

    for sign in vargas:

        if sign == EXALTATION_SIGNS[name]:
            total += 8.57
            continue

        if sign == DEBILITATION_SIGNS[name]:
            total += 0.0
            continue

        if sign in OWN_SIGNS[name]:
            total += 5.0
            continue

        lord = sign_lord(sign)

        relation = relationship(name, lord)

        if relation == "friend":
            total += 3.5

        elif relation == "enemy":
            total += 1.0

        else:
            total += 2.5

    return clamp(total)


def calculate_ojayugma_bala(planet):
    """
    Ojayugma Rasyamsha Bala.

    Odd/even sign and divisional position support.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    if name not in SHADBALA_PLANETS:
        return 0.0

    sign = get_sign_index(planet)

    longitude = get_longitude(planet)

    if sign is None:
        return 15.0

    if longitude is not None:
        degree = longitude % 30.0
    else:
        degree = 15.0

    # Odd signs in the 0-based representation:
    # Aries, Gemini, Leo, Libra, Sagittarius, Aquarius.
    odd_sign = sign % 2 == 0

    male_planets = {
        "Sun",
        "Mars",
        "Jupiter",
    }

    female_planets = {
        "Moon",
        "Venus",
    }

    neutral_planets = {
        "Mercury",
        "Saturn",
    }

    score = 15.0

    if name in male_planets:
        if odd_sign:
            score += 15.0
        else:
            score -= 5.0

    elif name in female_planets:
        if not odd_sign:
            score += 15.0
        else:
            score -= 5.0

    elif name in neutral_planets:
        score += 5.0

    # Navamsa parity support.
    nav = navamsa_sign(
        sign,
        degree,
    )

    if nav is not None:
        if (nav % 2 == 0) == odd_sign:
            score += 5.0

    return clamp(score)


def calculate_kendradi_bala(planet):
    """
    Kendradi Bala.

    Kendra:
        1,4,7,10 -> strongest

    Panaphara:
        2,5,8,11 -> medium

    Apoklima:
        3,6,9,12 -> lower
    """

    house = get_house_from_planet(planet)

    if house is None:
        return 30.0

    if house in (1, 4, 7, 10):
        return 60.0

    if house in (2, 5, 8, 11):
        return 30.0

    return 15.0


def calculate_drekkana_bala(planet):
    """
    Drekkana Bala.

    Uses the planet's position in the three decans and
    classical masculine/feminine planetary grouping.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    longitude = get_longitude(planet)

    sign = get_sign_index(planet)

    if longitude is not None:
        sign = int(longitude / 30.0)
        degree = longitude % 30.0
    else:
        degree = 15.0

    if sign is None:
        return 10.0

    decan = int(degree / 10.0)

    # Classical three-decan support.
    masculine = {
        "Sun",
        "Mars",
        "Jupiter",
    }

    feminine = {
        "Moon",
        "Venus",
    }

    if name in masculine:
        preferred = 0
    elif name in feminine:
        preferred = 1
    else:
        preferred = 2

    if decan == preferred:
        return 15.0

    return 7.5


def calculate_sthana_bala(planet):
    """
    Complete Sthana Bala.

    Sum of:
        Uccha
        Saptavargaja
        Ojayugma
        Kendradi
        Drekkana
    """

    values = {
        "uccha_bala": calculate_uccha_bala(planet),
        "saptavargaja_bala": calculate_saptavargaja_bala(planet),
        "ojayugma_bala": calculate_ojayugma_bala(planet),
        "kendradi_bala": calculate_kendradi_bala(planet),
        "drekkana_bala": calculate_drekkana_bala(planet),
    }

    return round(
        sum(values.values()),
        2,
    )


# ============================================================
# DIG BALA
# ============================================================

def calculate_dig_bala(planet):
    """
    Directional strength.

    60 Virupas at the planet's strongest direction and
    progressively less according to angular distance.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    if name not in SHADBALA_PLANETS:
        return 0.0

    longitude = get_longitude(planet)

    house = get_house_from_planet(planet)

    if longitude is not None:
        # House center approximation is used when only longitude
        # and whole-sign houses are available.
        house_degree = (
            ((house - 1) * 30.0) + 15.0
            if house
            else 15.0
        )

        preferred_house = DIG_BALA_HOUSE[name]

        preferred_degree = (
            (preferred_house - 1) * 30.0
        ) + 15.0

        distance = angular_distance(
            longitude,
            preferred_degree,
        )

        return round(
            clamp(
                60.0 - (distance / 180.0 * 60.0)
            ),
            2,
        )

    if house is None:
        return 30.0

    preferred = DIG_BALA_HOUSE[name]

    difference = abs(
        house - preferred
    )

    difference = min(
        difference,
        12 - difference,
    )

    return round(
        clamp(
            60.0 - difference * 10.0
        ),
        2,
    )


# ============================================================
# KALA BALA
# ============================================================

def calculate_nathonnatha_bala(planet, chart=None):
    """
    Nathonnatha Bala.

    Day planets gain strength during daytime.
    Night planets gain strength during nighttime.

    The Sun/Moon receive the strongest day/night distinction.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    day = chart_is_day(chart)

    if day is None:
        return 30.0

    if day:
        if name in DAY_PLANETS:
            return 60.0
        if name in NIGHT_PLANETS:
            return 0.0
        return 30.0

    if name in NIGHT_PLANETS:
        return 60.0

    if name in DAY_PLANETS:
        return 0.0

    return 30.0


def calculate_paksha_bala(planet, planets=None):
    """
    Paksha Bala based on angular separation between Sun and Moon.

    Benefic waxing/waning strength is evaluated from lunar phase.

    Moon receives the strongest phase contribution.
    Other planets receive a corresponding half-phase support.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    if not planets:
        return 30.0

    sun = None
    moon = None

    for item in planets:
        if not isinstance(item, dict):
            continue

        pname = normalize_planet_name(
            item.get("name")
        )

        if pname == "Sun":
            sun = item

        elif pname == "Moon":
            moon = item

    if not sun or not moon:
        return 30.0

    sun_lon = get_longitude(sun)
    moon_lon = get_longitude(moon)

    if sun_lon is None or moon_lon is None:
        return 30.0

    elongation = (
        normalize_degree(moon_lon - sun_lon)
    )

    # 0 at Amavasya, 180 at Purnima.
    phase_strength = (
        elongation / 180.0
        if elongation <= 180.0
        else (360.0 - elongation) / 180.0
    )

    phase_strength = clamp(
        phase_strength,
        0.0,
        1.0,
    )

    # Moon gets up to 60.
    if name == "Moon":
        return round(
            phase_strength * 60.0,
            2,
        )

    benefics = {
        "Jupiter",
        "Venus",
        "Mercury",
    }

    malefics = {
        "Sun",
        "Mars",
        "Saturn",
    }

    if name in benefics:
        return round(
            30.0 + phase_strength * 30.0,
            2,
        )

    if name in malefics:
        return round(
            60.0 - phase_strength * 30.0,
            2,
        )

    return 30.0


def calculate_tribhaga_bala(planet, chart=None):
    """
    Tribhaga Bala.

    Divides day/night into three sections.

    Uses birth hour when exact sunrise/sunset information is
    not available from the chart.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    dt = get_chart_datetime(chart)

    if dt is None:
        return 30.0

    hour = dt.hour + (
        dt.minute / 60.0
    )

    day = chart_is_day(chart)

    if day is None:
        day = 6.0 <= hour < 18.0

    if day:
        part = int(
            max(
                0,
                min(
                    2,
                    (hour - 6.0) / 4.0,
                ),
            )
        )

        lords = [
            "Mercury",
            "Sun",
            "Jupiter",
        ]

    else:
        part = int(
            max(
                0,
                min(
                    2,
                    ((hour - 18.0) % 12.0) / 4.0,
                ),
            )
        )

        lords = [
            "Moon",
            "Venus",
            "Mars",
        ]

    lord = lords[part]

    if name == lord:
        return 60.0

    if relationship(
        name,
        lord,
    ) == "friend":
        return 30.0

    return 15.0


def calculate_vara_bala(planet, chart=None):
    """
    Vara Bala.

    Birth weekday lord gets maximum support.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    dt = get_chart_datetime(chart)

    if dt is None:
        weekday = get_chart_value(
            chart,
            "weekday",
            "day_of_week",
        )

        try:
            weekday = int(weekday)
        except (TypeError, ValueError):
            return 8.57

    else:
        # Python:
        # Monday=0 ... Sunday=6
        weekday = dt.weekday()

    lord = WEEKDAY_LORDS.get(
        weekday
    )

    if name == lord:
        return 45.0

    if relationship(
        name,
        lord,
    ) == "friend":
        return 20.0

    return 10.0


def calculate_hora_bala(planet, chart=None):
    """
    Hora Bala.

    Uses local birth time when available.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    dt = get_chart_datetime(chart)

    if dt is None:
        return 30.0

    weekday = dt.weekday()

    day_lord = WEEKDAY_LORDS[weekday]

    # Sunrise assumed at 6:00 when exact sunrise isn't supplied.
    hour_from_sunrise = (
        dt.hour
        + dt.minute / 60.0
        - 6.0
    )

    hora_number = int(
        hour_from_sunrise % 24
    )

    # First hora of Sunday is Sun.
    day_lord_index = HORA_SEQUENCE.index(
        day_lord
    )

    hora_lord = HORA_SEQUENCE[
        (day_lord_index + hora_number) % 7
    ]

    if name == hora_lord:
        return 60.0

    if relationship(
        name,
        hora_lord,
    ) == "friend":
        return 30.0

    return 15.0


def calculate_masa_bala(planet, chart=None):
    """
    Masa Bala.

    Uses month information when supplied.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    dt = get_chart_datetime(chart)

    if dt is not None:
        month = dt.month
    else:
        month = get_chart_value(
            chart,
            "month",
            "birth_month",
        )

        try:
            month = int(month)
        except (TypeError, ValueError):
            return 30.0

    month = max(
        1,
        min(
            12,
            month,
        ),
    )

    lord = MONTH_LORDS[
        month - 1
    ]

    if name == lord:
        return 30.0

    if relationship(
        name,
        lord,
    ) == "friend":
        return 20.0

    return 10.0


def calculate_abda_bala(planet, chart=None):
    """
    Abda Bala.

    Uses birth year cycle when exact traditional year-lord
    information is not available.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    dt = get_chart_datetime(chart)

    if dt is None:
        return 30.0

    year = dt.year

    # 60-year cycle approximation.
    cycle_index = (
        year - 1
    ) % 60

    lord = SHADBALA_PLANETS[
        cycle_index % 7
    ]

    if name == lord:
        return 30.0

    if relationship(
        name,
        lord,
    ) == "friend":
        return 20.0

    return 10.0


def calculate_ayana_bala(planet, chart=None):
    """
    Ayana Bala.

    Uses solar declination when available.

    If declination isn't supplied, falls back to Sun's
    sidereal longitude.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    sun = None

    if isinstance(chart, dict):
        candidate = chart.get("sun")

        if isinstance(candidate, dict):
            sun = candidate

    if sun is None:
        return 30.0

    sun_longitude = get_longitude(sun)

    if sun_longitude is None:
        return 30.0

    # Northern half roughly corresponds to Aries->Virgo.
    northern = (
        0.0 <= sun_longitude < 180.0
    )

    if name in {
        "Sun",
        "Jupiter",
        "Venus",
    }:
        preferred = northern
    else:
        preferred = not northern

    return 45.0 if preferred else 15.0


def calculate_yuddha_bala(planet, planets=None):
    """
    Planetary-war support.

    When no close conjunction exists, neutral 0 contribution.

    A victorious planet receives positive support while the
    defeated planet receives negative support.

    This value is kept separate and small to avoid distorting
    the other Kala Bala components.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    longitude = get_longitude(planet)

    if longitude is None or not planets:
        return 0.0

    eligible = {
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
    }

    if name not in eligible:
        return 0.0

    for other in planets:

        if not isinstance(other, dict):
            continue

        other_name = normalize_planet_name(
            other.get("name")
        )

        if other_name not in eligible:
            continue

        if other_name == name:
            continue

        other_longitude = get_longitude(other)

        if other_longitude is None:
            continue

        distance = angular_distance(
            longitude,
            other_longitude,
        )

        # Planetary war is only considered at close conjunction.
        if distance <= 1.0:

            speed1 = get_speed(planet)
            speed2 = get_speed(other)

            if speed1 is not None and speed2 is not None:

                if abs(speed1) > abs(speed2):
                    return 5.0

                return -5.0

            return 0.0

    return 0.0


def calculate_kala_bala(planet, chart=None, planets=None):
    """
    Complete Kala Bala.

    Includes:
        Nathonnatha
        Paksha
        Tribhaga
        Vara
        Hora
        Masa
        Abda
        Ayana
        Yuddha

    Values are normalized to a 0-60 component range for
    compatibility with the existing six-component output.
    """

    values = [
        calculate_nathonnatha_bala(
            planet,
            chart,
        ),

        calculate_paksha_bala(
            planet,
            planets,
        ),

        calculate_tribhaga_bala(
            planet,
            chart,
        ),

        calculate_vara_bala(
            planet,
            chart,
        ),

        calculate_hora_bala(
            planet,
            chart,
        ),

        calculate_masa_bala(
            planet,
            chart,
        ),

        calculate_abda_bala(
            planet,
            chart,
        ),

        calculate_ayana_bala(
            planet,
            chart,
        ),
    ]

    yuddha = calculate_yuddha_bala(
        planet,
        planets,
    )

    # Average the Kala subcomponents instead of allowing the
    # number of subcomponents to artificially create a value
    # greater than 60.
    score = (
        sum(values) / len(values)
    )

    score += yuddha

    return round(
        clamp(score),
        2,
    )


# ============================================================
# CHESHTA BALA
# ============================================================

def calculate_cheshta_bala(planet):
    """
    Motional strength.

    Uses actual planetary speed when supplied.

    Retrograde motion receives high motional strength.

    Sun and Moon are handled separately because they don't
    undergo ordinary retrograde motion.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    if name not in SHADBALA_PLANETS:
        return 0.0

    if is_retrograde(planet):
        return 60.0

    speed = get_speed(planet)

    if speed is None:
        if name in (
            "Sun",
            "Moon",
        ):
            return 30.0

        return 30.0

    absolute_speed = abs(speed)

    # Approximate speed normalization.
    #
    # This is deliberately smooth instead of assigning one
    # fixed value to every direct planet.
    reference_speeds = {
        "Mercury": 2.0,
        "Venus": 1.2,
        "Mars": 0.7,
        "Jupiter": 0.2,
        "Saturn": 0.1,
        "Sun": 1.0,
        "Moon": 13.2,
    }

    reference = reference_speeds.get(
        name,
        1.0,
    )

    if reference <= 0:
        return 30.0

    ratio = absolute_speed / reference

    ratio = max(
        0.0,
        min(
            2.0,
            ratio,
        ),
    )

    score = 15.0 + (
        ratio * 22.5
    )

    return round(
        clamp(score),
        2,
    )


# ============================================================
# NAISARGIKA BALA
# ============================================================

def calculate_naisargika_bala(planet):
    """Return natural strength."""

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    return round(
        NAISARGIKA_BALA.get(
            name,
            0.0,
        ),
        2,
    )


# ============================================================
# DRIK BALA
# ============================================================

def get_aspect_houses(
    planet_name,
    source_house,
):
    """
    Classical Parashari aspect houses.

    Returned values are absolute house numbers.
    """

    if source_house is None:
        return []

    aspects = [
        7,
    ]

    if planet_name == "Mars":
        aspects.extend([
            4,
            8,
        ])

    elif planet_name == "Jupiter":
        aspects.extend([
            5,
            9,
        ])

    elif planet_name == "Saturn":
        aspects.extend([
            3,
            10,
        ])

    result = []

    for aspect in aspects:
        target = (
            (source_house - 1)
            + (aspect - 1)
        ) % 12 + 1

        result.append(target)

    return result


def calculate_drik_bala(planet, planets=None):
    """
    Aspectual strength.

    Classical Drik Bala is signed:
        benefic aspects -> positive
        malefic aspects -> negative

    Unlike the previous implementation, the result is NOT
    artificially forced into 0-60.
    """

    name = normalize_planet_name(
        planet.get("name")
        if isinstance(planet, dict)
        else None
    )

    if name not in SHADBALA_PLANETS:
        return 0.0

    if not planets:
        return 0.0

    target_house = get_house_from_planet(
        planet
    )

    if target_house is None:
        return 0.0

    benefics = {
        "Jupiter",
        "Venus",
        "Mercury",
        "Moon",
    }

    malefics = {
        "Sun",
        "Mars",
        "Saturn",
    }

    score = 0.0

    for other in planets:

        if not isinstance(other, dict):
            continue

        other_name = normalize_planet_name(
            other.get("name")
        )

        if other_name not in SHADBALA_PLANETS:
            continue

        if other_name == name:
            continue

        source_house = get_house_from_planet(
            other
        )

        if source_house is None:
            continue

        aspect_houses = get_aspect_houses(
            other_name,
            source_house,
        )

        if target_house not in aspect_houses:
            continue

        # Signed aspect contribution.
        if other_name in benefics:
            score += 15.0

        elif other_name in malefics:
            score -= 15.0

    return round(
        clamp_signed(
            score,
            -60.0,
            60.0,
        ),
        2,
    )


# ============================================================
# COMPLETE COMPONENTS
# ============================================================

def calculate_sthana_breakdown(planet):
    """Return detailed Sthana Bala components."""

    return {
        "uccha_bala": round(
            calculate_uccha_bala(planet),
            2,
        ),

        "saptavargaja_bala": round(
            calculate_saptavargaja_bala(planet),
            2,
        ),

        "ojayugma_bala": round(
            calculate_ojayugma_bala(planet),
            2,
        ),

        "kendradi_bala": round(
            calculate_kendradi_bala(planet),
            2,
        ),

        "drekkana_bala": round(
            calculate_drekkana_bala(planet),
            2,
        ),
    }


def calculate_kala_breakdown(
    planet,
    chart=None,
    planets=None,
):
    """Return detailed Kala Bala components."""

    return {
        "nathonnatha_bala": round(
            calculate_nathonnatha_bala(
                planet,
                chart,
            ),
            2,
        ),

        "paksha_bala": round(
            calculate_paksha_bala(
                planet,
                planets,
            ),
            2,
        ),

        "tribhaga_bala": round(
            calculate_tribhaga_bala(
                planet,
                chart,
            ),
            2,
        ),

        "vara_bala": round(
            calculate_vara_bala(
                planet,
                chart,
            ),
            2,
        ),

        "hora_bala": round(
            calculate_hora_bala(
                planet,
                chart,
            ),
            2,
        ),

        "masa_bala": round(
            calculate_masa_bala(
                planet,
                chart,
            ),
            2,
        ),

        "abda_bala": round(
            calculate_abda_bala(
                planet,
                chart,
            ),
            2,
        ),

        "ayana_bala": round(
            calculate_ayana_bala(
                planet,
                chart,
            ),
            2,
        ),

        "yuddha_bala": round(
            calculate_yuddha_bala(
                planet,
                planets,
            ),
            2,
        ),
    }


def calculate_shadbala_components(
    planet,
    planets=None,
    chart=None,
):
    """
    Calculate all six Shadbala components.

    Existing API preserved.
    """

    sthana = calculate_sthana_bala(
        planet
    )

    dig = calculate_dig_bala(
        planet
    )

    kala = calculate_kala_bala(
        planet,
        chart=chart,
        planets=planets,
    )

    cheshta = calculate_cheshta_bala(
        planet
    )

    naisargika = calculate_naisargika_bala(
        planet
    )

    drik = calculate_drik_bala(
        planet,
        planets,
    )

    return {
        "sthana_bala": round(
            sthana,
            2,
        ),

        "dig_bala": round(
            dig,
            2,
        ),

        "kala_bala": round(
            kala,
            2,
        ),

        "cheshta_bala": round(
            cheshta,
            2,
        ),

        "naisargika_bala": round(
            naisargika,
            2,
        ),

        "drik_bala": round(
            drik,
            2,
        ),
    }


# ============================================================
# TOTAL
# ============================================================

def calculate_total_shadbala(components):
    """Total six-fold Shadbala in Virupas."""

    if not isinstance(components, dict):
        return 0.0

    keys = [
        "sthana_bala",
        "dig_bala",
        "kala_bala",
        "cheshta_bala",
        "naisargika_bala",
        "drik_bala",
    ]

    total = 0.0

    for key in keys:

        try:
            total += float(
                components.get(
                    key,
                    0.0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):
            pass

    return round(
        total,
        2,
    )


def shashtiamsa_to_rupa(value):
    """60 Virupas = 1 Rupa."""

    try:
        return round(
            float(value) / 60.0,
            2,
        )

    except (
        TypeError,
        ValueError,
    ):
        return 0.0


# ============================================================
# STRENGTH RATIO
# ============================================================

def get_strength_ratio(
    planet_name,
    rupas,
):
    """
    Shadbala / minimum required Shadbala.
    """

    name = normalize_planet_name(
        planet_name
    )

    try:
        rupas = float(rupas)
    except (
        TypeError,
        ValueError,
    ):
        return 0.0

    minimum = MINIMUM_RUPAS.get(
        name,
        5.0,
    )

    if minimum <= 0:
        return 0.0

    return round(
        rupas / minimum,
        2,
    )


# ============================================================
# PLANET ANALYSIS
# ============================================================

def analyze_planet_shadbala(
    planet,
    planets=None,
    chart=None,
):
    """Complete Shadbala analysis for one planet."""

    if not isinstance(planet, dict):
        return None

    name = normalize_planet_name(
        planet.get("name")
    )

    if name not in SHADBALA_PLANETS:
        return None

    components = calculate_shadbala_components(
        planet,
        planets=planets,
        chart=chart,
    )

    total = calculate_total_shadbala(
        components
    )

    rupas = shashtiamsa_to_rupa(
        total
    )

    minimum = MINIMUM_RUPAS.get(
        name,
        5.0,
    )

    ratio = get_strength_ratio(
        name,
        rupas,
    )

    return {
        "planet": name,

        "components": components,

        "sthana_breakdown":
            calculate_sthana_breakdown(
                planet
            ),

        "kala_breakdown":
            calculate_kala_breakdown(
                planet,
                chart=chart,
                planets=planets,
            ),

        "total_shashtiamsas": total,

        "total_rupas": rupas,

        "minimum_required_rupas":
            minimum,

        "strength_ratio":
            ratio,

        "retrograde":
            is_retrograde(planet),
    }


def analyze_planets_shadbala(
    planets,
    chart=None,
):
    """Analyze all seven classical planets."""

    if not planets:
        return []

    results = []

    for planet in planets:

        if not isinstance(
            planet,
            dict,
        ):
            continue

        name = normalize_planet_name(
            planet.get("name")
        )

        if name not in SHADBALA_PLANETS:
            continue

        result = analyze_planet_shadbala(
            planet,
            planets=planets,
            chart=chart,
        )

        if result:
            results.append(result)

    return results


# ============================================================
# ENRICH PLANETS
# ============================================================

def enrich_planets_with_shadbala(
    planets,
    chart=None,
):
    """Add Shadbala data to planet objects."""

    if not planets:
        return []

    analyses = analyze_planets_shadbala(
        planets,
        chart=chart,
    )

    analysis_map = {
        item["planet"]: item
        for item in analyses
    }

    enriched = []

    for planet in planets:

        if not isinstance(
            planet,
            dict,
        ):
            enriched.append(planet)
            continue

        new_planet = dict(
            planet
        )

        name = normalize_planet_name(
            planet.get("name")
        )

        analysis = analysis_map.get(
            name
        )

        if analysis:
            new_planet["shadbala"] = analysis

        enriched.append(
            new_planet
        )

    return enriched


# ============================================================
# RANKING
# ============================================================

def rank_shadbala_planets(analyses):
    """
    Rank planets from strongest to weakest.

    Ranking uses strength ratio first and total Rupas as
    secondary ordering.
    """

    if not analyses:
        return []

    ordered = sorted(
        analyses,
        key=lambda item: (
            float(
                item.get(
                    "strength_ratio",
                    0.0,
                )
            ),
            float(
                item.get(
                    "total_rupas",
                    0.0,
                )
            ),
        ),
        reverse=True,
    )

    ranked = []

    for rank, item in enumerate(
        ordered,
        start=1,
    ):

        row = dict(item)

        row["rank"] = rank

        ranked.append(row)

    return ranked


# ============================================================
# LEGACY FILTER COMPATIBILITY
# ============================================================

def get_strong_planets_by_shadbala(
    analyses,
):
    """
    Kept for compatibility.

    Uses the upper half of the ranking instead of the old
    Strong/Very Strong classification system.
    """

    ranked = rank_shadbala_planets(
        analyses
    )

    return [
        item
        for item in ranked
        if item.get("rank", 99) <= 3
    ]


def get_weak_planets_by_shadbala(
    analyses,
):
    """
    Kept for compatibility.

    Returns lower-ranked planets.
    """

    ranked = rank_shadbala_planets(
        analyses
    )

    return [
        item
        for item in ranked
        if item.get("rank", 0) >= 5
    ]


def get_very_strong_planets(
    analyses,
):
    """Compatibility helper: rank #1."""

    ranked = rank_shadbala_planets(
        analyses
    )

    return [
        item
        for item in ranked
        if item.get("rank") == 1
    ]


def get_very_weak_planets(
    analyses,
):
    """Compatibility helper: rank #7."""

    ranked = rank_shadbala_planets(
        analyses
    )

    return [
        item
        for item in ranked
        if item.get("rank") == 7
    ]


# ============================================================
# SUMMARY
# ============================================================

def build_shadbala_summary(
    analyses,
):
    """Build Shadbala summary."""

    if not analyses:
        return {
            "strongest_planet": None,
            "weakest_planet": None,
            "average_rupas": 0.0,
            "planet_count": 0,
        }

    ranked = rank_shadbala_planets(
        analyses
    )

    average = (
        sum(
            float(
                item.get(
                    "total_rupas",
                    0.0,
                )
            )
            for item in analyses
        )
        / len(analyses)
    )

    return {
        "strongest_planet":
            ranked[0]["planet"]
            if ranked
            else None,

        "weakest_planet":
            ranked[-1]["planet"]
            if ranked
            else None,

        "average_rupas":
            round(
                average,
                2,
            ),

        "planet_count":
            len(analyses),
    }


# ============================================================
# TABLE
# ============================================================

def build_shadbala_table(
    analyses,
):
    """
    Build frontend-friendly ranked table.

    No Weak / Very Weak classification is returned.
    """

    ranked = rank_shadbala_planets(
        analyses
    )

    table = []

    for item in ranked:

        components = item.get(
            "components",
            {},
        )

        table.append({
            "rank":
                item.get(
                    "rank",
                    0,
                ),

            "planet":
                item.get(
                    "planet"
                ),

            "sthana_bala":
                components.get(
                    "sthana_bala",
                    0.0,
                ),

            "dig_bala":
                components.get(
                    "dig_bala",
                    0.0,
                ),

            "kala_bala":
                components.get(
                    "kala_bala",
                    0.0,
                ),

            "cheshta_bala":
                components.get(
                    "cheshta_bala",
                    0.0,
                ),

            "naisargika_bala":
                components.get(
                    "naisargika_bala",
                    0.0,
                ),

            "drik_bala":
                components.get(
                    "drik_bala",
                    0.0,
                ),

            "total_shashtiamsas":
                item.get(
                    "total_shashtiamsas",
                    0.0,
                ),

            "total_rupas":
                item.get(
                    "total_rupas",
                    0.0,
                ),

            "strength_ratio":
                item.get(
                    "strength_ratio",
                    0.0,
                ),
        })

    return table


# ============================================================
# COMPLETE ANALYSIS
# ============================================================

def build_shadbala_analysis(
    planets,
    chart=None,
):
    """
    Build complete Shadbala analysis.

    Public return structure remains compatible with the
    existing AI Jyotish backend.
    """

    analyses = analyze_planets_shadbala(
        planets,
        chart=chart,
    )

    ranked = rank_shadbala_planets(
        analyses
    )

    return {
        "planets":
            analyses,

        "summary":
            build_shadbala_summary(
                analyses
            ),

        "strong_planets":
            [
                item["planet"]
                for item in get_strong_planets_by_shadbala(
                    analyses
                )
            ],

        "weak_planets":
            [
                item["planet"]
                for item in get_weak_planets_by_shadbala(
                    analyses
                )
            ],

        "table":
            build_shadbala_table(
                analyses
            ),
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 80)
    print("AI JYOTISH - CLASSICAL SHADBALA TEST")
    print("=" * 80)

    sample_planets = [
        {
            "name": "Sun",
            "sign_index": 0,
            "longitude": 15.0,
            "house": 10,
            "retrograde": False,
            "speed": 0.98,
        },
        {
            "name": "Moon",
            "sign_index": 1,
            "longitude": 45.0,
            "house": 4,
            "retrograde": False,
            "speed": 13.2,
        },
        {
            "name": "Mars",
            "sign_index": 9,
            "longitude": 280.0,
            "house": 10,
            "retrograde": False,
            "speed": 0.65,
        },
        {
            "name": "Mercury",
            "sign_index": 5,
            "longitude": 165.0,
            "house": 1,
            "retrograde": False,
            "speed": 1.5,
        },
        {
            "name": "Jupiter",
            "sign_index": 3,
            "longitude": 100.0,
            "house": 1,
            "retrograde": False,
            "speed": 0.15,
        },
        {
            "name": "Venus",
            "sign_index": 11,
            "longitude": 345.0,
            "house": 4,
            "retrograde": False,
            "speed": 1.0,
        },
        {
            "name": "Saturn",
            "sign_index": 6,
            "longitude": 200.0,
            "house": 7,
            "retrograde": True,
            "speed": -0.05,
        },
    ]

    chart = {
        "is_day": True,
        "birth_date": "2002-05-11",
        "birth_time": "14:30",
    }

    result = build_shadbala_analysis(
        sample_planets,
        chart=chart,
    )

    print()
    print(
        f"{'RANK':<6}"
        f"{'PLANET':<10}"
        f"{'STHANA':>10}"
        f"{'DIG':>10}"
        f"{'KALA':>10}"
        f"{'CHESHTA':>10}"
        f"{'NAIS':>10}"
        f"{'DRIK':>10}"
        f"{'TOTAL':>12}"
        f"{'RUPAS':>10}"
    )

    print("-" * 98)

    for row in result["table"]:

        print(
            f"{row['rank']:<6}"
            f"{row['planet']:<10}"
            f"{row['sthana_bala']:>10.2f}"
            f"{row['dig_bala']:>10.2f}"
            f"{row['kala_bala']:>10.2f}"
            f"{row['cheshta_bala']:>10.2f}"
            f"{row['naisargika_bala']:>10.2f}"
            f"{row['drik_bala']:>10.2f}"
            f"{row['total_shashtiamsas']:>12.2f}"
            f"{row['total_rupas']:>10.2f}"
        )

    print()
    print(
        "Strongest:",
        result["summary"]["strongest_planet"],
    )

    print(
        "Weakest:",
        result["summary"]["weakest_planet"],
    )

    print(
        "Average Rupas:",
        result["summary"]["average_rupas"],
    )

    print()
    print("=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)