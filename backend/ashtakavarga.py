"""
AI Jyotish - Ashtakavarga Engine

Calculates:
    - Bhinnashtakavarga (BAV)
    - Sarvashtakavarga (SAV)
    - Planet-wise Ashtakavarga
    - Sign-wise scores
    - House-wise scores
    - Strong / weak houses
    - Transit-friendly signs

The implementation uses the standard sign-based Ashtakavarga
framework and is designed to work with the existing AI Jyotish
planet dictionaries.

Planet sign_index convention:
    Aries      = 0
    Taurus     = 1
    Gemini     = 2
    Cancer     = 3
    Leo        = 4
    Virgo      = 5
    Libra      = 6
    Scorpio    = 7
    Sagittarius= 8
    Capricorn  = 9
    Aquarius   = 10
    Pisces     = 11

Note:
Ashtakavarga has traditional rule variations between schools.
This module uses a standard Parashari-style sign-based framework.
"""

# ============================================================
# CONSTANTS
# ============================================================

SIGNS = [
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


ASHTAKAVARGA_PLANETS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
]


REFERENCE_PLANETS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Ascendant",
]


# ============================================================
# STANDARD BAV CONTRIBUTION TABLES
# ============================================================
#
# Each list contains the houses counted from the reference
# planet/ascendant which contribute one bindu to the target
# planet.
#
# Example:
#     Sun's BAV from Sun/Moon/etc.
#
# The values are house numbers, 1 through 12.
# ============================================================

BAV_RULES = {

    "Sun": {
        "Sun":      [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon":     [3, 6, 10, 11],
        "Mars":     [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury":  [3, 5, 6, 9, 10, 11, 12],
        "Jupiter":  [5, 6, 9, 11],
        "Venus":    [6, 7, 12],
        "Saturn":   [1, 2, 4, 7, 8, 10, 11],
        "Ascendant":[3, 4, 6, 10, 11, 12],
    },

    "Moon": {
        "Sun":      [3, 6, 7, 8, 10, 11],
        "Moon":     [1, 3, 6, 7, 10, 11],
        "Mars":     [2, 3, 5, 6, 9, 10, 11],
        "Mercury":  [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter":  [1, 4, 7, 8, 10, 11, 12],
        "Venus":    [3, 4, 5, 7, 9, 10, 11],
        "Saturn":   [3, 5, 6, 11],
        "Ascendant":[3, 6, 10, 11],
    },

    "Mars": {
        "Sun":      [3, 5, 6, 10, 11],
        "Moon":     [3, 6, 11],
        "Mars":     [1, 2, 4, 7, 8, 10, 11],
        "Mercury":  [1, 3, 6, 10, 11],
        "Jupiter":  [6, 10, 11, 12],
        "Venus":    [6, 8, 11, 12],
        "Saturn":   [1, 4, 7, 8, 10, 11],
        "Ascendant":[1, 3, 5, 6, 10, 11],
    },

    "Mercury": {
        "Sun":      [5, 6, 9, 11, 12],
        "Moon":     [2, 4, 6, 8, 10, 11],
        "Mars":     [1, 2, 4, 8, 10, 11],
        "Mercury":  [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter":  [6, 8, 11, 12],
        "Venus":    [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn":   [1, 2, 4, 7, 8, 10, 11],
        "Ascendant":[1, 2, 4, 6, 8, 10, 11],
    },

    "Jupiter": {
        "Sun":      [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon":     [2, 5, 7, 9, 11],
        "Mars":     [1, 2, 4, 7, 8, 10, 11],
        "Mercury":  [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter":  [2, 3, 4, 5, 8, 9, 11],
        "Venus":    [2, 5, 6, 9, 10, 11],
        "Saturn":   [3, 5, 6, 12],
        "Ascendant":[1, 2, 4, 5, 6, 8, 9, 10, 11],
    },

    "Venus": {
        "Sun":      [8, 11, 12],
        "Moon":     [1, 2, 3, 4, 5, 8, 9, 11],
        "Mars":     [3, 5, 6, 9, 11, 12],
        "Mercury":  [3, 5, 6, 9, 11],
        "Jupiter":  [5, 8, 9, 10, 11],
        "Venus":    [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Saturn":   [3, 4, 5, 8, 9, 10, 11],
        "Ascendant":[1, 2, 3, 4, 5, 8, 9, 11],
    },

    "Saturn": {
        "Sun":      [1, 2, 4, 7, 8, 10, 11],
        "Moon":     [3, 6, 11],
        "Mars":     [3, 5, 6, 10, 11, 12],
        "Mercury":  [6, 8, 9, 10, 11, 12],
        "Jupiter":  [5, 6, 11, 12],
        "Venus":    [6, 8, 11, 12],
        "Saturn":   [3, 5, 6, 11],
        "Ascendant":[1, 3, 4, 6, 10, 11],
    },
}


# ============================================================
# HELPERS
# ============================================================

def normalize_planet_name(name):
    """Normalize common planet names."""

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

        "ascendant": "Ascendant",
        "lagna": "Ascendant",
    }

    return aliases.get(str(name).strip().lower())


def validate_sign_index(sign_index):
    """Validate a zodiac sign index."""

    try:
        sign_index = int(sign_index)
    except (TypeError, ValueError):
        return False

    return 0 <= sign_index <= 11


def normalize_sign_index(sign_index):
    """Normalize sign index."""

    try:
        return int(sign_index) % 12
    except (TypeError, ValueError):
        return None


def get_sign_name(sign_index):
    """Return sign name."""

    sign_index = normalize_sign_index(sign_index)

    if sign_index is None:
        return None

    return SIGNS[sign_index]


def house_from_reference(reference_sign, target_sign):
    """
    Calculate house/sign distance.

    If reference = Aries (0)
    and target = Gemini (2)

    result = 3
    because Gemini is the 3rd sign from Aries.
    """

    reference_sign = normalize_sign_index(reference_sign)
    target_sign = normalize_sign_index(target_sign)

    if reference_sign is None or target_sign is None:
        return None

    return ((target_sign - reference_sign) % 12) + 1


def get_planet_sign(planets, planet_name):
    """Find a planet's sign index."""

    target = normalize_planet_name(planet_name)

    if target == "Ascendant":

        if isinstance(planets, dict):

            ascendant = planets.get("ascendant")

            if isinstance(ascendant, dict):
                value = ascendant.get("sign_index")

                if validate_sign_index(value):
                    return int(value)

            value = planets.get("ascendant_sign_index")

            if validate_sign_index(value):
                return int(value)

        return None

    if isinstance(planets, dict):

        if target in planets:
            item = planets[target]

            if isinstance(item, dict):
                value = item.get("sign_index")

                if validate_sign_index(value):
                    return int(value)

        planet_list = planets.get("planets")

        if isinstance(planet_list, list):
            planets = planet_list

    if isinstance(planets, list):

        for planet in planets:

            if not isinstance(planet, dict):
                continue

            name = normalize_planet_name(
                planet.get("name")
            )

            if name == target:

                value = planet.get("sign_index")

                if validate_sign_index(value):
                    return int(value)

    return None


# ============================================================
# BAV
# ============================================================

def calculate_bav_for_planet(
    target_planet,
    planets,
):
    """
    Calculate Bhinnashtakavarga for one planet.

    Returns a list of 12 values (0/1).
    """

    target = normalize_planet_name(target_planet)

    if target not in ASHTAKAVARGA_PLANETS:
        return [0] * 12

    result = [0] * 12

    rules = BAV_RULES.get(target, {})

    for reference in REFERENCE_PLANETS:

        reference_sign = get_planet_sign(
            planets,
            reference,
        )

        if reference_sign is None:
            continue

        allowed_houses = rules.get(
            reference,
            []
        )

        for target_sign in range(12):

            house_number = house_from_reference(
                reference_sign,
                target_sign,
            )

            if house_number in allowed_houses:
                result[target_sign] = 1

    return result


def calculate_all_bav(planets):
    """Calculate BAV for all seven planets."""

    result = {}

    for planet in ASHTAKAVARGA_PLANETS:

        result[planet] = (
            calculate_bav_for_planet(
                planet,
                planets,
            )
        )

    return result


# ============================================================
# BAV TOTALS
# ============================================================

def calculate_bav_total(bav):
    """Calculate total bindus in a BAV."""

    if not isinstance(bav, list):
        return 0

    return sum(
        1
        for value in bav
        if value
    )


def calculate_bav_sign_totals(bav):
    """
    Return BAV values as sign-labelled data.
    """

    if not isinstance(bav, list):
        return []

    return [
        {
            "sign_index": index,
            "sign": SIGNS[index],
            "bindus": int(bool(value)),
        }
        for index, value in enumerate(bav)
    ]


# ============================================================
# SARVASHTAKAVARGA
# ============================================================

def calculate_sarvashtakavarga(bav_data):
    """
    Calculate Sarvashtakavarga.

    SAV = sum of BAV values of all seven planets.
    """

    result = [0] * 12

    if not isinstance(bav_data, dict):
        return result

    for planet in ASHTAKAVARGA_PLANETS:

        values = bav_data.get(planet)

        if not isinstance(values, list):
            continue

        for index in range(
            min(12, len(values))
        ):

            result[index] += int(
                bool(values[index])
            )

    return result


def get_sarvashtakavarga_total(sav):
    """Return total SAV bindus."""

    if not isinstance(sav, list):
        return 0

    return sum(sav)


def build_sav_table(sav):
    """Build sign-wise SAV table."""

    if not isinstance(sav, list):
        return []

    return [
        {
            "sign_index": index,
            "sign": SIGNS[index],
            "bindus": int(value),
        }
        for index, value in enumerate(sav)
    ]


# ============================================================
# HOUSE MAPPING
# ============================================================

def sign_to_house(sign_index, ascendant_sign):
    """Convert sign index into Whole Sign house number."""

    sign_index = normalize_sign_index(sign_index)
    ascendant_sign = normalize_sign_index(
        ascendant_sign
    )

    if sign_index is None or ascendant_sign is None:
        return None

    return (
        (sign_index - ascendant_sign) % 12
    ) + 1


def build_house_sav(sav, ascendant_sign):
    """
    Convert sign-based SAV into house-based SAV.
    """

    if not isinstance(sav, list):
        return []

    result = []

    for sign_index, bindus in enumerate(sav):

        house = sign_to_house(
            sign_index,
            ascendant_sign,
        )

        result.append({
            "house": house,
            "sign_index": sign_index,
            "sign": SIGNS[sign_index],
            "bindus": int(bindus),
        })

    result.sort(
        key=lambda item: item["house"]
    )

    return result


# ============================================================
# ANALYSIS
# ============================================================

def classify_sav_score(score):
    """Classify SAV strength."""

    try:
        score = int(score)
    except (TypeError, ValueError):
        return "Unknown"

    if score >= 35:
        return "Excellent"

    if score >= 30:
        return "Strong"

    if score >= 25:
        return "Moderate"

    if score >= 20:
        return "Weak"

    return "Very Weak"


def get_strong_sav_signs(sav, minimum=30):
    """Return signs with strong SAV."""

    if not isinstance(sav, list):
        return []

    return [
        {
            "sign_index": index,
            "sign": SIGNS[index],
            "bindus": int(value),
        }
        for index, value in enumerate(sav)
        if value >= minimum
    ]


def get_weak_sav_signs(sav, maximum=24):
    """Return signs with weak SAV."""

    if not isinstance(sav, list):
        return []

    return [
        {
            "sign_index": index,
            "sign": SIGNS[index],
            "bindus": int(value),
        }
        for index, value in enumerate(sav)
        if value <= maximum
    ]


def get_strong_sav_houses(
    sav,
    ascendant_sign,
    minimum=30,
):
    """Return houses with strong SAV."""

    house_data = build_house_sav(
        sav,
        ascendant_sign,
    )

    return [
        item
        for item in house_data
        if item["bindus"] >= minimum
    ]


def get_weak_sav_houses(
    sav,
    ascendant_sign,
    maximum=24,
):
    """Return houses with weak SAV."""

    house_data = build_house_sav(
        sav,
        ascendant_sign,
    )

    return [
        item
        for item in house_data
        if item["bindus"] <= maximum
    ]


# ============================================================
# PLANET-SPECIFIC ANALYSIS
# ============================================================

def analyze_bav_planet(
    planet,
    bav,
):
    """Analyze one planet's BAV."""

    total = calculate_bav_total(bav)

    sign_data = calculate_bav_sign_totals(
        bav
    )

    strongest = sorted(
        sign_data,
        key=lambda item: item["bindus"],
        reverse=True,
    )

    return {
        "planet": planet,
        "total_bindus": total,
        "signs": sign_data,
        "strong_signs": [
            item["sign"]
            for item in strongest
            if item["bindus"] == 1
        ],
    }


def analyze_all_bav(bav_data):
    """Analyze all BAV data."""

    result = {}

    for planet in ASHTAKAVARGA_PLANETS:

        bav = bav_data.get(
            planet,
            [0] * 12,
        )

        result[planet] = analyze_bav_planet(
            planet,
            bav,
        )

    return result


# ============================================================
# COMPLETE ENGINE
# ============================================================

def build_ashtakavarga_analysis(
    planets,
    ascendant_sign=None,
):
    """
    Build complete Ashtakavarga analysis.

    Parameters
    ----------
    planets:
        Existing project planet list or chart dictionary.

    ascendant_sign:
        Optional Ascendant sign index.
        If omitted, the function attempts to obtain it
        from the chart dictionary.
    """

    # --------------------------------------------------------
    # Ascendant
    # --------------------------------------------------------

    if ascendant_sign is None:
        ascendant_sign = get_planet_sign(
            planets,
            "Ascendant",
        )

    # --------------------------------------------------------
    # BAV
    # --------------------------------------------------------

    bav_data = calculate_all_bav(
        planets
    )

    # --------------------------------------------------------
    # SAV
    # --------------------------------------------------------

    sav = calculate_sarvashtakavarga(
        bav_data
    )

    sav_total = get_sarvashtakavarga_total(
        sav
    )

    # --------------------------------------------------------
    # BAV analysis
    # --------------------------------------------------------

    bav_analysis = analyze_all_bav(
        bav_data
    )

    # --------------------------------------------------------
    # Sign analysis
    # --------------------------------------------------------

    sign_analysis = []

    for index, score in enumerate(sav):

        sign_analysis.append({
            "sign_index": index,
            "sign": SIGNS[index],
            "bindus": int(score),
            "classification": classify_sav_score(
                score
            ),
        })

    # --------------------------------------------------------
    # House analysis
    # --------------------------------------------------------

    house_analysis = []

    if ascendant_sign is not None:

        house_data = build_house_sav(
            sav,
            ascendant_sign,
        )

        for item in house_data:

            house_analysis.append({
                **item,
                "classification":
                    classify_sav_score(
                        item["bindus"]
                    ),
            })

    # --------------------------------------------------------
    # Strong / weak signs
    # --------------------------------------------------------

    strong_signs = get_strong_sav_signs(
        sav
    )

    weak_signs = get_weak_sav_signs(
        sav
    )

    # --------------------------------------------------------
    # Strong / weak houses
    # --------------------------------------------------------

    strong_houses = []

    weak_houses = []

    if ascendant_sign is not None:

        strong_houses = get_strong_sav_houses(
            sav,
            ascendant_sign,
        )

        weak_houses = get_weak_sav_houses(
            sav,
            ascendant_sign,
        )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    return {
        "bhinna_ashtakavarga": bav_data,

        "bav_analysis": bav_analysis,

        "sarvashtakavarga": sav,

        "sarvashtakavarga_total": sav_total,

        "sign_analysis": sign_analysis,

        "house_analysis": house_analysis,

        "strong_signs": strong_signs,

        "weak_signs": weak_signs,

        "strong_houses": strong_houses,

        "weak_houses": weak_houses,

        "ascendant_sign_index": ascendant_sign,

        "ascendant_sign":
            get_sign_name(ascendant_sign),
    }


# ============================================================
# TRANSIT SUPPORT
# ============================================================

def get_transit_score(
    sav,
    transit_sign_index,
):
    """
    Get SAV score for a transit sign.

    Higher bindus generally indicate a more supportive
    transit environment.
    """

    transit_sign_index = normalize_sign_index(
        transit_sign_index
    )

    if (
        transit_sign_index is None
        or not isinstance(sav, list)
        or len(sav) < 12
    ):
        return None

    score = int(
        sav[transit_sign_index]
    )

    return {
        "sign_index": transit_sign_index,
        "sign": SIGNS[transit_sign_index],
        "bindus": score,
        "classification":
            classify_sav_score(score),
    }


def get_supportive_transit_signs(
    sav,
    minimum=30,
):
    """Return signs suitable for stronger transit support."""

    if not isinstance(sav, list):
        return []

    return [
        {
            "sign_index": index,
            "sign": SIGNS[index],
            "bindus": int(value),
        }
        for index, value in enumerate(sav)
        if value >= minimum
    ]


# ============================================================
# COMPACT SUMMARY
# ============================================================

def build_ashtakavarga_summary(analysis):
    """Create a compact summary."""

    if not isinstance(analysis, dict):
        return {}

    sav = analysis.get(
        "sarvashtakavarga",
        [],
    )

    if not sav:
        return {
            "total_bindus": 0,
            "strongest_sign": None,
            "weakest_sign": None,
        }

    strongest_index = max(
        range(12),
        key=lambda index: sav[index],
    )

    weakest_index = min(
        range(12),
        key=lambda index: sav[index],
    )

    return {
        "total_bindus":
            get_sarvashtakavarga_total(sav),

        "strongest_sign":
            SIGNS[strongest_index],

        "strongest_sign_bindus":
            int(sav[strongest_index]),

        "weakest_sign":
            SIGNS[weakest_index],

        "weakest_sign_bindus":
            int(sav[weakest_index]),

        "strong_sign_count":
            len(
                analysis.get(
                    "strong_signs",
                    [],
                )
            ),

        "weak_sign_count":
            len(
                analysis.get(
                    "weak_signs",
                    [],
                )
            ),
    }


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("ASHTAKAVARGA MODULE TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Sample chart
    # --------------------------------------------------------

    sample_planets = [
        {
            "name": "Sun",
            "sign_index": 0,
            "longitude": 15.0,
        },
        {
            "name": "Moon",
            "sign_index": 3,
            "longitude": 100.0,
        },
        {
            "name": "Mars",
            "sign_index": 9,
            "longitude": 280.0,
        },
        {
            "name": "Mercury",
            "sign_index": 1,
            "longitude": 55.0,
        },
        {
            "name": "Jupiter",
            "sign_index": 3,
            "longitude": 105.0,
        },
        {
            "name": "Venus",
            "sign_index": 11,
            "longitude": 340.0,
        },
        {
            "name": "Saturn",
            "sign_index": 6,
            "longitude": 200.0,
        },
    ]

    # Aries Ascendant
    ascendant_sign = 0

    # --------------------------------------------------------
    # Calculate
    # --------------------------------------------------------

    analysis = build_ashtakavarga_analysis(
        sample_planets,
        ascendant_sign=ascendant_sign,
    )

    # --------------------------------------------------------
    # BAV
    # --------------------------------------------------------

    print("\nBHINNASHTAKAVARGA")
    print("-" * 70)

    for planet in ASHTAKAVARGA_PLANETS:

        bav = analysis[
            "bhinna_ashtakavarga"
        ][planet]

        total = calculate_bav_total(
            bav
        )

        print(
            f"{planet:8} | "
            f"Total Bindus: {total:2}"
        )

    # --------------------------------------------------------
    # SAV
    # --------------------------------------------------------

    print("\nSARVASHTAKAVARGA")
    print("-" * 70)

    for item in analysis[
        "sign_analysis"
    ]:

        print(
            f"{item['sign']:12} | "
            f"Bindus: {item['bindus']:2} | "
            f"{item['classification']}"
        )

    # --------------------------------------------------------
    # Houses
    # --------------------------------------------------------

    print("\nHOUSE-WISE SAV")
    print("-" * 70)

    for item in analysis[
        "house_analysis"
    ]:

        print(
            f"House {item['house']:2} | "
            f"{item['sign']:12} | "
            f"Bindus: {item['bindus']:2} | "
            f"{item['classification']}"
        )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    summary = build_ashtakavarga_summary(
        analysis
    )

    print("\nSUMMARY")
    print("-" * 70)

    print(
        "Total SAV bindus:",
        summary["total_bindus"]
    )

    print(
        "Strongest sign:",
        summary["strongest_sign"],
        "(",
        summary["strongest_sign_bindus"],
        ")"
    )

    print(
        "Weakest sign:",
        summary["weakest_sign"],
        "(",
        summary["weakest_sign_bindus"],
        ")"
    )

    print(
        "Strong signs:",
        [
            item["sign"]
            for item in analysis[
                "strong_signs"
            ]
        ]
    )

    print(
        "Weak signs:",
        [
            item["sign"]
            for item in analysis[
                "weak_signs"
            ]
        ]
    )

    # --------------------------------------------------------
    # Transit test
    # --------------------------------------------------------

    print("\nTRANSIT TEST")
    print("-" * 70)

    transit = get_transit_score(
        analysis["sarvashtakavarga"],
        0,
    )

    print(
        "Transit sign:",
        transit["sign"]
    )

    print(
        "Transit bindus:",
        transit["bindus"]
    )

    print(
        "Transit classification:",
        transit["classification"]
    )

    print("\n" + "=" * 70)
    print("ASHTAKAVARGA MODULE TEST COMPLETED")
    print("=" * 70)