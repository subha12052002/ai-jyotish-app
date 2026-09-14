"""
AI Jyotish - House / Bhava Analysis Engine

Handles:
- 12 Bhavas
- Rashi in each house
- Rashi lord
- House themes
- Planets occupying houses
- Empty / occupied houses
- Kendra
- Trikona
- Dusthana
- Upachaya
- Maraka
- Basic house analysis

This module uses Whole Sign Houses.
"""

from ephemeris import (
    SIGNS,
    get_sign_lord,
    get_house_sign,
    calculate_whole_sign_houses,
)


# ============================================================
# HOUSE DEFINITIONS
# ============================================================

HOUSE_NAMES = {
    1: "Tanu Bhava",
    2: "Dhana Bhava",
    3: "Sahaja Bhava",
    4: "Sukha Bhava",
    5: "Putra Bhava",
    6: "Ari Bhava",
    7: "Kalatra Bhava",
    8: "Randhra Bhava",
    9: "Dharma Bhava",
    10: "Karma Bhava",
    11: "Labha Bhava",
    12: "Vyaya Bhava",
}


HOUSE_THEMES = {
    1: {
        "name": "Self, body and personality",
        "description": "Physical body, appearance, personality, identity, vitality and overall life direction.",
    },
    2: {
        "name": "Wealth, family and speech",
        "description": "Money, accumulated wealth, family values, food, speech and possessions.",
    },
    3: {
        "name": "Courage, communication and siblings",
        "description": "Courage, initiative, communication, younger siblings, skills and short journeys.",
    },
    4: {
        "name": "Home, mother and happiness",
        "description": "Mother, home, property, vehicles, emotional happiness, education and inner peace.",
    },
    5: {
        "name": "Intelligence, children and creativity",
        "description": "Children, intelligence, education, creativity, romance, speculation and past-life merit.",
    },
    6: {
        "name": "Enemies, disease and service",
        "description": "Health problems, debts, enemies, competition, service, work and daily struggles.",
    },
    7: {
        "name": "Marriage and partnerships",
        "description": "Marriage, spouse, partnerships, business relationships, contracts and public dealings.",
    },
    8: {
        "name": "Transformation and longevity",
        "description": "Longevity, sudden events, inheritance, hidden matters, transformation and occult subjects.",
    },
    9: {
        "name": "Dharma, fortune and higher knowledge",
        "description": "Luck, dharma, father, teachers, higher education, spirituality and long-distance travel.",
    },
    10: {
        "name": "Career, profession and status",
        "description": "Career, profession, authority, reputation, achievements and public status.",
    },
    11: {
        "name": "Gains, income and networks",
        "description": "Income, financial gains, elder siblings, friendships, ambitions and fulfillment of desires.",
    },
    12: {
        "name": "Expenses, foreign lands and liberation",
        "description": "Expenses, losses, sleep, foreign residence, isolation, spirituality and liberation.",
    },
}


# ============================================================
# HOUSE CLASSIFICATIONS
# ============================================================

KENDRA_HOUSES = {1, 4, 7, 10}

TRIKONA_HOUSES = {1, 5, 9}

DUSTHANA_HOUSES = {6, 8, 12}

UPACHAYA_HOUSES = {3, 6, 10, 11}

MARAKA_HOUSES = {2, 7}


# ============================================================
# VALIDATION
# ============================================================

def validate_house_number(house_number):
    """Validate a house number."""

    try:
        house_number = int(house_number)
    except (TypeError, ValueError):
        raise ValueError("House number must be an integer from 1 to 12.")

    if house_number < 1 or house_number > 12:
        raise ValueError("House number must be between 1 and 12.")

    return house_number


def validate_sign_index(sign_index):
    """Validate a zodiac sign index."""

    try:
        sign_index = int(sign_index)
    except (TypeError, ValueError):
        raise ValueError("Sign index must be an integer from 0 to 11.")

    if sign_index < 0 or sign_index > 11:
        raise ValueError("Sign index must be between 0 and 11.")

    return sign_index


# ============================================================
# HOUSE CLASSIFICATION FUNCTIONS
# ============================================================

def is_kendra(house_number):
    """Return True if house is a Kendra house."""
    return validate_house_number(house_number) in KENDRA_HOUSES


def is_trikona(house_number):
    """Return True if house is a Trikona house."""
    return validate_house_number(house_number) in TRIKONA_HOUSES


def is_dusthana(house_number):
    """Return True if house is a Dusthana house."""
    return validate_house_number(house_number) in DUSTHANA_HOUSES


def is_upachaya(house_number):
    """Return True if house is an Upachaya house."""
    return validate_house_number(house_number) in UPACHAYA_HOUSES


def is_maraka(house_number):
    """Return True if house is a Maraka house."""
    return validate_house_number(house_number) in MARAKA_HOUSES


def get_house_category(house_number):
    """
    Return all major classifications of a house.

    Example:
        House 1 -> ["Kendra", "Trikona"]
    """

    house_number = validate_house_number(house_number)

    categories = []

    if house_number in KENDRA_HOUSES:
        categories.append("Kendra")

    if house_number in TRIKONA_HOUSES:
        categories.append("Trikona")

    if house_number in DUSTHANA_HOUSES:
        categories.append("Dusthana")

    if house_number in UPACHAYA_HOUSES:
        categories.append("Upachaya")

    if house_number in MARAKA_HOUSES:
        categories.append("Maraka")

    return categories


# ============================================================
# HOUSE THEME
# ============================================================

def get_house_theme(house_number):
    """Return the theme/details of a house."""

    house_number = validate_house_number(house_number)

    return HOUSE_THEMES[house_number]


# ============================================================
# SIGN / RASHI FUNCTIONS
# ============================================================

def get_house_sign_index(asc_sign_index, house_number):
    """
    Get the zodiac sign index occupying a particular house.

    Whole Sign House system:
        House 1 = Ascendant sign
        House 2 = next sign
        ...
        House 12 = sign before Ascendant
    """

    asc_sign_index = validate_sign_index(asc_sign_index)
    house_number = validate_house_number(house_number)

    return (asc_sign_index + house_number - 1) % 12


def get_house_sign_name(asc_sign_index, house_number):
    """Get the Rashi name occupying a house."""

    sign_index = get_house_sign_index(
        asc_sign_index,
        house_number
    )

    return SIGNS[sign_index]


def get_house_lord(asc_sign_index, house_number):
    """Get the lord of the sign occupying a house."""

    sign_index = get_house_sign_index(
        asc_sign_index,
        house_number
    )

    return get_sign_lord(sign_index)


# ============================================================
# SINGLE HOUSE INFORMATION
# ============================================================

def get_house_info(asc_sign_index, house_number):
    """
    Return complete information about one house.
    """

    asc_sign_index = validate_sign_index(asc_sign_index)
    house_number = validate_house_number(house_number)

    sign_index = get_house_sign_index(
        asc_sign_index,
        house_number
    )

    sign_name = SIGNS[sign_index]

    lord = get_sign_lord(sign_index)

    theme = get_house_theme(house_number)

    categories = get_house_category(house_number)

    return {
        "house": house_number,
        "name": HOUSE_NAMES[house_number],

        "sign": sign_name,
        "sign_index": sign_index,

        "lord": lord,

        "theme": theme["name"],
        "description": theme["description"],

        "categories": categories,

        "kendra": house_number in KENDRA_HOUSES,
        "trikona": house_number in TRIKONA_HOUSES,
        "dusthana": house_number in DUSTHANA_HOUSES,
        "upachaya": house_number in UPACHAYA_HOUSES,
        "maraka": house_number in MARAKA_HOUSES,

        "planets": [],
        "planet_names": [],
        "occupied": False,
        "planet_count": 0,
    }


# ============================================================
# BUILD ALL 12 HOUSES
# ============================================================

def build_houses(asc_sign_index):
    """
    Build all 12 Whole Sign houses.

    Returns:
        List containing 12 house dictionaries.
    """

    asc_sign_index = validate_sign_index(asc_sign_index)

    houses = []

    for house_number in range(1, 13):

        house = get_house_info(
            asc_sign_index,
            house_number
        )

        houses.append(house)

    return houses


# ============================================================
# FIND HOUSE
# ============================================================

def get_house_by_number(houses, house_number):
    """Find a house from a house list."""

    house_number = validate_house_number(house_number)

    for house in houses:

        if house.get("house") == house_number:
            return house

    return None


# ============================================================
# PLANET HOUSE FUNCTIONS
# ============================================================

def get_planets_in_house(planets, house_number):
    """
    Get planets occupying a particular house.

    Works with planet dictionaries containing:
        house

    Example:
        {
            "name": "Sun",
            "house": 10
        }
    """

    house_number = validate_house_number(house_number)

    if not planets:
        return []

    result = []

    for planet in planets:

        if not isinstance(planet, dict):
            continue

        if planet.get("house") == house_number:
            result.append(planet)

    return result


def assign_planets_to_houses(houses, planets):
    """
    Add planets to the appropriate houses.

    Returns a new enriched house list.
    """

    if houses is None:
        return []

    enriched_houses = []

    for house in houses:

        new_house = dict(house)

        house_number = new_house["house"]

        occupying_planets = get_planets_in_house(
            planets,
            house_number
        )

        new_house["planets"] = occupying_planets

        new_house["planet_names"] = [
            planet.get("name")
            for planet in occupying_planets
            if planet.get("name")
        ]

        new_house["planet_count"] = len(
            occupying_planets
        )

        new_house["occupied"] = (
            len(occupying_planets) > 0
        )

        enriched_houses.append(new_house)

    return enriched_houses


# ============================================================
# OCCUPIED / EMPTY HOUSES
# ============================================================

def get_occupied_houses(houses):
    """Return house numbers containing planets."""

    if not houses:
        return []

    return [
        house["house"]
        for house in houses
        if house.get("occupied", False)
    ]


def get_empty_houses(houses):
    """Return house numbers without planets."""

    if not houses:
        return []

    return [
        house["house"]
        for house in houses
        if not house.get("occupied", False)
    ]


# ============================================================
# CLASSIFICATION GROUPS
# ============================================================

def get_kendra_houses(houses=None):
    """Return Kendra houses."""

    if houses is None:
        return sorted(KENDRA_HOUSES)

    return [
        house
        for house in houses
        if house["house"] in KENDRA_HOUSES
    ]


def get_trikona_houses(houses=None):
    """Return Trikona houses."""

    if houses is None:
        return sorted(TRIKONA_HOUSES)

    return [
        house
        for house in houses
        if house["house"] in TRIKONA_HOUSES
    ]


def get_dusthana_houses(houses=None):
    """Return Dusthana houses."""

    if houses is None:
        return sorted(DUSTHANA_HOUSES)

    return [
        house
        for house in houses
        if house["house"] in DUSTHANA_HOUSES
    ]


def get_upachaya_houses(houses=None):
    """Return Upachaya houses."""

    if houses is None:
        return sorted(UPACHAYA_HOUSES)

    return [
        house
        for house in houses
        if house["house"] in UPACHAYA_HOUSES
    ]


def get_maraka_houses(houses=None):
    """Return Maraka houses."""

    if houses is None:
        return sorted(MARAKA_HOUSES)

    return [
        house
        for house in houses
        if house["house"] in MARAKA_HOUSES
    ]


# ============================================================
# HOUSE ANALYSIS
# ============================================================

def build_house_analysis(asc_sign_index, planets=None):
    """
    Build complete house analysis.

    Parameters:
        asc_sign_index:
            Ascendant zodiac sign index (0-11)

        planets:
            Optional list of planet dictionaries.

    Returns:
        Complete house analysis dictionary.
    """

    asc_sign_index = validate_sign_index(
        asc_sign_index
    )

    if planets is None:
        planets = []

    houses = build_houses(
        asc_sign_index
    )

    houses = assign_planets_to_houses(
        houses,
        planets
    )

    occupied_houses = get_occupied_houses(
        houses
    )

    empty_houses = get_empty_houses(
        houses
    )

    return {
        "ascendant_sign": SIGNS[asc_sign_index],

        "ascendant_sign_index": asc_sign_index,

        "house_system": "Whole Sign",

        "houses": houses,

        "occupied_houses": occupied_houses,

        "empty_houses": empty_houses,

        "classifications": {
            "kendra": sorted(KENDRA_HOUSES),
            "trikona": sorted(TRIKONA_HOUSES),
            "dusthana": sorted(DUSTHANA_HOUSES),
            "upachaya": sorted(UPACHAYA_HOUSES),
            "maraka": sorted(MARAKA_HOUSES),
        },
    }


# ============================================================
# HOUSE SUMMARY
# ============================================================

def build_house_summary(houses):
    """
    Create a simplified house summary suitable
    for frontend / AI interpretation.
    """

    summary = []

    if not houses:
        return summary

    for house in houses:

        summary.append({
            "house": house.get("house"),
            "name": house.get("name"),
            "sign": house.get("sign"),
            "lord": house.get("lord"),
            "occupied": house.get("occupied", False),
            "planets": house.get("planet_names", []),
            "categories": house.get("categories", []),
            "theme": house.get("theme"),
        })

    return summary


# ============================================================
# HOUSE LORDS TABLE
# ============================================================

def get_house_lords_table(asc_sign_index):
    """
    Return a simple House -> Sign -> Lord table.
    """

    houses = build_houses(
        asc_sign_index
    )

    table = []

    for house in houses:

        table.append({
            "house": house["house"],
            "house_name": house["name"],
            "sign": house["sign"],
            "sign_index": house["sign_index"],
            "lord": house["lord"],
        })

    return table


# ============================================================
# FIND ALL HOUSES OF A LORD
# ============================================================

def get_houses_owned_by_planet(asc_sign_index, planet_name):
    """
    Find houses whose signs are ruled by a particular planet.
    """

    houses = build_houses(
        asc_sign_index
    )

    result = []

    planet_name = str(
        planet_name
    ).strip().lower()

    for house in houses:

        lord = str(
            house["lord"]
        ).strip().lower()

        if lord == planet_name:
            result.append(house["house"])

    return result


# ============================================================
# PLANETS BY HOUSE
# ============================================================

def build_planets_by_house(houses):
    """
    Return:

        {
            1: ["Sun"],
            2: ["Moon"],
            ...
        }
    """

    result = {}

    if not houses:
        return result

    for house in houses:

        house_number = house["house"]

        result[house_number] = (
            house.get("planet_names", [])
        )

    return result


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("AI JYOTISH - HOUSES MODULE TEST")
    print("=" * 60)

    # Aries Ascendant
    ascendant_sign_index = 0

    # Sample planets
    sample_planets = [
        {
            "name": "Sun",
            "sign": "Aries",
            "sign_index": 0,
            "house": 1,
        },
        {
            "name": "Moon",
            "sign": "Cancer",
            "sign_index": 3,
            "house": 4,
        },
        {
            "name": "Mars",
            "sign": "Gemini",
            "sign_index": 2,
            "house": 3,
        },
        {
            "name": "Jupiter",
            "sign": "Leo",
            "sign_index": 4,
            "house": 5,
        },
        {
            "name": "Saturn",
            "sign": "Capricorn",
            "sign_index": 9,
            "house": 10,
        },
    ]

    # Build analysis
    analysis = build_house_analysis(
        ascendant_sign_index,
        sample_planets
    )

    print()
    print("Ascendant:", analysis["ascendant_sign"])

    print()
    print("-" * 60)
    print("12 HOUSES")
    print("-" * 60)

    for house in analysis["houses"]:

        print(
            f"House {house['house']:2} | "
            f"{house['name']:18} | "
            f"Sign: {house['sign']:10} | "
            f"Lord: {house['lord']:8} | "
            f"Planets: {house['planet_names']} | "
            f"Categories: {house['categories']}"
        )

    print()
    print("-" * 60)
    print("OCCUPIED HOUSES")
    print("-" * 60)

    print(
        analysis["occupied_houses"]
    )

    print()
    print("-" * 60)
    print("EMPTY HOUSES")
    print("-" * 60)

    print(
        analysis["empty_houses"]
    )

    print()
    print("-" * 60)
    print("HOUSE CLASSIFICATIONS")
    print("-" * 60)

    print(
        "Kendra   :", analysis["classifications"]["kendra"]
    )

    print(
        "Trikona  :", analysis["classifications"]["trikona"]
    )

    print(
        "Dusthana :", analysis["classifications"]["dusthana"]
    )

    print(
        "Upachaya :", analysis["classifications"]["upachaya"]
    )

    print(
        "Maraka   :", analysis["classifications"]["maraka"]
    )

    print()
    print("-" * 60)
    print("HOUSE LORD TABLE")
    print("-" * 60)

    for row in get_house_lords_table(
        ascendant_sign_index
    ):
        print(
            f"{row['house']:2}. "
            f"{row['sign']:10} -> "
            f"{row['lord']}"
        )

    print()
    print("=" * 60)
    print("HOUSES MODULE TEST COMPLETED")
    print("=" * 60)