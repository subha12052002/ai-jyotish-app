"""
AI Jyotish - Planetary Combustion Engine

Calculates whether planets are combust due to proximity to the Sun.

The calculation uses geocentric ecliptic longitude.

Important:
- Sun itself is never considered combust.
- Rahu and Ketu are excluded from combustion.
- Combustion limits can vary between Jyotish traditions.
- This module uses commonly used approximate limits.
"""


# ============================================================
# PLANETS
# ============================================================

COMBUSTION_PLANETS = [
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
]


# ============================================================
# COMBUSTION LIMITS
# ============================================================

# Approximate angular distances from the Sun.
#
# These values are configurable because different Jyotish
# traditions use slightly different limits.
#
# Mercury:
#   14 degrees
#
# Venus:
#   10 degrees
#
# Mars:
#   17 degrees
#
# Jupiter:
#   11 degrees
#
# Saturn:
#   15 degrees
#
# Moon:
#   12 degrees

COMBUSTION_LIMITS = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": 14.0,
    "Jupiter": 11.0,
    "Venus": 10.0,
    "Saturn": 15.0,
}


# ============================================================
# SEVERITY LEVELS
# ============================================================

def get_combustion_severity(
    distance,
    limit
):
    """
    Determine combustion severity.

    The closer the planet is to the Sun, the stronger
    the combustion condition.

    Returns:
        "Not Combust"
        "Mild"
        "Moderate"
        "Strong"
        "Very Strong"
    """

    if distance > limit:
        return "Not Combust"

    if limit <= 0:
        return "Unknown"

    ratio = distance / limit

    if ratio <= 0.25:
        return "Very Strong"

    if ratio <= 0.50:
        return "Strong"

    if ratio <= 0.75:
        return "Moderate"

    return "Mild"


# ============================================================
# VALIDATION
# ============================================================

def normalize_planet_name(
    planet_name
):
    """Normalize planet name."""

    if not planet_name:
        return ""

    return str(
        planet_name
    ).strip().title()


def normalize_longitude(
    longitude
):
    """
    Normalize longitude to 0-360 degrees.
    """

    try:
        longitude = float(longitude)
    except (TypeError, ValueError):
        raise ValueError(
            "Longitude must be a number."
        )

    longitude = longitude % 360.0

    return longitude


# ============================================================
# ANGULAR DISTANCE
# ============================================================

def angular_distance(
    longitude1,
    longitude2
):
    """
    Calculate the smallest angular distance between
    two zodiac longitudes.

    Example:

        Sun = 359°
        Planet = 1°

        Distance = 2°
    """

    longitude1 = normalize_longitude(
        longitude1
    )

    longitude2 = normalize_longitude(
        longitude2
    )

    difference = abs(
        longitude1 - longitude2
    )

    return min(
        difference,
        360.0 - difference
    )


# ============================================================
# GET COMBUSTION LIMIT
# ============================================================

def get_combustion_limit(
    planet_name
):
    """
    Return combustion limit for a planet.
    """

    planet_name = normalize_planet_name(
        planet_name
    )

    return COMBUSTION_LIMITS.get(
        planet_name
    )


# ============================================================
# CAN PLANET BE COMBUST?
# ============================================================

def can_be_combust(
    planet_name
):
    """
    Check whether combustion is applicable to a planet.
    """

    planet_name = normalize_planet_name(
        planet_name
    )

    return planet_name in COMBUSTION_PLANETS


# ============================================================
# CHECK COMBUSTION
# ============================================================

def is_combust(
    planet_name,
    planet_longitude,
    sun_longitude
):
    """
    Return True if a planet is combust.
    """

    planet_name = normalize_planet_name(
        planet_name
    )

    if not can_be_combust(
        planet_name
    ):
        return False

    distance = angular_distance(
        planet_longitude,
        sun_longitude
    )

    limit = get_combustion_limit(
        planet_name
    )

    if limit is None:
        return False

    return distance <= limit


# ============================================================
# COMPLETE PLANET COMBUSTION ANALYSIS
# ============================================================

def analyze_planet_combustion(
    planet,
    sun_longitude
):
    """
    Analyze combustion for one planet.

    Expected planet format:

        {
            "name": "Venus",
            "longitude": 105.5
        }
    """

    if not isinstance(
        planet,
        dict
    ):
        return None

    planet_name = normalize_planet_name(
        planet.get("name")
    )

    if not planet_name:
        return None

    # Sun cannot be combust.
    if planet_name == "Sun":

        return {
            "planet": "Sun",
            "applicable": False,
            "combust": False,
            "distance_from_sun": 0.0,
            "combustion_limit": None,
            "severity": "Not Applicable",
            "reason": "Sun itself cannot be combust.",
        }

    # Rahu and Ketu are excluded.
    if planet_name in {
        "Rahu",
        "Ketu",
    }:

        return {
            "planet": planet_name,
            "applicable": False,
            "combust": False,
            "distance_from_sun": None,
            "combustion_limit": None,
            "severity": "Not Applicable",
            "reason": (
                "Combustion is not applied to "
                "Rahu/Ketu in this engine."
            ),
        }

    planet_longitude = planet.get(
        "longitude"
    )

    if planet_longitude is None:

        return {
            "planet": planet_name,
            "applicable": False,
            "combust": False,
            "distance_from_sun": None,
            "combustion_limit": None,
            "severity": "Unknown",
            "reason": (
                "Planet longitude is unavailable."
            ),
        }

    try:
        planet_longitude = normalize_longitude(
            planet_longitude
        )

        sun_longitude = normalize_longitude(
            sun_longitude
        )

    except ValueError:

        return {
            "planet": planet_name,
            "applicable": False,
            "combust": False,
            "distance_from_sun": None,
            "combustion_limit": None,
            "severity": "Unknown",
            "reason": (
                "Invalid longitude."
            ),
        }

    limit = get_combustion_limit(
        planet_name
    )

    if limit is None:

        return {
            "planet": planet_name,
            "applicable": False,
            "combust": False,
            "distance_from_sun": None,
            "combustion_limit": None,
            "severity": "Unknown",
            "reason": (
                "No combustion rule is configured "
                "for this planet."
            ),
        }

    distance = angular_distance(
        planet_longitude,
        sun_longitude
    )

    combust = (
        distance <= limit
    )

    severity = get_combustion_severity(
        distance,
        limit
    )

    return {
        "planet": planet_name,

        "applicable": True,

        "combust": combust,

        "planet_longitude":
            round(
                planet_longitude,
                6
            ),

        "sun_longitude":
            round(
                sun_longitude,
                6
            ),

        "distance_from_sun":
            round(
                distance,
                6
            ),

        "combustion_limit":
            limit,

        "severity":
            severity,

        "within_limit":
            combust,

        "retrograde":
            bool(
                planet.get(
                    "retrograde",
                    False
                )
            ),

        "reason": (
            f"{planet_name} is "
            f"{round(distance, 2)}° "
            f"from the Sun; combustion limit "
            f"is {limit}°."
        ),
    }


# ============================================================
# FIND SUN
# ============================================================

def get_sun_from_planets(
    planets
):
    """
    Find the Sun dictionary from a planet list.
    """

    if not planets:
        return None

    for planet in planets:

        if not isinstance(
            planet,
            dict
        ):
            continue

        name = normalize_planet_name(
            planet.get("name")
        )

        if name == "Sun":
            return planet

    return None


# ============================================================
# ANALYZE ALL PLANETS
# ============================================================

def analyze_planets_combustion(
    planets
):
    """
    Analyze combustion for every planet.

    The Sun longitude is taken from the planet list.
    """

    if not planets:
        return []

    sun = get_sun_from_planets(
        planets
    )

    if not sun:
        return []

    sun_longitude = sun.get(
        "longitude"
    )

    if sun_longitude is None:
        return []

    results = []

    for planet in planets:

        result = analyze_planet_combustion(
            planet,
            sun_longitude
        )

        if result:
            results.append(
                result
            )

    return results


# ============================================================
# ENRICH PLANETS
# ============================================================

def enrich_planets_with_combustion(
    planets
):
    """
    Add combustion information to each planet dictionary.

    Original planet data is preserved.
    """

    if not planets:
        return []

    sun = get_sun_from_planets(
        planets
    )

    if not sun:
        return [
            dict(planet)
            for planet in planets
            if isinstance(
                planet,
                dict
            )
        ]

    sun_longitude = sun.get(
        "longitude"
    )

    if sun_longitude is None:
        return [
            dict(planet)
            for planet in planets
            if isinstance(
                planet,
                dict
            )
        ]

    enriched = []

    for planet in planets:

        if not isinstance(
            planet,
            dict
        ):
            continue

        new_planet = dict(
            planet
        )

        analysis = analyze_planet_combustion(
            planet,
            sun_longitude
        )

        if analysis:

            new_planet["combust"] = (
                analysis["combust"]
            )

            new_planet[
                "combustion_applicable"
            ] = (
                analysis["applicable"]
            )

            new_planet[
                "distance_from_sun"
            ] = (
                analysis[
                    "distance_from_sun"
                ]
            )

            new_planet[
                "combustion_limit"
            ] = (
                analysis[
                    "combustion_limit"
                ]
            )

            new_planet[
                "combustion_severity"
            ] = (
                analysis["severity"]
            )

        enriched.append(
            new_planet
        )

    return enriched


# ============================================================
# GET COMBUST PLANETS
# ============================================================

def get_combust_planets(
    combustion_analysis
):
    """
    Return planets that are combust.
    """

    if not combustion_analysis:
        return []

    return [
        item
        for item in combustion_analysis
        if item.get("combust") is True
    ]


# ============================================================
# GET NON-COMBUST PLANETS
# ============================================================

def get_non_combust_planets(
    combustion_analysis
):
    """
    Return applicable planets that are not combust.
    """

    if not combustion_analysis:
        return []

    return [
        item
        for item in combustion_analysis
        if (
            item.get("applicable") is True
            and
            item.get("combust") is False
        )
    ]


# ============================================================
# GET STRONGLY COMBUST PLANETS
# ============================================================

def get_strongly_combust_planets(
    combustion_analysis
):
    """
    Return planets with strong or very strong combustion.
    """

    if not combustion_analysis:
        return []

    return [
        item
        for item in combustion_analysis
        if item.get("severity")
        in {
            "Strong",
            "Very Strong",
        }
    ]


# ============================================================
# BUILD COMBUSTION SUMMARY
# ============================================================

def build_combustion_summary(
    planets
):
    """
    Build complete combustion analysis.
    """

    analysis = analyze_planets_combustion(
        planets
    )

    combust = get_combust_planets(
        analysis
    )

    non_combust = get_non_combust_planets(
        analysis
    )

    strongly_combust = (
        get_strongly_combust_planets(
            analysis
        )
    )

    return {
        "planets": analysis,

        "combust_planets": combust,

        "non_combust_planets":
            non_combust,

        "strongly_combust_planets":
            strongly_combust,

        "total_planets":
            len(analysis),

        "total_combust":
            len(combust),
    }


# ============================================================
# COMBUSTION TABLE
# ============================================================

def build_combustion_table(
    planets
):
    """
    Build a frontend-friendly table.
    """

    analysis = analyze_planets_combustion(
        planets
    )

    table = []

    for item in analysis:

        table.append({
            "planet":
                item["planet"],

            "combust":
                item["combust"],

            "distance_from_sun":
                item["distance_from_sun"],

            "limit":
                item["combustion_limit"],

            "severity":
                item["severity"],
        })

    return table


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("AI JYOTISH - COMBUSTION MODULE TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Sample planets
    # --------------------------------------------------------
    #
    # Sun = 100°
    #
    # Mercury = 105° -> 5° from Sun -> Combust
    # Venus = 107°   -> 7° from Sun -> Combust
    # Mars = 125°    -> 25° from Sun -> Not Combust
    # Jupiter = 130° -> 30° from Sun -> Not Combust
    # Saturn = 80°   -> 20° from Sun -> Not Combust
    #

    sample_planets = [

        {
            "name": "Sun",
            "longitude": 100.0,
            "retrograde": False,
        },

        {
            "name": "Mercury",
            "longitude": 105.0,
            "retrograde": False,
        },

        {
            "name": "Venus",
            "longitude": 107.0,
            "retrograde": False,
        },

        {
            "name": "Mars",
            "longitude": 125.0,
            "retrograde": False,
        },

        {
            "name": "Jupiter",
            "longitude": 130.0,
            "retrograde": False,
        },

        {
            "name": "Saturn",
            "longitude": 80.0,
            "retrograde": True,
        },

        {
            "name": "Rahu",
            "longitude": 102.0,
            "retrograde": True,
        },

        {
            "name": "Ketu",
            "longitude": 282.0,
            "retrograde": True,
        },
    ]

    # --------------------------------------------------------
    # Test angular distance
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("ANGULAR DISTANCE TEST")
    print("-" * 70)

    tests = [
        (100, 105),
        (359, 1),
        (10, 350),
        (100, 130),
    ]

    for a, b in tests:

        distance = angular_distance(
            a,
            b
        )

        print(
            f"{a}° -> {b}° = "
            f"{distance}°"
        )

    # --------------------------------------------------------
    # Test combustion limits
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("COMBUSTION LIMITS")
    print("-" * 70)

    for planet, limit in COMBUSTION_LIMITS.items():

        print(
            f"{planet:10} -> "
            f"{limit}°"
        )

    # --------------------------------------------------------
    # Analyze all planets
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("PLANETARY COMBUSTION")
    print("-" * 70)

    analysis = analyze_planets_combustion(
        sample_planets
    )

    for item in analysis:

        print(
            f"{item['planet']:10} | "
            f"Combust: "
            f"{str(item['combust']):5} | "
            f"Distance: "
            f"{str(item['distance_from_sun']):7} | "
            f"Limit: "
            f"{str(item['combustion_limit']):5} | "
            f"Severity: "
            f"{item['severity']}"
        )

    # --------------------------------------------------------
    # Combust planets
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("COMBUST PLANETS")
    print("-" * 70)

    combust = get_combust_planets(
        analysis
    )

    for item in combust:

        print(
            f"{item['planet']} "
            f"-> {item['severity']}"
        )

    # --------------------------------------------------------
    # Strongly combust planets
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("STRONGLY COMBUST PLANETS")
    print("-" * 70)

    strongly_combust = (
        get_strongly_combust_planets(
            analysis
        )
    )

    for item in strongly_combust:

        print(
            f"{item['planet']} "
            f"-> {item['severity']}"
        )

    # --------------------------------------------------------
    # Enrichment test
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("ENRICHED PLANETS")
    print("-" * 70)

    enriched = (
        enrich_planets_with_combustion(
            sample_planets
        )
    )

    for planet in enriched:

        print(
            f"{planet['name']:10} | "
            f"Combust: "
            f"{planet.get('combust')} | "
            f"Severity: "
            f"{planet.get('combustion_severity')}"
        )

    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("COMBUSTION TABLE")
    print("-" * 70)

    table = build_combustion_table(
        sample_planets
    )

    for row in table:

        print(
            f"{row['planet']:10} | "
            f"{str(row['combust']):5} | "
            f"{str(row['distance_from_sun']):7}° | "
            f"{str(row['limit']):5}° | "
            f"{row['severity']}"
        )

    # --------------------------------------------------------
    # Complete summary
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("COMPLETE SUMMARY")
    print("-" * 70)

    summary = build_combustion_summary(
        sample_planets
    )

    print(
        "Total planets:",
        summary["total_planets"]
    )

    print(
        "Total combust:",
        summary["total_combust"]
    )

    print(
        "Combust planets:",
        [
            p["planet"]
            for p in summary[
                "combust_planets"
            ]
        ]
    )

    print()
    print("=" * 70)
    print("COMBUSTION MODULE TEST COMPLETED")
    print("=" * 70)