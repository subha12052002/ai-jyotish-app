"""
AI Jyotish - Planetary Dignity Engine

Calculates:
- Exaltation
- Debilitation
- Own sign
- Moolatrikona
- Friendly sign
- Neutral sign
- Enemy sign
- Dignity score
- Dignity strength
- Planetary dignity analysis

Works with the existing ephemeris.py and planets.py.
"""

from ephemeris import SIGNS, get_sign_lord


# ============================================================
# PLANETS
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
# SIGN LORDS
# ============================================================

SIGN_LORDS = {
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
    "Pisces": "Jupiter",
}


# ============================================================
# EXALTATION SIGNS
# ============================================================

EXALTATION_SIGNS = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",

    # Rahu/Ketu traditions vary.
    # These are kept here as a configurable traditional scheme.
    "Rahu": "Taurus",
    "Ketu": "Scorpio",
}


# ============================================================
# DEBILITATION SIGNS
# ============================================================

DEBILITATION_SIGNS = {
    "Sun": "Libra",
    "Moon": "Scorpio",
    "Mars": "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus": "Virgo",
    "Saturn": "Aries",

    "Rahu": "Scorpio",
    "Ketu": "Taurus",
}


# ============================================================
# OWN SIGNS
# ============================================================

OWN_SIGNS = {
    "Sun": [
        "Leo",
    ],

    "Moon": [
        "Cancer",
    ],

    "Mars": [
        "Aries",
        "Scorpio",
    ],

    "Mercury": [
        "Gemini",
        "Virgo",
    ],

    "Jupiter": [
        "Sagittarius",
        "Pisces",
    ],

    "Venus": [
        "Taurus",
        "Libra",
    ],

    "Saturn": [
        "Capricorn",
        "Aquarius",
    ],

    # Node sign ownership varies between traditions.
    "Rahu": [],
    "Ketu": [],
}


# ============================================================
# MOOLATRIKONA SIGNS
# ============================================================

MOOLATRIKONA_SIGNS = {
    "Sun": "Leo",
    "Moon": "Taurus",
    "Mars": "Aries",
    "Mercury": "Virgo",
    "Jupiter": "Sagittarius",
    "Venus": "Libra",
    "Saturn": "Aquarius",

    "Rahu": None,
    "Ketu": None,
}


# ============================================================
# NATURAL FRIENDS
# ============================================================

NATURAL_FRIENDS = {
    "Sun": {
        "Moon",
        "Mars",
        "Jupiter",
    },

    "Moon": {
        "Sun",
        "Mercury",
    },

    "Mars": {
        "Sun",
        "Moon",
        "Jupiter",
    },

    "Mercury": {
        "Sun",
        "Venus",
    },

    "Jupiter": {
        "Sun",
        "Moon",
        "Mars",
    },

    "Venus": {
        "Mercury",
        "Saturn",
    },

    "Saturn": {
        "Mercury",
        "Venus",
    },

    "Rahu": {
        "Venus",
        "Saturn",
        "Mercury",
    },

    "Ketu": {
        "Mars",
        "Jupiter",
    },
}


# ============================================================
# NATURAL ENEMIES
# ============================================================

NATURAL_ENEMIES = {
    "Sun": {
        "Venus",
        "Saturn",
    },

    "Moon": set(),

    "Mars": {
        "Mercury",
    },

    "Mercury": {
        "Moon",
    },

    "Jupiter": {
        "Mercury",
        "Venus",
    },

    "Venus": {
        "Sun",
        "Moon",
    },

    "Saturn": {
        "Sun",
        "Moon",
        "Mars",
    },

    "Rahu": {
        "Sun",
        "Moon",
        "Mars",
    },

    "Ketu": {
        "Sun",
        "Moon",
    },
}


# ============================================================
# DIGNITY SCORES
# ============================================================

DIGNITY_SCORES = {
    "Exalted": 5,
    "Moolatrikona": 4,
    "Own Sign": 3,
    "Friendly Sign": 2,
    "Neutral Sign": 1,
    "Enemy Sign": -1,
    "Debilitated": -5,
    "Unknown": 0,
}


# ============================================================
# VALIDATION
# ============================================================

def normalize_planet_name(planet_name):
    """Normalize a planet name."""

    if not planet_name:
        return ""

    return str(
        planet_name
    ).strip().title()


def normalize_sign_name(sign_name):
    """Normalize a zodiac sign name."""

    if not sign_name:
        return ""

    return str(
        sign_name
    ).strip().title()


def validate_sign_index(sign_index):
    """Validate zodiac sign index."""

    try:
        sign_index = int(sign_index)
    except (TypeError, ValueError):
        raise ValueError(
            "Sign index must be an integer from 0 to 11."
        )

    if sign_index < 0 or sign_index > 11:
        raise ValueError(
            "Sign index must be between 0 and 11."
        )

    return sign_index


# ============================================================
# SIGN RELATIONSHIP
# ============================================================

def get_sign_lord_by_name(sign_name):
    """
    Get the lord of a zodiac sign.
    """

    sign_name = normalize_sign_name(
        sign_name
    )

    return SIGN_LORDS.get(
        sign_name
    )


def get_natural_relationship(
    planet_name,
    sign_name
):
    """
    Determine the natural relationship between a planet
    and the lord of the sign it occupies.

    Returns:
        Friend
        Neutral
        Enemy
        Unknown
    """

    planet_name = normalize_planet_name(
        planet_name
    )

    sign_name = normalize_sign_name(
        sign_name
    )

    sign_lord = get_sign_lord_by_name(
        sign_name
    )

    if not sign_lord:
        return "Unknown"

    if sign_lord == planet_name:
        return "Own"

    if sign_lord in NATURAL_FRIENDS.get(
        planet_name,
        set()
    ):
        return "Friend"

    if sign_lord in NATURAL_ENEMIES.get(
        planet_name,
        set()
    ):
        return "Enemy"

    return "Neutral"


# ============================================================
# INDIVIDUAL DIGNITY CHECKS
# ============================================================

def is_exalted(
    planet_name,
    sign_name
):
    """Return True if planet is exalted."""

    planet_name = normalize_planet_name(
        planet_name
    )

    sign_name = normalize_sign_name(
        sign_name
    )

    return (
        EXALTATION_SIGNS.get(planet_name)
        == sign_name
    )


def is_debilitated(
    planet_name,
    sign_name
):
    """Return True if planet is debilitated."""

    planet_name = normalize_planet_name(
        planet_name
    )

    sign_name = normalize_sign_name(
        sign_name
    )

    return (
        DEBILITATION_SIGNS.get(planet_name)
        == sign_name
    )


def is_own_sign(
    planet_name,
    sign_name
):
    """Return True if planet occupies its own sign."""

    planet_name = normalize_planet_name(
        planet_name
    )

    sign_name = normalize_sign_name(
        sign_name
    )

    return sign_name in OWN_SIGNS.get(
        planet_name,
        []
    )


def is_moolatrikona(
    planet_name,
    sign_name
):
    """Return True if planet occupies its Moolatrikona sign."""

    planet_name = normalize_planet_name(
        planet_name
    )

    sign_name = normalize_sign_name(
        sign_name
    )

    return (
        MOOLATRIKONA_SIGNS.get(
            planet_name
        )
        == sign_name
    )


# ============================================================
# DIGNITY
# ============================================================

def get_dignity(
    planet_name,
    sign_name
):
    """
    Determine planetary dignity.

    Priority:
        Exalted
        Debilitated
        Moolatrikona
        Own Sign
        Friendly Sign
        Enemy Sign
        Neutral Sign
    """

    planet_name = normalize_planet_name(
        planet_name
    )

    sign_name = normalize_sign_name(
        sign_name
    )

    if not planet_name or not sign_name:
        return "Unknown"

    if is_exalted(
        planet_name,
        sign_name
    ):
        return "Exalted"

    if is_debilitated(
        planet_name,
        sign_name
    ):
        return "Debilitated"

    if is_moolatrikona(
        planet_name,
        sign_name
    ):
        return "Moolatrikona"

    if is_own_sign(
        planet_name,
        sign_name
    ):
        return "Own Sign"

    relationship = get_natural_relationship(
        planet_name,
        sign_name
    )

    if relationship == "Friend":
        return "Friendly Sign"

    if relationship == "Enemy":
        return "Enemy Sign"

    if relationship == "Neutral":
        return "Neutral Sign"

    return "Unknown"


# ============================================================
# DIGNITY SCORE
# ============================================================

def get_dignity_score(
    planet_name,
    sign_name
):
    """Return numeric dignity score."""

    dignity = get_dignity(
        planet_name,
        sign_name
    )

    return DIGNITY_SCORES.get(
        dignity,
        0
    )


# ============================================================
# STRENGTH LABEL
# ============================================================

def get_dignity_strength(
    dignity
):
    """
    Convert dignity into a simple strength category.
    """

    if dignity == "Exalted":
        return "Very Strong"

    if dignity == "Moolatrikona":
        return "Strong"

    if dignity == "Own Sign":
        return "Strong"

    if dignity == "Friendly Sign":
        return "Good"

    if dignity == "Neutral Sign":
        return "Average"

    if dignity == "Enemy Sign":
        return "Weak"

    if dignity == "Debilitated":
        return "Very Weak"

    return "Unknown"


# ============================================================
# COMPLETE PLANET DIGNITY ANALYSIS
# ============================================================

def analyze_planet_dignity(
    planet
):
    """
    Analyze dignity from a planet dictionary.

    Expected:

        {
            "name": "Jupiter",
            "sign": "Cancer",
            "sign_index": 3
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

    sign_name = normalize_sign_name(
        planet.get("sign")
    )

    if not planet_name or not sign_name:
        return None

    sign_lord = get_sign_lord_by_name(
        sign_name
    )

    relationship = get_natural_relationship(
        planet_name,
        sign_name
    )

    dignity = get_dignity(
        planet_name,
        sign_name
    )

    score = get_dignity_score(
        planet_name,
        sign_name
    )

    strength = get_dignity_strength(
        dignity
    )

    result = {
        "planet": planet_name,

        "sign": sign_name,

        "sign_index": planet.get(
            "sign_index"
        ),

        "sign_lord": sign_lord,

        "relationship_with_sign_lord":
            relationship,

        "dignity": dignity,

        "dignity_score": score,

        "strength": strength,

        "exalted": is_exalted(
            planet_name,
            sign_name
        ),

        "debilitated": is_debilitated(
            planet_name,
            sign_name
        ),

        "own_sign": is_own_sign(
            planet_name,
            sign_name
        ),

        "moolatrikona":
            is_moolatrikona(
                planet_name,
                sign_name
            ),
    }

    return result


# ============================================================
# ANALYZE ALL PLANETS
# ============================================================

def analyze_planets_dignity(
    planets
):
    """
    Analyze dignity for all planets.
    """

    if not planets:
        return []

    results = []

    for planet in planets:

        analysis = analyze_planet_dignity(
            planet
        )

        if analysis:
            results.append(
                analysis
            )

    return results


# ============================================================
# PLANET DICT WITH DIGNITY
# ============================================================

def enrich_planets_with_dignity(
    planets
):
    """
    Add dignity information to planet dictionaries.

    Original planet data is preserved.
    """

    if not planets:
        return []

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

        analysis = analyze_planet_dignity(
            planet
        )

        if analysis:

            new_planet["dignity"] = (
                analysis["dignity"]
            )

            new_planet["dignity_score"] = (
                analysis["dignity_score"]
            )

            new_planet["dignity_strength"] = (
                analysis["strength"]
            )

            new_planet["sign_lord"] = (
                analysis["sign_lord"]
            )

            new_planet[
                "relationship_with_sign_lord"
            ] = (
                analysis[
                    "relationship_with_sign_lord"
                ]
            )

            new_planet["exalted"] = (
                analysis["exalted"]
            )

            new_planet["debilitated"] = (
                analysis["debilitated"]
            )

            new_planet["own_sign"] = (
                analysis["own_sign"]
            )

            new_planet["moolatrikona"] = (
                analysis["moolatrikona"]
            )

        enriched.append(
            new_planet
        )

    return enriched


# ============================================================
# STRONG / WEAK PLANETS
# ============================================================

def get_strong_planets(
    dignity_analysis
):
    """
    Return planets with positive dignity.
    """

    if not dignity_analysis:
        return []

    return [
        item
        for item in dignity_analysis
        if item.get("dignity_score", 0) >= 2
    ]


def get_weak_planets(
    dignity_analysis
):
    """
    Return planets with negative dignity.
    """

    if not dignity_analysis:
        return []

    return [
        item
        for item in dignity_analysis
        if item.get("dignity_score", 0) < 0
    ]


def get_exalted_planets(
    dignity_analysis
):
    """Return exalted planets."""

    if not dignity_analysis:
        return []

    return [
        item
        for item in dignity_analysis
        if item.get("dignity") == "Exalted"
    ]


def get_debilitated_planets(
    dignity_analysis
):
    """Return debilitated planets."""

    if not dignity_analysis:
        return []

    return [
        item
        for item in dignity_analysis
        if item.get("dignity") == "Debilitated"
    ]


# ============================================================
# COMPLETE DIGNITY ANALYSIS
# ============================================================

def build_dignity_analysis(
    planets
):
    """
    Build the complete dignity analysis.
    """

    analysis = analyze_planets_dignity(
        planets
    )

    return {
        "planets": analysis,

        "strong_planets":
            get_strong_planets(
                analysis
            ),

        "weak_planets":
            get_weak_planets(
                analysis
            ),

        "exalted_planets":
            get_exalted_planets(
                analysis
            ),

        "debilitated_planets":
            get_debilitated_planets(
                analysis
            ),

        "total_planets":
            len(analysis),
    }


# ============================================================
# SIMPLE DIGNITY TABLE
# ============================================================

def build_dignity_table(
    planets
):
    """
    Create a frontend-friendly dignity table.
    """

    analysis = analyze_planets_dignity(
        planets
    )

    table = []

    for item in analysis:

        table.append({
            "planet": item["planet"],
            "sign": item["sign"],
            "sign_lord": item["sign_lord"],
            "dignity": item["dignity"],
            "score": item["dignity_score"],
            "strength": item["strength"],
        })

    return table


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("AI JYOTISH - DIGNITY MODULE TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Sample planets
    # --------------------------------------------------------

    sample_planets = [
        {
            "name": "Sun",
            "sign": "Aries",
            "sign_index": 0,
        },

        {
            "name": "Moon",
            "sign": "Taurus",
            "sign_index": 1,
        },

        {
            "name": "Mars",
            "sign": "Capricorn",
            "sign_index": 9,
        },

        {
            "name": "Mercury",
            "sign": "Virgo",
            "sign_index": 5,
        },

        {
            "name": "Jupiter",
            "sign": "Cancer",
            "sign_index": 3,
        },

        {
            "name": "Venus",
            "sign": "Pisces",
            "sign_index": 11,
        },

        {
            "name": "Saturn",
            "sign": "Aries",
            "sign_index": 0,
        },

        {
            "name": "Rahu",
            "sign": "Taurus",
            "sign_index": 1,
        },

        {
            "name": "Ketu",
            "sign": "Scorpio",
            "sign_index": 7,
        },
    ]

    # --------------------------------------------------------
    # Individual dignity tests
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("INDIVIDUAL DIGNITY TEST")
    print("-" * 70)

    for planet in sample_planets:

        result = analyze_planet_dignity(
            planet
        )

        print(
            f"{result['planet']:10} "
            f"{result['sign']:12} "
            f"-> "
            f"{result['dignity']:15} "
            f"Score: {result['dignity_score']:2} "
            f"Strength: {result['strength']}"
        )

    # --------------------------------------------------------
    # Exalted planets
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("EXALTED PLANETS")
    print("-" * 70)

    analysis = analyze_planets_dignity(
        sample_planets
    )

    exalted = get_exalted_planets(
        analysis
    )

    for planet in exalted:

        print(
            f"{planet['planet']} "
            f"in {planet['sign']}"
        )

    # --------------------------------------------------------
    # Debilitated planets
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("DEBILITATED PLANETS")
    print("-" * 70)

    debilitated = get_debilitated_planets(
        analysis
    )

    for planet in debilitated:

        print(
            f"{planet['planet']} "
            f"in {planet['sign']}"
        )

    # --------------------------------------------------------
    # Strong planets
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("STRONG PLANETS")
    print("-" * 70)

    strong = get_strong_planets(
        analysis
    )

    for planet in strong:

        print(
            f"{planet['planet']} "
            f"-> {planet['dignity']}"
        )

    # --------------------------------------------------------
    # Weak planets
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("WEAK PLANETS")
    print("-" * 70)

    weak = get_weak_planets(
        analysis
    )

    for planet in weak:

        print(
            f"{planet['planet']} "
            f"-> {planet['dignity']}"
        )

    # --------------------------------------------------------
    # Dignity table
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("DIGNITY TABLE")
    print("-" * 70)

    table = build_dignity_table(
        sample_planets
    )

    for row in table:

        print(
            f"{row['planet']:10} | "
            f"{row['sign']:12} | "
            f"Lord: {row['sign_lord']:8} | "
            f"{row['dignity']:15} | "
            f"Score: {row['score']:2}"
        )

    # --------------------------------------------------------
    # Enriched planets
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("ENRICHED PLANET TEST")
    print("-" * 70)

    enriched = enrich_planets_with_dignity(
        sample_planets
    )

    for planet in enriched:

        print(
            f"{planet['name']:10} "
            f"-> {planet.get('dignity')} "
            f"({planet.get('dignity_strength')})"
        )

    # --------------------------------------------------------
    # Complete analysis
    # --------------------------------------------------------

    print()
    print("-" * 70)
    print("COMPLETE ANALYSIS")
    print("-" * 70)

    complete = build_dignity_analysis(
        sample_planets
    )

    print(
        "Total planets:",
        complete["total_planets"]
    )

    print(
        "Exalted:",
        len(
            complete["exalted_planets"]
        )
    )

    print(
        "Debilitated:",
        len(
            complete["debilitated_planets"]
        )
    )

    print()
    print("=" * 70)
    print("DIGNITY MODULE TEST COMPLETED")
    print("=" * 70)