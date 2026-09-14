# =========================================================
# AI JYOTISH
# planets.py
#
# Planetary Analysis Engine
#
# This module does NOT calculate planetary positions again.
# It analyzes the positions already produced by ephemeris.py.
#
# Provides:
#   - Planet information
#   - Rashi
#   - Rashi lord
#   - House
#   - Nakshatra
#   - Retrograde status
#   - Planet nature
#   - Planet gender
#   - Element
#   - Quality
#   - Exaltation
#   - Debilitation
#   - Own signs
#   - Moolatrikona
#   - Dignity
#   - Functional helpers
#   - Planet summaries
# =========================================================


from ephemeris import (
    SIGNS,
    get_sign_lord,
)


# =========================================================
# PLANETS
# =========================================================

PLANET_ORDER = [
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


# =========================================================
# PLANET BASIC INFORMATION
# =========================================================

PLANET_INFO = {

    "Sun": {

        "sanskrit": "Surya",

        "symbol": "☉",

        "nature": "Malefic",

        "type": "Luminary",

        "gender": "Male",

        "element": "Fire",

        "quality": "Sattva",

        "day": "Sunday",

        "direction": "East",

        "exaltation_sign": "Mesha",

        "exaltation_degree": 10.0,

        "debilitation_sign": "Tula",

        "debilitation_degree": 10.0,

        "own_signs": [
            "Simha"
        ],

        "moolatrikona_sign": "Simha",

        "moolatrikona_start": 0.0,

        "moolatrikona_end": 20.0,

    },


    "Moon": {

        "sanskrit": "Chandra",

        "symbol": "☽",

        "nature": "Benefic",

        "type": "Luminary",

        "gender": "Female",

        "element": "Water",

        "quality": "Sattva",

        "day": "Monday",

        "direction": "North-West",

        "exaltation_sign": "Vrishabha",

        "exaltation_degree": 3.0,

        "debilitation_sign": "Vrishchika",

        "debilitation_degree": 3.0,

        "own_signs": [
            "Karka"
        ],

        "moolatrikona_sign": "Vrishabha",

        "moolatrikona_start": 4.0,

        "moolatrikona_end": 30.0,

    },


    "Mars": {

        "sanskrit": "Mangala",

        "symbol": "♂",

        "nature": "Malefic",

        "type": "Planet",

        "gender": "Male",

        "element": "Fire",

        "quality": "Tamas",

        "day": "Tuesday",

        "direction": "South",

        "exaltation_sign": "Makara",

        "exaltation_degree": 28.0,

        "debilitation_sign": "Karka",

        "debilitation_degree": 28.0,

        "own_signs": [
            "Mesha",
            "Vrishchika"
        ],

        "moolatrikona_sign": "Mesha",

        "moolatrikona_start": 0.0,

        "moolatrikona_end": 12.0,

    },


    "Mercury": {

        "sanskrit": "Budha",

        "symbol": "☿",

        "nature": "Benefic",

        "type": "Planet",

        "gender": "Neutral",

        "element": "Earth",

        "quality": "Rajas",

        "day": "Wednesday",

        "direction": "North",

        "exaltation_sign": "Kanya",

        "exaltation_degree": 15.0,

        "debilitation_sign": "Meena",

        "debilitation_degree": 15.0,

        "own_signs": [
            "Mithuna",
            "Kanya"
        ],

        "moolatrikona_sign": "Kanya",

        "moolatrikona_start": 16.0,

        "moolatrikona_end": 20.0,

    },


    "Jupiter": {

        "sanskrit": "Guru",

        "symbol": "♃",

        "nature": "Benefic",

        "type": "Planet",

        "gender": "Male",

        "element": "Ether",

        "quality": "Sattva",

        "day": "Thursday",

        "direction": "North-East",

        "exaltation_sign": "Karka",

        "exaltation_degree": 5.0,

        "debilitation_sign": "Makara",

        "debilitation_degree": 5.0,

        "own_signs": [
            "Dhanu",
            "Meena"
        ],

        "moolatrikona_sign": "Dhanu",

        "moolatrikona_start": 0.0,

        "moolatrikona_end": 10.0,

    },


    "Venus": {

        "sanskrit": "Shukra",

        "symbol": "♀",

        "nature": "Benefic",

        "type": "Planet",

        "gender": "Female",

        "element": "Water",

        "quality": "Rajas",

        "day": "Friday",

        "direction": "South-East",

        "exaltation_sign": "Meena",

        "exaltation_degree": 27.0,

        "debilitation_sign": "Kanya",

        "debilitation_degree": 27.0,

        "own_signs": [
            "Vrishabha",
            "Tula"
        ],

        "moolatrikona_sign": "Tula",

        "moolatrikona_start": 0.0,

        "moolatrikona_end": 15.0,

    },


    "Saturn": {

        "sanskrit": "Shani",

        "symbol": "♄",

        "nature": "Malefic",

        "type": "Planet",

        "gender": "Neutral",

        "element": "Air",

        "quality": "Tamas",

        "day": "Saturday",

        "direction": "West",

        "exaltation_sign": "Tula",

        "exaltation_degree": 20.0,

        "debilitation_sign": "Mesha",

        "debilitation_degree": 20.0,

        "own_signs": [
            "Makara",
            "Kumbha"
        ],

        "moolatrikona_sign": "Kumbha",

        "moolatrikona_start": 0.0,

        "moolatrikona_end": 20.0,

    },


    "Rahu": {

        "sanskrit": "Rahu",

        "symbol": "☊",

        "nature": "Malefic",

        "type": "Lunar Node",

        "gender": "Neutral",

        "element": "Air",

        "quality": "Tamas",

        "day": None,

        "direction": "South-West",

        "exaltation_sign": "Vrishabha",

        "exaltation_degree": None,

        "debilitation_sign": "Vrishchika",

        "debilitation_degree": None,

        "own_signs": [],

        "moolatrikona_sign": None,

        "moolatrikona_start": None,

        "moolatrikona_end": None,

    },


    "Ketu": {

        "sanskrit": "Ketu",

        "symbol": "☋",

        "nature": "Malefic",

        "type": "Lunar Node",

        "gender": "Neutral",

        "element": "Fire",

        "quality": "Tamas",

        "day": None,

        "direction": "South-West",

        "exaltation_sign": "Vrishchika",

        "exaltation_degree": None,

        "debilitation_sign": "Vrishabha",

        "debilitation_degree": None,

        "own_signs": [],

        "moolatrikona_sign": None,

        "moolatrikona_start": None,

        "moolatrikona_end": None,

    },

}


# =========================================================
# SIGN ELEMENTS
# =========================================================

SIGN_ELEMENTS = {

    "Mesha": "Fire",

    "Vrishabha": "Earth",

    "Mithuna": "Air",

    "Karka": "Water",

    "Simha": "Fire",

    "Kanya": "Earth",

    "Tula": "Air",

    "Vrishchika": "Water",

    "Dhanu": "Fire",

    "Makara": "Earth",

    "Kumbha": "Air",

    "Meena": "Water",

}


# =========================================================
# SIGN QUALITIES
# =========================================================

SIGN_QUALITIES = {

    "Mesha": "Movable",

    "Vrishabha": "Fixed",

    "Mithuna": "Dual",

    "Karka": "Movable",

    "Simha": "Fixed",

    "Kanya": "Dual",

    "Tula": "Movable",

    "Vrishchika": "Fixed",

    "Dhanu": "Dual",

    "Makara": "Movable",

    "Kumbha": "Fixed",

    "Meena": "Dual",

}


# =========================================================
# PLANET FRIENDSHIP
#
# Natural friendship.
# =========================================================

NATURAL_FRIENDS = {

    "Sun": [
        "Moon",
        "Mars",
        "Jupiter"
    ],

    "Moon": [
        "Sun",
        "Mercury"
    ],

    "Mars": [
        "Sun",
        "Moon",
        "Jupiter"
    ],

    "Mercury": [
        "Sun",
        "Venus"
    ],

    "Jupiter": [
        "Sun",
        "Moon",
        "Mars"
    ],

    "Venus": [
        "Mercury",
        "Saturn"
    ],

    "Saturn": [
        "Mercury",
        "Venus"
    ],

    "Rahu": [
        "Venus",
        "Saturn"
    ],

    "Ketu": [
        "Mars",
        "Jupiter"
    ],

}


NATURAL_ENEMIES = {

    "Sun": [
        "Venus",
        "Saturn"
    ],

    "Moon": [],

    "Mars": [
        "Mercury"
    ],

    "Mercury": [
        "Moon"
    ],

    "Jupiter": [
        "Mercury",
        "Venus"
    ],

    "Venus": [
        "Sun",
        "Moon"
    ],

    "Saturn": [
        "Sun",
        "Moon",
        "Mars"
    ],

    "Rahu": [
        "Sun",
        "Moon"
    ],

    "Ketu": [
        "Sun",
        "Moon"
    ],

}


# =========================================================
# NATURAL NEUTRALS
# =========================================================

NATURAL_NEUTRALS = {

    "Sun": [
        "Mercury"
    ],

    "Moon": [
        "Mars",
        "Jupiter",
        "Venus",
        "Saturn"
    ],

    "Mars": [
        "Venus",
        "Saturn"
    ],

    "Mercury": [
        "Mars",
        "Jupiter",
        "Saturn"
    ],

    "Jupiter": [
        "Saturn"
    ],

    "Venus": [
        "Mars",
        "Jupiter"
    ],

    "Saturn": [
        "Jupiter"
    ],

    "Rahu": [
        "Mercury"
    ],

    "Ketu": [
        "Mercury",
        "Venus",
        "Saturn"
    ],

}


# =========================================================
# GET PLANET INFORMATION
# =========================================================

def get_planet_info(
    planet_name
):
    """
    Return static information about a planet.
    """

    return PLANET_INFO.get(
        planet_name,
        {}
    ).copy()


# =========================================================
# GET PLANET NATURE
# =========================================================

def get_planet_nature(
    planet_name
):
    """
    Return natural benefic/malefic classification.
    """

    info = PLANET_INFO.get(
        planet_name,
        {}
    )

    return info.get(
        "nature"
    )


# =========================================================
# GET PLANET LORD
# =========================================================

def get_planet_sign_lord(
    sign_index
):
    """
    Return lord of a sign.
    """

    return get_sign_lord(
        int(sign_index)
    )


# =========================================================
# CHECK EXALTATION
# =========================================================

def is_exalted(
    planet_name,
    sign,
    degree=None
):
    """
    Check whether a planet is exalted.

    For normal planetary dignity:
        sign match is sufficient.

    Degree is used to identify exact exaltation
    degree when available.
    """

    info = PLANET_INFO.get(
        planet_name
    )

    if not info:
        return False

    if info.get(
        "exaltation_sign"
    ) != sign:

        return False

    return True


# =========================================================
# CHECK DEBILITATION
# =========================================================

def is_debilitated(
    planet_name,
    sign,
    degree=None
):
    """
    Check whether a planet is debilitated.
    """

    info = PLANET_INFO.get(
        planet_name
    )

    if not info:
        return False

    if info.get(
        "debilitation_sign"
    ) != sign:

        return False

    return True


# =========================================================
# CHECK OWN SIGN
# =========================================================

def is_own_sign(
    planet_name,
    sign
):
    """
    Check whether planet is in its own sign.
    """

    info = PLANET_INFO.get(
        planet_name
    )

    if not info:
        return False

    return sign in info.get(
        "own_signs",
        []
    )


# =========================================================
# CHECK MOOLATRIKONA
# =========================================================

def is_moolatrikona(
    planet_name,
    sign,
    degree=None
):
    """
    Check Moolatrikona placement.

    Degree range is used when available.
    """

    info = PLANET_INFO.get(
        planet_name
    )

    if not info:
        return False

    mt_sign = info.get(
        "moolatrikona_sign"
    )

    if mt_sign is None:
        return False

    if sign != mt_sign:
        return False

    if degree is None:
        return True

    start = info.get(
        "moolatrikona_start"
    )

    end = info.get(
        "moolatrikona_end"
    )

    if start is None or end is None:
        return True

    try:

        degree = float(
            degree
        )

    except (
        TypeError,
        ValueError
    ):

        return True

    return (
        start
        <= degree
        <= end
    )


# =========================================================
# GET DIGNITY
# =========================================================

def get_dignity(
    planet_name,
    sign,
    degree=None
):
    """
    Determine basic planetary dignity.

    Priority:
        Exalted
        Debilitated
        Moolatrikona
        Own Sign
        Neutral
    """

    if is_exalted(
        planet_name,
        sign,
        degree
    ):

        return "Exalted"


    if is_debilitated(
        planet_name,
        sign,
        degree
    ):

        return "Debilitated"


    if is_moolatrikona(
        planet_name,
        sign,
        degree
    ):

        return "Moolatrikona"


    if is_own_sign(
        planet_name,
        sign
    ):

        return "Own Sign"


    return "Neutral"


# =========================================================
# NATURAL RELATIONSHIP
# =========================================================

def get_natural_relationship(
    planet_name,
    other_planet
):
    """
    Return natural relationship between two planets.
    """

    if (
        planet_name == other_planet
    ):

        return "Same"


    if other_planet in NATURAL_FRIENDS.get(
        planet_name,
        []
    ):

        return "Friend"


    if other_planet in NATURAL_ENEMIES.get(
        planet_name,
        []
    ):

        return "Enemy"


    return "Neutral"


# =========================================================
# GET SIGN DETAILS
# =========================================================

def get_sign_details(
    sign_index
):
    """
    Return details of a zodiac sign.
    """

    sign_index = int(
        sign_index
    ) % 12

    sign = SIGNS[
        sign_index
    ]

    return {

        "sign":
            sign,

        "sign_index":
            sign_index,

        "lord":
            get_sign_lord(
                sign_index
            ),

        "element":
            SIGN_ELEMENTS.get(
                sign
            ),

        "quality":
            SIGN_QUALITIES.get(
                sign
            ),

    }


# =========================================================
# ANALYZE ONE PLANET
# =========================================================

def analyze_planet(
    planet
):
    """
    Enrich one planetary position.

    Input example:

        {
            "name": "Sun",
            "sign": "Mesha",
            "sign_index": 0,
            "degree": 12.5,
            "house": 1,
            "retrograde": False
        }

    Returns the original data plus detailed analysis.
    """

    if not isinstance(
        planet,
        dict
    ):

        raise TypeError(
            "Planet must be a dictionary."
        )


    result = planet.copy()


    # =====================================================
    # BASIC VALUES
    # =====================================================

    name = result.get(
        "name"
    )

    sign = result.get(
        "sign"
    )

    sign_index = result.get(
        "sign_index"
    )

    degree = result.get(
        "degree"
    )


    # =====================================================
    # VALIDATE PLANET NAME
    # =====================================================

    if name not in PLANET_INFO:

        raise ValueError(
            f"Unknown planet: {name}"
        )


    # =====================================================
    # STATIC INFORMATION
    # =====================================================

    info = get_planet_info(
        name
    )


    result["sanskrit"] = info.get(
        "sanskrit"
    )

    result["symbol"] = info.get(
        "symbol"
    )

    result["nature"] = info.get(
        "nature"
    )

    result["planet_type"] = info.get(
        "type"
    )

    result["gender"] = info.get(
        "gender"
    )

    result["element"] = info.get(
        "element"
    )

    result["quality"] = info.get(
        "quality"
    )

    result["day"] = info.get(
        "day"
    )

    result["direction"] = info.get(
        "direction"
    )


    # =====================================================
    # SIGN INFORMATION
    # =====================================================

    if sign_index is not None:

        sign_details = get_sign_details(
            sign_index
        )

        result["sign_details"] = (
            sign_details
        )

        result["rashi_lord"] = (
            sign_details["lord"]
        )

        result["sign_element"] = (
            sign_details["element"]
        )

        result["sign_quality"] = (
            sign_details["quality"]
        )

    elif sign:

        try:

            sign_index = SIGNS.index(
                sign
            )

            sign_details = get_sign_details(
                sign_index
            )

            result["sign_index"] = (
                sign_index
            )

            result["sign_details"] = (
                sign_details
            )

            result["rashi_lord"] = (
                sign_details["lord"]
            )

            result["sign_element"] = (
                sign_details["element"]
            )

            result["sign_quality"] = (
                sign_details["quality"]
            )

        except ValueError:

            pass


    # =====================================================
    # DIGNITY
    # =====================================================

    result["dignity"] = get_dignity(

        name,

        sign,

        degree

    )


    # =====================================================
    # EXALTATION
    # =====================================================

    result["exalted"] = is_exalted(

        name,

        sign,

        degree

    )


    # =====================================================
    # DEBILITATION
    # =====================================================

    result["debilitated"] = is_debilitated(

        name,

        sign,

        degree

    )


    # =====================================================
    # OWN SIGN
    # =====================================================

    result["own_sign"] = is_own_sign(

        name,

        sign

    )


    # =====================================================
    # MOOLATRIKONA
    # =====================================================

    result["moolatrikona"] = (
        is_moolatrikona(
            name,
            sign,
            degree
        )
    )


    # =====================================================
    # RETROGRADE
    # =====================================================

    result["retrograde"] = bool(
        result.get(
            "retrograde",
            False
        )
    )


    # =====================================================
    # MOTION
    # =====================================================

    if result["retrograde"]:

        result["motion"] = (
            "Retrograde"
        )

    else:

        result["motion"] = (
            "Direct"
        )


    # =====================================================
    # HOUSE
    # =====================================================

    house = result.get(
        "house"
    )

    if house is not None:

        try:

            house = int(
                house
            )

            result["house"] = house

        except (
            TypeError,
            ValueError
        ):

            pass


    # =====================================================
    # SUMMARY
    # =====================================================

    result["summary"] = (
        build_planet_description(
            result
        )
    )


    return result


# =========================================================
# ANALYZE ALL PLANETS
# =========================================================

def analyze_planets(
    planets
):
    """
    Analyze every planet in a calculated planet list.
    """

    if not isinstance(
        planets,
        list
    ):

        raise TypeError(
            "Planets must be a list."
        )


    analyzed = []

    for planet in planets:

        analyzed.append(

            analyze_planet(
                planet
            )

        )

    return analyzed


# =========================================================
# BUILD PLANET DESCRIPTION
# =========================================================

def build_planet_description(
    planet
):
    """
    Build a readable short description.
    """

    name = planet.get(
        "name",
        "Planet"
    )

    sign = planet.get(
        "sign",
        "-"
    )

    degree_dms = planet.get(
        "degree_dms"
    )

    house = planet.get(
        "house"
    )

    dignity = planet.get(
        "dignity",
        "Neutral"
    )

    motion = planet.get(
        "motion",
        "Direct"
    )


    parts = []

    parts.append(
        f"{name} is in {sign}"
    )


    if degree_dms:

        parts.append(
            f"at {degree_dms}"
        )


    if house is not None:

        parts.append(
            f"in House {house}"
        )


    parts.append(
        f"with {dignity} dignity"
    )


    if motion == "Retrograde":

        parts.append(
            "and is retrograde"
        )


    return " ".join(
        parts
    ) + "."


# =========================================================
# GET STRONG PLANETS
# =========================================================

def get_strong_planets(
    planets
):
    """
    Return planets having classical strong dignity.

    Strong dignity:
        Exalted
        Moolatrikona
        Own Sign
    """

    strong = []

    for planet in planets:

        dignity = planet.get(
            "dignity"
        )

        if dignity in (
            "Exalted",
            "Moolatrikona",
            "Own Sign"
        ):

            strong.append(
                planet
            )

    return strong


# =========================================================
# GET WEAK PLANETS
# =========================================================

def get_weak_planets(
    planets
):
    """
    Return debilitated planets.
    """

    weak = []

    for planet in planets:

        if planet.get(
            "dignity"
        ) == "Debilitated":

            weak.append(
                planet
            )

    return weak


# =========================================================
# GET RETROGRADE PLANETS
# =========================================================

def get_retrograde_planets(
    planets
):
    """
    Return all retrograde planets.
    """

    return [

        planet

        for planet in planets

        if planet.get(
            "retrograde",
            False
        )

    ]


# =========================================================
# GET PLANETS IN HOUSE
# =========================================================

def get_planets_in_house(
    planets,
    house
):
    """
    Return planets occupying a particular house.
    """

    try:

        house = int(
            house
        )

    except (
        TypeError,
        ValueError
    ):

        return []


    return [

        planet

        for planet in planets

        if planet.get(
            "house"
        ) == house

    ]


# =========================================================
# GET PLANETS IN SIGN
# =========================================================

def get_planets_in_sign(
    planets,
    sign
):
    """
    Return planets occupying a particular sign.
    """

    return [

        planet

        for planet in planets

        if planet.get(
            "sign"
        ) == sign

    ]


# =========================================================
# GET PLANET BY NAME
# =========================================================

def get_planet(
    planets,
    name
):
    """
    Find one planet.
    """

    for planet in planets:

        if planet.get(
            "name"
        ) == name:

            return planet

    return None


# =========================================================
# CREATE PLANET TABLE
# =========================================================

def build_planet_table(
    planets
):
    """
    Build frontend-friendly planetary table data.
    """

    table = []

    for planet in planets:

        table.append({

            "name":
                planet.get(
                    "name"
                ),

            "sanskrit":
                planet.get(
                    "sanskrit"
                ),

            "symbol":
                planet.get(
                    "symbol"
                ),

            "sign":
                planet.get(
                    "sign"
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

            "motion":
                planet.get(
                    "motion"
                ),

            "dignity":
                planet.get(
                    "dignity"
                ),

            "nature":
                planet.get(
                    "nature"
                ),

            "exalted":
                planet.get(
                    "exalted",
                    False
                ),

            "debilitated":
                planet.get(
                    "debilitated",
                    False
                ),

            "own_sign":
                planet.get(
                    "own_sign",
                    False
                ),

            "moolatrikona":
                planet.get(
                    "moolatrikona",
                    False
                ),

        })

    return table


# =========================================================
# BUILD COMPLETE PLANETARY ANALYSIS
# =========================================================

def build_planetary_analysis(
    planets
):
    """
    Create a complete planetary analysis object.
    """

    analyzed = analyze_planets(
        planets
    )

    return {

        "planets":
            analyzed,

        "table":
            build_planet_table(
                analyzed
            ),

        "strong_planets":
            get_strong_planets(
                analyzed
            ),

        "weak_planets":
            get_weak_planets(
                analyzed
            ),

        "retrograde_planets":
            get_retrograde_planets(
                analyzed
            ),

        "count":
            len(analyzed),

    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print()

    print("=" * 78)

    print(
        "AI JYOTISH - PLANETARY ANALYSIS ENGINE TEST"
    )

    print("=" * 78)


    # -----------------------------------------------------
    # SAMPLE DATA
    #
    # This uses the same structure produced by
    # ephemeris.calculate_planets().
    # -----------------------------------------------------

    sample_planets = [

        {

            "name": "Sun",

            "sign": "Mesha",

            "sign_index": 0,

            "degree": 12.5,

            "degree_dms": "12°30′00″",

            "longitude": 12.5,

            "longitude_dms": "12°30′00″",

            "house": 1,

            "retrograde": False,

            "speed": 0.95,

        },

        {

            "name": "Moon",

            "sign": "Vrishabha",

            "sign_index": 1,

            "degree": 8.25,

            "degree_dms": "8°15′00″",

            "longitude": 38.25,

            "longitude_dms": "38°15′00″",

            "house": 2,

            "retrograde": False,

            "speed": 13.2,

        },

        {

            "name": "Mars",

            "sign": "Makara",

            "sign_index": 9,

            "degree": 20.0,

            "degree_dms": "20°00′00″",

            "longitude": 290.0,

            "longitude_dms": "290°00′00″",

            "house": 10,

            "retrograde": False,

            "speed": 0.5,

        },

        {

            "name": "Mercury",

            "sign": "Kanya",

            "sign_index": 5,

            "degree": 18.0,

            "degree_dms": "18°00′00″",

            "longitude": 168.0,

            "longitude_dms": "168°00′00″",

            "house": 6,

            "retrograde": False,

            "speed": 1.2,

        },

        {

            "name": "Jupiter",

            "sign": "Karka",

            "sign_index": 3,

            "degree": 5.0,

            "degree_dms": "5°00′00″",

            "longitude": 95.0,

            "longitude_dms": "95°00′00″",

            "house": 4,

            "retrograde": False,

            "speed": 0.1,

        },

        {

            "name": "Venus",

            "sign": "Meena",

            "sign_index": 11,

            "degree": 27.0,

            "degree_dms": "27°00′00″",

            "longitude": 357.0,

            "longitude_dms": "357°00′00″",

            "house": 12,

            "retrograde": False,

            "speed": 1.0,

        },

        {

            "name": "Saturn",

            "sign": "Tula",

            "sign_index": 6,

            "degree": 20.0,

            "degree_dms": "20°00′00″",

            "longitude": 200.0,

            "longitude_dms": "200°00′00″",

            "house": 7,

            "retrograde": True,

            "speed": -0.05,

        },

        {

            "name": "Rahu",

            "sign": "Mithuna",

            "sign_index": 2,

            "degree": 15.0,

            "degree_dms": "15°00′00″",

            "longitude": 75.0,

            "longitude_dms": "75°00′00″",

            "house": 3,

            "retrograde": True,

            "speed": -0.05,

        },

        {

            "name": "Ketu",

            "sign": "Dhanu",

            "sign_index": 8,

            "degree": 15.0,

            "degree_dms": "15°00′00″",

            "longitude": 255.0,

            "longitude_dms": "255°00′00″",

            "house": 9,

            "retrograde": True,

            "speed": -0.05,

        },

    ]


    # =====================================================
    # RUN ANALYSIS
    # =====================================================

    analysis = build_planetary_analysis(
        sample_planets
    )


    # =====================================================
    # PRINT RESULTS
    # =====================================================

    print()

    print(
        "✓ PLANETARY ANALYSIS COMPLETED"
    )

    print()

    print(
        f'Total planets: {analysis["count"]}'
    )


    print()

    print(
        "PLANETARY DETAILS"
    )

    print("-" * 78)


    for planet in analysis["planets"]:

        print()

        print(
            f'Planet: {planet["name"]}'
        )

        print(
            f'  Rashi: {planet.get("sign")}'
        )

        print(
            f'  Degree: {planet.get("degree_dms")}'
        )

        print(
            f'  House: {planet.get("house")}'
        )

        print(
            f'  Rashi Lord: {planet.get("rashi_lord")}'
        )

        print(
            f'  Nature: {planet.get("nature")}'
        )

        print(
            f'  Dignity: {planet.get("dignity")}'
        )

        print(
            f'  Retrograde: {planet.get("retrograde")}'
        )

        print(
            f'  Exalted: {planet.get("exalted")}'
        )

        print(
            f'  Debilitated: {planet.get("debilitated")}'
        )

        print(
            f'  Own Sign: {planet.get("own_sign")}'
        )

        print(
            f'  Moolatrikona: '
            f'{planet.get("moolatrikona")}'
        )


    # =====================================================
    # STRONG PLANETS
    # =====================================================

    print()

    print(
        "STRONG PLANETS"
    )

    print("-" * 78)

    for planet in analysis[
        "strong_planets"
    ]:

        print(

            "-",

            planet.get(
                "name"
            ),

            "(",

            planet.get(
                "dignity"
            ),

            ")"

        )


    # =====================================================
    # WEAK PLANETS
    # =====================================================

    print()

    print(
        "DEBILITATED PLANETS"
    )

    print("-" * 78)

    for planet in analysis[
        "weak_planets"
    ]:

        print(

            "-",

            planet.get(
                "name"
            )

        )


    # =====================================================
    # RETROGRADE PLANETS
    # =====================================================

    print()

    print(
        "RETROGRADE PLANETS"
    )

    print("-" * 78)

    for planet in analysis[
        "retrograde_planets"
    ]:

        print(

            "-",

            planet.get(
                "name"
            )

        )


    # =====================================================
    # FINISHED
    # =====================================================

    print()

    print("=" * 78)

    print(
        "✓ PLANETS.PY TEST COMPLETED"
    )

    print("=" * 78)

    print()