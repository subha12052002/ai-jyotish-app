"""
AI Jyotish - Vedic Planetary Aspects (Drishti)

Implements:
- 7th aspect for all planets
- Mars: 4th and 8th aspects
- Jupiter: 5th and 9th aspects
- Saturn: 3rd and 10th aspects
- Rahu/Ketu: 7th , 5th and 9th aspects by default
- Planet -> house aspects
- Planet -> planet aspects
- Aspect lookup and summaries

House numbering:
1 = Ascendant house
2 = 2nd house
...
12 = 12th house

This module works with Whole Sign houses.
"""


# ============================================================
# PLANET ORDER
# ============================================================

PLANETS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu",
]


# ============================================================
# VEDIC ASPECT RULES
# ============================================================

# Every planet has a 7th aspect.
#
# The number represents the house counted from the planet's
# current house.
#
# Example:
# Planet in house 1
# 7th aspect -> house 7
#
# Planet in house 5
# 7th aspect -> house 11

ASPECT_RULES = {
    "Sun": [7],
    "Moon": [7],
    "Mars": [4, 7, 8],
    "Mercury": [7],
    "Jupiter": [5, 7, 9],
    "Venus": [7],
    "Saturn": [3, 7, 10],
    "Rahu": [5,7,9],
    "Ketu": [5,7,9],
}


# ============================================================
# ASPECT NAMES
# ============================================================

ASPECT_NAMES = {
    3: "3rd Aspect",
    4: "4th Aspect",
    5: "5th Aspect",
    7: "7th Aspect",
    8: "8th Aspect",
    9: "9th Aspect",
    10: "10th Aspect",
}


# ============================================================
# VALIDATION
# ============================================================

def validate_house_number(house_number):
    """Validate house number from 1 to 12."""

    try:
        house_number = int(house_number)
    except (TypeError, ValueError):
        raise ValueError(
            "House number must be an integer from 1 to 12."
        )

    if house_number < 1 or house_number > 12:
        raise ValueError(
            "House number must be between 1 and 12."
        )

    return house_number


def normalize_planet_name(planet_name):
    """Normalize planet name for rule lookup."""

    if not planet_name:
        return ""

    return str(planet_name).strip().title()


# ============================================================
# GET ASPECT RULES
# ============================================================

def get_aspect_houses(planet_name):
    """
    Return the aspect numbers applicable to a planet.

    Example:
        Mars -> [4, 7, 8]
        Jupiter -> [5, 7, 9]
        Saturn -> [3, 7, 10]
    """

    planet_name = normalize_planet_name(
        planet_name
    )

    return ASPECT_RULES.get(
        planet_name,
        [7]
    )


# ============================================================
# CALCULATE TARGET HOUSE
# ============================================================

def calculate_aspect_target(
    planet_house,
    aspect_number
):
    """
    Calculate the target house of a Vedic planetary aspect.

    House itself is counted as 1.
    Therefore:
        7th aspect from House 1 -> House 7
        5th aspect from House 10 -> House 2
        9th aspect from House 10 -> House 6
    """

    planet_house = validate_house_number(
        planet_house
    )

    try:
        aspect_number = int(aspect_number)
    except (TypeError, ValueError):
        raise ValueError(
            "Aspect number must be an integer."
        )

    if aspect_number < 1 or aspect_number > 12:
        raise ValueError(
            "Aspect number must be between 1 and 12."
        )

    # Correct Vedic house counting.
    target_house = (
    (planet_house - 1 + aspect_number - 1) % 12
) + 1
    return target_house


# ============================================================
# BUILD SINGLE ASPECT
# ============================================================

def build_aspect(
    planet_name,
    planet_house,
    aspect_number
):
    """
    Build a single aspect record.
    """

    planet_name = normalize_planet_name(
        planet_name
    )

    planet_house = validate_house_number(
        planet_house
    )

    target_house = calculate_aspect_target(
        planet_house,
        aspect_number
    )

    aspect_name = ASPECT_NAMES.get(
        aspect_number,
        f"{aspect_number}th Aspect"
    )

    return {
        "planet": planet_name,

        "source_house": planet_house,

        "aspect_number": aspect_number,

        "aspect_name": aspect_name,

        "target_house": target_house,
    }


# ============================================================
# PLANET ASPECTS
# ============================================================

def calculate_planet_aspects(
    planet_name,
    planet_house
):
    """
    Calculate all aspects cast by one planet.

    Example:

        Mars in House 1

        -> 4th aspect -> House 4
        -> 7th aspect -> House 7
        -> 8th aspect -> House 8
    """

    planet_name = normalize_planet_name(
        planet_name
    )

    planet_house = validate_house_number(
        planet_house
    )

    aspect_numbers = get_aspect_houses(
        planet_name
    )

    aspects = []

    for aspect_number in aspect_numbers:

        aspects.append(
            build_aspect(
                planet_name,
                planet_house,
                aspect_number
            )
        )

    return aspects


# ============================================================
# ALL PLANET ASPECTS
# ============================================================

def calculate_all_aspects(planets):
    """
    Calculate aspects for all planets.

    Expected planet format:

        {
            "name": "Mars",
            "house": 1
        }

    Returns a flat list of aspect records.
    """

    if not planets:
        return []

    all_aspects = []

    for planet in planets:

        if not isinstance(planet, dict):
            continue

        planet_name = planet.get(
            "name"
        )

        planet_house = planet.get(
            "house"
        )

        if not planet_name:
            continue

        if planet_house is None:
            continue

        try:
            aspects = calculate_planet_aspects(
                planet_name,
                planet_house
            )
        except ValueError:
            continue

        all_aspects.extend(
            aspects
        )

    return all_aspects


# ============================================================
# PLANET -> HOUSE ASPECTS
# ============================================================

def get_aspects_to_house(
    aspects,
    target_house
):
    """
    Return all planetary aspects falling on a house.
    """

    target_house = validate_house_number(
        target_house
    )

    if not aspects:
        return []

    return [
        aspect
        for aspect in aspects
        if aspect.get("target_house")
        == target_house
    ]


# ============================================================
# PLANET -> PLANET ASPECT
# ============================================================

def planet_aspects_planet(
    source_planet,
    target_planet,
    planets
):
    """
    Determine whether one planet aspects another planet.

    Returns a list because a planet can potentially have
    more than one applicable aspect relationship.
    """

    source_planet = normalize_planet_name(
        source_planet
    )

    target_planet = normalize_planet_name(
        target_planet
    )

    source = None
    target = None

    for planet in planets or []:

        if not isinstance(planet, dict):
            continue

        name = normalize_planet_name(
            planet.get("name")
        )

        if name == source_planet:
            source = planet

        if name == target_planet:
            target = planet

    if not source or not target:
        return []

    source_house = source.get(
        "house"
    )

    target_house = target.get(
        "house"
    )

    if source_house is None or target_house is None:
        return []

    source_aspects = calculate_planet_aspects(
        source_planet,
        source_house
    )

    result = []

    for aspect in source_aspects:

        if aspect["target_house"] == target_house:

            result.append({
                **aspect,

                "target_planet": target_planet,
            })

    return result


# ============================================================
# ALL PLANET-TO-PLANET ASPECTS
# ============================================================

def calculate_planet_to_planet_aspects(
    planets
):
    """
    Calculate all planet-to-planet aspects.
    """

    if not planets:
        return []

    aspects = calculate_all_aspects(
        planets
    )

    result = []

    for aspect in aspects:

        source_planet = aspect.get(
            "planet"
        )

        target_house = aspect.get(
            "target_house"
        )

        for planet in planets:

            if not isinstance(planet, dict):
                continue

            target_planet = normalize_planet_name(
                planet.get("name")
            )

            source_normalized = normalize_planet_name(
                source_planet
            )

            if not target_planet:
                continue

            # A planet does not aspect itself.
            if target_planet == source_normalized:
                continue

            if planet.get("house") == target_house:

                result.append({
                    **aspect,

                    "target_planet":
                        target_planet,
                })

    return result


# ============================================================
# ASPECTS RECEIVED BY A PLANET
# ============================================================

def get_aspects_to_planet(
    target_planet,
    planets
):
    """
    Return all aspects received by a particular planet.
    """

    target_planet = normalize_planet_name(
        target_planet
    )

    if not planets:
        return []

    target = None

    for planet in planets:

        if not isinstance(planet, dict):
            continue

        if normalize_planet_name(
            planet.get("name")
        ) == target_planet:

            target = planet
            break

    if not target:
        return []

    target_house = target.get(
        "house"
    )

    if target_house is None:
        return []

    all_aspects = calculate_all_aspects(
        planets
    )

    result = []

    for aspect in all_aspects:

        if (
            aspect["target_house"]
            == target_house
            and normalize_planet_name(
                aspect["planet"]
            ) != target_planet
        ):

            result.append({
                **aspect,

                "target_planet":
                    target_planet,
            })

    return result


# ============================================================
# HOUSE ASPECT SUMMARY
# ============================================================

def build_house_aspect_summary(
    planets
):
    """
    Create:

        {
            1: [...],
            2: [...],
            ...
            12: [...]
        }

    showing which planets aspect each house.
    """

    all_aspects = calculate_all_aspects(
        planets
    )

    result = {}

    for house_number in range(1, 13):

        result[house_number] = (
            get_aspects_to_house(
                all_aspects,
                house_number
            )
        )

    return result


# ============================================================
# PLANET ASPECT SUMMARY
# ============================================================

def build_planet_aspect_summary(
    planets
):
    """
    Create a summary for each planet.

    Example:

        {
            "Mars": {
                "casts": [...],
                "receives": [...]
            }
        }
    """

    result = {}

    if not planets:
        return result

    for planet in planets:

        if not isinstance(planet, dict):
            continue

        planet_name = normalize_planet_name(
            planet.get("name")
        )

        if not planet_name:
            continue

        house = planet.get(
            "house"
        )

        if house is None:
            continue

        result[planet_name] = {
            "casts": calculate_planet_aspects(
                planet_name,
                house
            ),

            "receives": get_aspects_to_planet(
                planet_name,
                planets
            ),
        }

    return result


# ============================================================
# SPECIAL ASPECTS
# ============================================================

def get_special_aspects(
    planet_name
):
    """
    Return only special aspects beyond the universal
    7th aspect.
    """

    planet_name = normalize_planet_name(
        planet_name
    )

    aspects = get_aspect_houses(
        planet_name
    )

    return [
        aspect
        for aspect in aspects
        if aspect != 7
    ]


# ============================================================
# ASPECT DESCRIPTION
# ============================================================

def describe_aspect(aspect):
    """
    Create a human-readable description.
    """

    if not aspect:
        return ""

    planet = aspect.get(
        "planet",
        "Unknown"
    )

    source_house = aspect.get(
        "source_house"
    )

    target_house = aspect.get(
        "target_house"
    )

    aspect_name = aspect.get(
        "aspect_name",
        "Aspect"
    )

    return (
        f"{planet} in house {source_house} "
        f"casts its {aspect_name.lower()} "
        f"on house {target_house}."
    )


# ============================================================
# COMPLETE ASPECT ANALYSIS
# ============================================================

def build_aspect_analysis(
    planets
):
    """
    Build complete aspect analysis.

    This is the main function that can later be
    integrated into kundli.py.
    """

    all_aspects = calculate_all_aspects(
        planets
    )

    planet_to_planet = (
        calculate_planet_to_planet_aspects(
            planets
        )
    )

    house_summary = (
        build_house_aspect_summary(
            planets
        )
    )

    planet_summary = (
        build_planet_aspect_summary(
            planets
        )
    )

    return {
        "aspects": all_aspects,

        "planet_to_planet":
            planet_to_planet,

        "by_house":
            house_summary,

        "by_planet":
            planet_summary,

        "total_aspects":
            len(all_aspects),
    }


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("AI JYOTISH - ASPECTS MODULE TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Sample planets
    # --------------------------------------------------------

    sample_planets = [
        {
            "name": "Sun",
            "house": 1,
        },

        {
            "name": "Moon",
            "house": 4,
        },

        {
            "name": "Mars",
            "house": 2,
        },

        {
            "name": "Mercury",
            "house": 5,
        },

        {
            "name": "Jupiter",
            "house": 7,
        },

        {
            "name": "Venus",
            "house": 6,
        },

        {
            "name": "Saturn",
            "house": 10,
        },

        {
            "name": "Rahu",
            "house": 3,
        },

        {
            "name": "Ketu",
            "house": 9,
        },
    ]

    # --------------------------------------------------------
    # Test aspect rules
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("PLANET ASPECT RULES")
    print("-" * 70)

    for planet in PLANETS:

        print(
            f"{planet:10} -> "
            f"{get_aspect_houses(planet)}"
        )

    # --------------------------------------------------------
    # Calculate all aspects
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("ALL PLANETARY ASPECTS")
    print("-" * 70)

    all_aspects = calculate_all_aspects(
        sample_planets
    )

    for aspect in all_aspects:

        print(
            f"{aspect['planet']:10} "
            f"House {aspect['source_house']:2} "
            f"-> "
            f"House {aspect['target_house']:2} "
            f"({aspect['aspect_name']})"
        )

    # --------------------------------------------------------
    # House 7 aspects
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("ASPECTS TO HOUSE 7")
    print("-" * 70)

    house_7_aspects = get_aspects_to_house(
        all_aspects,
        7
    )

    for aspect in house_7_aspects:

        print(
            describe_aspect(aspect)
        )

    # --------------------------------------------------------
    # Mars special aspects
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("MARS SPECIAL ASPECTS")
    print("-" * 70)

    mars_aspects = calculate_planet_aspects(
        "Mars",
        2
    )

    for aspect in mars_aspects:

        print(
            describe_aspect(aspect)
        )

    # --------------------------------------------------------
    # Jupiter special aspects
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("JUPITER SPECIAL ASPECTS")
    print("-" * 70)

    jupiter_aspects = calculate_planet_aspects(
        "Jupiter",
        7
    )

    for aspect in jupiter_aspects:

        print(
            describe_aspect(aspect)
        )

    # --------------------------------------------------------
    # Saturn special aspects
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("SATURN SPECIAL ASPECTS")
    print("-" * 70)

    saturn_aspects = calculate_planet_aspects(
        "Saturn",
        10
    )

    for aspect in saturn_aspects:

        print(
            describe_aspect(aspect)
        )

    # --------------------------------------------------------
    # Planet-to-planet aspects
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("PLANET-TO-PLANET ASPECTS")
    print("-" * 70)

    planet_aspects = (
        calculate_planet_to_planet_aspects(
            sample_planets
        )
    )

    for aspect in planet_aspects:

        print(
            f"{aspect['planet']} "
            f"-> "
            f"{aspect['target_planet']} "
            f"({aspect['aspect_name']})"
        )

    # --------------------------------------------------------
    # Planet summary
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("PLANET ASPECT SUMMARY")
    print("-" * 70)

    summary = build_planet_aspect_summary(
        sample_planets
    )

    for planet, data in summary.items():

        print()
        print(f"{planet}:")

        print(
            "  Casts:"
        )

        for aspect in data["casts"]:

            print(
                f"    -> House "
                f"{aspect['target_house']} "
                f"({aspect['aspect_name']})"
            )

        print(
            "  Receives:"
        )

        for aspect in data["receives"]:

            print(
                f"    <- {aspect['planet']} "
                f"({aspect['aspect_name']})"
            )

    # --------------------------------------------------------
    # Complete analysis
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("COMPLETE ANALYSIS")
    print("-" * 70)

    analysis = build_aspect_analysis(
        sample_planets
    )

    print(
        "Total aspects:",
        analysis["total_aspects"]
    )

    print(
        "Planet-to-planet aspects:",
        len(
            analysis["planet_to_planet"]
        )
    )

    print()
    print("=" * 70)
    print("ASPECTS MODULE TEST COMPLETED")
    print("=" * 70)