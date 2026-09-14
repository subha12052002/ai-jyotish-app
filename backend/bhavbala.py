"""
AI JYOTISH
Bhava Bala Engine

Classical Bhava Bala is composed of:

1. Bhavadhipati Bala
2. Bhava Dig Bala
3. Bhava Drishti Bala

All values are expressed in Shashtiamsas.
60 Shashtiamsas = 1 Rupa.

This module is intentionally separate from houses.py.
"""


# =========================================================
# CONSTANTS
# =========================================================

SHASTHIAMSA_PER_RUPA = 60.0

HOUSE_COUNT = 12


# =========================================================
# PLANET NORMALIZATION
# =========================================================

def normalize_planet_name(name):
    """
    Normalize common planet names.
    """

    if not isinstance(name, str):
        return ""

    value = name.strip().lower()

    aliases = {
        "sun": "Sun",
        "surya": "Sun",

        "moon": "Moon",
        "chandra": "Moon",

        "mars": "Mars",
        "mangal": "Mars",
        "kuja": "Mars",

        "mercury": "Mercury",
        "budha": "Mercury",

        "jupiter": "Jupiter",
        "guru": "Jupiter",
        "brihaspati": "Jupiter",

        "venus": "Venus",
        "shukra": "Venus",

        "saturn": "Saturn",
        "shani": "Saturn",

        "rahu": "Rahu",
        "ketu": "Ketu",
    }

    return aliases.get(
        value,
        name.strip()
    )


# =========================================================
# SIGN NORMALIZATION
# =========================================================

def get_sign_index(value):
    """
    Convert a sign value to a 0-11 sign index.
    """

    if isinstance(value, int):

        if 0 <= value <= 11:
            return value

        if 1 <= value <= 12:
            return value - 1

    if isinstance(value, float):

        value = int(value)

        if 0 <= value <= 11:
            return value

        if 1 <= value <= 12:
            return value - 1

    if isinstance(value, str):

        names = {
            "aries": 0,
            "taurus": 1,
            "gemini": 2,
            "cancer": 3,
            "leo": 4,
            "virgo": 5,
            "libra": 6,
            "scorpio": 7,
            "sagittarius": 8,
            "capricorn": 9,
            "aquarius": 10,
            "pisces": 11,
        }

        return names.get(
            value.strip().lower()
        )

    return None


# =========================================================
# PLANET → SIGN LORD
# =========================================================

SIGN_LORDS = {
    0: "Mars",       # Aries
    1: "Venus",      # Taurus
    2: "Mercury",    # Gemini
    3: "Moon",       # Cancer
    4: "Sun",        # Leo
    5: "Mercury",    # Virgo
    6: "Venus",      # Libra
    7: "Mars",       # Scorpio
    8: "Jupiter",    # Sagittarius
    9: "Saturn",     # Capricorn
    10: "Saturn",    # Aquarius
    11: "Jupiter",   # Pisces
}


# =========================================================
# EXTRACT PLANET HOUSE
# =========================================================

def get_planet_house(planet):
    """
    Get planetary house number from common chart formats.
    """

    if not isinstance(planet, dict):
        return None

    for key in (
        "house",
        "house_number",
        "bhava",
        "bhava_number",
    ):

        value = planet.get(key)

        if value is not None:

            try:

                value = int(value)

                if 1 <= value <= 12:
                    return value

            except Exception:
                pass

    return None


# =========================================================
# EXTRACT PLANET SIGN
# =========================================================

def get_planet_sign(planet):
    """
    Get planetary sign index.
    """

    if not isinstance(planet, dict):
        return None

    for key in (
        "sign_index",
        "sign",
        "rashi",
        "rashi_index",
    ):

        if key in planet:

            value = get_sign_index(
                planet.get(key)
            )

            if value is not None:
                return value

    return None


# =========================================================
# FIND PLANET
# =========================================================

def find_planet(planets, planet_name):
    """
    Find a planet by normalized name.
    """

    target = normalize_planet_name(
        planet_name
    )

    for planet in planets:

        if not isinstance(
            planet,
            dict
        ):
            continue

        name = normalize_planet_name(
            planet.get(
                "name",
                planet.get(
                    "planet",
                    ""
                )
            )
        )

        if name == target:
            return planet

    return None


# =========================================================
# EXTRACT SHADBALA VALUE
# =========================================================

def get_planet_shadbala(
    shadbala_data,
    planet_name
):
    """
    Extract total Shadbala in Shashtiamsas.

    Supports the table returned by the existing
    Shadbala engine.
    """

    if not shadbala_data:
        return 0.0

    table = shadbala_data

    if isinstance(
        shadbala_data,
        dict
    ):

        table = (
            shadbala_data.get(
                "table",
                shadbala_data.get(
                    "data",
                    []
                )
            )
        )

    if not isinstance(
        table,
        list
    ):
        return 0.0

    target = normalize_planet_name(
        planet_name
    )

    for row in table:

        if not isinstance(
            row,
            dict
        ):
            continue

        name = normalize_planet_name(
            row.get(
                "planet",
                ""
            )
        )

        if name != target:
            continue

        # Preferred: total Shashtiamsas
        for key in (
            "total_shashtiamsas",
            "total_shashtiamsa",
            "total",
        ):

            value = row.get(key)

            if value is not None:

                try:
                    return float(value)

                except Exception:
                    pass

        # Fallback: Rupas
        for key in (
            "total_rupas",
            "rupas",
        ):

            value = row.get(key)

            if value is not None:

                try:

                    return (
                        float(value)
                        * SHASTHIAMSA_PER_RUPA
                    )

                except Exception:
                    pass

    return 0.0


# =========================================================
# BHAVADHIPATI BALA
# =========================================================

def calculate_bhavadhipati_bala(
    house_number,
    ascendant_sign,
    planets,
    shadbala_data
):
    """
    Bhavadhipati Bala:

    Strength of the lord of the sign occupying
    the given house.

    The existing Shadbala total of the house lord
    is used directly.
    """

    try:

        house_number = int(
            house_number
        )

    except Exception:

        return {
            "lord": None,
            "value": 0.0,
        }

    if not (
        1 <= house_number <= 12
    ):

        return {
            "lord": None,
            "value": 0.0,
        }

    ascendant_sign = get_sign_index(
        ascendant_sign
    )

    if ascendant_sign is None:

        return {
            "lord": None,
            "value": 0.0,
        }

    house_sign = (
        ascendant_sign
        + house_number
        - 1
    ) % 12

    lord = SIGN_LORDS.get(
        house_sign
    )

    if lord is None:

        return {
            "lord": None,
            "value": 0.0,
        }

    value = get_planet_shadbala(
        shadbala_data,
        lord
    )

    return {
        "lord": lord,
        "value": round(
            value,
            2
        ),
    }


# =========================================================
# BHAVA DIG BALA
# =========================================================

def calculate_bhava_dig_bala(
    house_number
):
    """
    Directional strength of a Bhava.

    Angular houses are the strongest:
        1st  = 60
        4th  = 60
        7th  = 60
        10th = 60

    Strength decreases according to the traditional
    house relationship to the Kendras.
    """

    house_number = int(
        house_number
    )

    # Kendra
    if house_number in (
        1,
        4,
        7,
        10,
    ):

        return 60.0

    # Panaphara
    if house_number in (
        2,
        5,
        8,
        11,
    ):

        return 30.0

    # Apoklima
    return 15.0


# =========================================================
# PLANET ASPECTS
# =========================================================

def get_planet_aspect_houses(
    planet,
    planets
):
    """
    Return houses receiving aspects from a planet.

    Classical Parashari aspects:

    All planets:
        7th aspect

    Mars:
        4th and 8th

    Jupiter:
        5th and 9th

    Saturn:
        3rd and 10th

    Rahu/Ketu:
        5th, 7th and 9th
        when supported by the project.
    """

    house = get_planet_house(
        planet
    )

    if house is None:
        return []

    name = normalize_planet_name(
        planet.get(
            "name",
            planet.get(
                "planet",
                ""
            )
        )
    )

    aspects = [
        7
    ]

    if name == "Mars":

        aspects.extend([
            4,
            8,
        ])

    elif name == "Jupiter":

        aspects.extend([
            5,
            9,
        ])

    elif name == "Saturn":

        aspects.extend([
            3,
            10,
        ])

    elif name in (
        "Rahu",
        "Ketu",
    ):

        aspects.extend([
            5,
            9,
        ])

    result = []

    for aspect in aspects:

        target = (
            (
                house - 1
            )
            + (
                aspect - 1
            )
        ) % 12 + 1

        if target != house:

            result.append(
                target
            )

    return result


# =========================================================
# PLANET BENEFIC / MALEFIC
# =========================================================

NATURAL_BENEFICS = {
    "Jupiter",
    "Venus",
    "Mercury",
    "Moon",
}

NATURAL_MALEFICS = {
    "Sun",
    "Mars",
    "Saturn",
    "Rahu",
    "Ketu",
}


# =========================================================
# BHAVA DRISHTI BALA
# =========================================================

def calculate_bhava_drishti_bala(
    house_number,
    planets
):
    """
    Calculate the net aspect contribution received
    by a house.

    Benefic planetary aspects add strength.
    Malefic planetary aspects reduce strength.

    The result is kept in Shashtiamsas.
    """

    total = 0.0

    if not isinstance(
        planets,
        list
    ):
        planets = []

    for planet in planets:

        if not isinstance(
            planet,
            dict
        ):
            continue

        name = normalize_planet_name(
            planet.get(
                "name",
                planet.get(
                    "planet",
                    ""
                )
            )
        )

        aspect_houses = (
            get_planet_aspect_houses(
                planet,
                planets
            )
        )

        if house_number not in aspect_houses:
            continue

        if name in NATURAL_BENEFICS:

            total += 15.0

        elif name in NATURAL_MALEFICS:

            total -= 15.0

    return round(
        total,
        2
    )


# =========================================================
# SINGLE BHAVA
# =========================================================

def calculate_single_bhava_bala(
    house_number,
    ascendant_sign,
    planets,
    shadbala_data
):
    """
    Calculate complete Bhava Bala for one house.
    """

    lord_data = (
        calculate_bhavadhipati_bala(
            house_number,
            ascendant_sign,
            planets,
            shadbala_data
        )
    )

    dig_bala = (
        calculate_bhava_dig_bala(
            house_number
        )
    )

    drishti_bala = (
        calculate_bhava_drishti_bala(
            house_number,
            planets
        )
    )

    total = (
        lord_data["value"]
        + dig_bala
        + drishti_bala
    )

    return {

        "house": house_number,

        "house_lord":
            lord_data["lord"],

        "bhavadhipati_bala":
            round(
                lord_data["value"],
                2
            ),

        "bhava_dig_bala":
            round(
                dig_bala,
                2
            ),

        "bhava_drishti_bala":
            round(
                drishti_bala,
                2
            ),

        "total_bhava_bala":
            round(
                total,
                2
            ),

        "bhava_bala_rupas":
            round(
                total
                / SHASTHIAMSA_PER_RUPA,
                2
            ),

    }


# =========================================================
# COMPLETE BHAVA BALA
# =========================================================

def build_bhava_bala_analysis(
    chart,
    shadbala_data=None,
    aspect_data=None
):
    """
    Build Bhava Bala for all 12 houses.

    Returns:

        {
            "table": [...],
            "strongest_house": ...,
            "weakest_house": ...,
            "average_rupas": ...
        }
    """

    if not isinstance(
        chart,
        dict
    ):

        raise ValueError(
            "Chart must be a dictionary."
        )

    planets = chart.get(
        "planets",
        []
    )

    if not isinstance(
        planets,
        list
    ):

        planets = []

    ascendant = chart.get(
        "ascendant",
        {}
    )

    if not isinstance(
        ascendant,
        dict
    ):

        ascendant = {}

    ascendant_sign = (
        ascendant.get(
            "sign_index"
        )
    )

    # -----------------------------------------------------
    # Calculate all houses
    # -----------------------------------------------------

    rows = []

    for house_number in range(
        1,
        HOUSE_COUNT + 1
    ):

        row = calculate_single_bhava_bala(
            house_number,
            ascendant_sign,
            planets,
            shadbala_data
        )

        rows.append(
            row
        )

    # -----------------------------------------------------
    # Rank strongest → weakest
    # -----------------------------------------------------

    ranked = sorted(
        rows,
        key=lambda row:
            row["total_bhava_bala"],
        reverse=True
    )

    for rank, row in enumerate(
        ranked,
        start=1
    ):

        row["rank"] = rank

    # -----------------------------------------------------
    # Restore normal house order
    # -----------------------------------------------------

    table = sorted(
        ranked,
        key=lambda row:
            row["house"]
    )

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

    if table:

        strongest = max(
            table,
            key=lambda row:
                row["total_bhava_bala"]
        )

        weakest = min(
            table,
            key=lambda row:
                row["total_bhava_bala"]
        )

        average_rupas = (
            sum(
                row["bhava_bala_rupas"]
                for row in table
            )
            / len(table)
        )

    else:

        strongest = None
        weakest = None
        average_rupas = 0.0

    return {

        "method":
            "Bhavadhipati Bala + Bhava Dig Bala + Bhava Drishti Bala",

        "unit":
            "Shashtiamsa",

        "shashtiamsa_per_rupa":
            SHASTHIAMSA_PER_RUPA,

        "table":
            table,

        "ranked":
            ranked,

        "strongest_house":
            strongest,

        "weakest_house":
            weakest,

        "average_rupas":
            round(
                average_rupas,
                2
            ),

    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "AI JYOTISH BHAVA BALA ENGINE TEST"
    )
    print("=" * 70)

    sample_chart = {

        "ascendant": {
            "sign_index": 0
        },

        "planets": [],

    }

    result = build_bhava_bala_analysis(
        sample_chart
    )

    print()

    for row in result["ranked"]:

        print(
            f"Rank {row['rank']:2d} | "
            f"House {row['house']:2d} | "
            f"Total "
            f"{row['total_bhava_bala']:7.2f} | "
            f"Rupas "
            f"{row['bhava_bala_rupas']:5.2f}"
        )

    print()
    print(
        "TEST COMPLETED"
    )

    print(
        "=" * 70
    )