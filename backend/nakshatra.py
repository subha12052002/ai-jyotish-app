# ============================================================
# AI JYOTISH
# nakshatra.py
#
# Vedic Nakshatra Analysis Engine
#
# 27 Nakshatras
# 4 Padas each
# Vimshottari Lords
# Nakshatra characteristics
# Longitude -> Nakshatra calculation
# ============================================================


# ============================================================
# CONSTANTS
# ============================================================

TOTAL_NAKSHATRAS = 27

NAKSHATRA_SIZE = 360.0 / 27.0

PADA_SIZE = NAKSHATRA_SIZE / 4.0


# ============================================================
# NAKSHATRA DATA
#
# Index:
#   0 = Ashwini
#   1 = Bharani
#   ...
#   26 = Revati
# ============================================================

NAKSHATRAS = [

    {
        "index": 0,
        "name": "Ashwini",
        "lord": "Ketu",
        "deity": "Ashwini Kumaras",
        "symbol": "Horse Head",
        "gana": "Deva",
        "yoni": "Horse",
        "nadi": "Adi",
        "varna": "Vaishya",
        "element": "Earth",
        "nature": "Light",
        "quality": "Active",
    },

    {
        "index": 1,
        "name": "Bharani",
        "lord": "Venus",
        "deity": "Yama",
        "symbol": "Yoni",
        "gana": "Manushya",
        "yoni": "Elephant",
        "nadi": "Madhya",
        "varna": "Mleccha",
        "element": "Earth",
        "nature": "Fierce",
        "quality": "Transformative",
    },

    {
        "index": 2,
        "name": "Krittika",
        "lord": "Sun",
        "deity": "Agni",
        "symbol": "Razor",
        "gana": "Rakshasa",
        "yoni": "Sheep",
        "nadi": "Antya",
        "varna": "Brahmin",
        "element": "Fire",
        "nature": "Sharp",
        "quality": "Purifying",
    },

    {
        "index": 3,
        "name": "Rohini",
        "lord": "Moon",
        "deity": "Brahma",
        "symbol": "Chariot",
        "gana": "Manushya",
        "yoni": "Serpent",
        "nadi": "Antya",
        "varna": "Shudra",
        "element": "Earth",
        "nature": "Fixed",
        "quality": "Creative",
    },

    {
        "index": 4,
        "name": "Mrigashira",
        "lord": "Mars",
        "deity": "Soma",
        "symbol": "Deer's Head",
        "gana": "Deva",
        "yoni": "Serpent",
        "nadi": "Madhya",
        "varna": "Shudra",
        "element": "Earth",
        "nature": "Soft",
        "quality": "Searching",
    },

    {
        "index": 5,
        "name": "Ardra",
        "lord": "Rahu",
        "deity": "Rudra",
        "symbol": "Teardrop",
        "gana": "Manushya",
        "yoni": "Dog",
        "nadi": "Adi",
        "varna": "Butcher",
        "element": "Water",
        "nature": "Sharp",
        "quality": "Transformative",
    },

    {
        "index": 6,
        "name": "Punarvasu",
        "lord": "Jupiter",
        "deity": "Aditi",
        "symbol": "Quiver of Arrows",
        "gana": "Deva",
        "yoni": "Cat",
        "nadi": "Adi",
        "varna": "Vaishya",
        "element": "Water",
        "nature": "Movable",
        "quality": "Renewing",
    },

    {
        "index": 7,
        "name": "Pushya",
        "lord": "Saturn",
        "deity": "Brihaspati",
        "symbol": "Flower",
        "gana": "Deva",
        "yoni": "Sheep",
        "nadi": "Madhya",
        "varna": "Kshatriya",
        "element": "Water",
        "nature": "Light",
        "quality": "Nourishing",
    },

    {
        "index": 8,
        "name": "Ashlesha",
        "lord": "Mercury",
        "deity": "Nagas",
        "symbol": "Coiled Serpent",
        "gana": "Rakshasa",
        "yoni": "Cat",
        "nadi": "Antya",
        "varna": "Mleccha",
        "element": "Water",
        "nature": "Sharp",
        "quality": "Mystical",
    },

    {
        "index": 9,
        "name": "Magha",
        "lord": "Ketu",
        "deity": "Pitris",
        "symbol": "Royal Throne",
        "gana": "Rakshasa",
        "yoni": "Rat",
        "nadi": "Antya",
        "varna": "Shudra",
        "element": "Water",
        "nature": "Fierce",
        "quality": "Ancestral",
    },

    {
        "index": 10,
        "name": "Purva Phalguni",
        "lord": "Venus",
        "deity": "Bhaga",
        "symbol": "Hammock",
        "gana": "Manushya",
        "yoni": "Rat",
        "nadi": "Madhya",
        "varna": "Brahmin",
        "element": "Water",
        "nature": "Fierce",
        "quality": "Enjoyment",
    },

    {
        "index": 11,
        "name": "Uttara Phalguni",
        "lord": "Sun",
        "deity": "Aryaman",
        "symbol": "Bed",
        "gana": "Manushya",
        "yoni": "Cow",
        "nadi": "Adi",
        "varna": "Kshatriya",
        "element": "Fire",
        "nature": "Fixed",
        "quality": "Stable",
    },

    {
        "index": 12,
        "name": "Hasta",
        "lord": "Moon",
        "deity": "Savitar",
        "symbol": "Hand",
        "gana": "Deva",
        "yoni": "Buffalo",
        "nadi": "Adi",
        "varna": "Vaishya",
        "element": "Fire",
        "nature": "Light",
        "quality": "Skillful",
    },

    {
        "index": 13,
        "name": "Chitra",
        "lord": "Mars",
        "deity": "Tvashtar",
        "symbol": "Pearl",
        "gana": "Rakshasa",
        "yoni": "Tiger",
        "nadi": "Madhya",
        "varna": "Vaishya",
        "element": "Fire",
        "nature": "Soft",
        "quality": "Creative",
    },

    {
        "index": 14,
        "name": "Swati",
        "lord": "Rahu",
        "deity": "Vayu",
        "symbol": "Young Plant",
        "gana": "Deva",
        "yoni": "Buffalo",
        "nadi": "Antya",
        "varna": "Butcher",
        "element": "Fire",
        "nature": "Movable",
        "quality": "Independent",
    },

    {
        "index": 15,
        "name": "Vishakha",
        "lord": "Jupiter",
        "deity": "Indra-Agni",
        "symbol": "Triumphal Arch",
        "gana": "Rakshasa",
        "yoni": "Tiger",
        "nadi": "Antya",
        "varna": "Kshatriya",
        "element": "Fire",
        "nature": "Fierce",
        "quality": "Goal-Oriented",
    },

    {
        "index": 16,
        "name": "Anuradha",
        "lord": "Saturn",
        "deity": "Mitra",
        "symbol": "Lotus",
        "gana": "Deva",
        "yoni": "Deer",
        "nadi": "Madhya",
        "varna": "Shudra",
        "element": "Fire",
        "nature": "Soft",
        "quality": "Devotional",
    },

    {
        "index": 17,
        "name": "Jyeshtha",
        "lord": "Mercury",
        "deity": "Indra",
        "symbol": "Earring",
        "gana": "Rakshasa",
        "yoni": "Deer",
        "nadi": "Adi",
        "varna": "Vaishya",
        "element": "Air",
        "nature": "Sharp",
        "quality": "Protective",
    },

    {
        "index": 18,
        "name": "Mula",
        "lord": "Ketu",
        "deity": "Nirriti",
        "symbol": "Roots",
        "gana": "Rakshasa",
        "yoni": "Dog",
        "nadi": "Adi",
        "varna": "Butcher",
        "element": "Air",
        "nature": "Sharp",
        "quality": "Investigative",
    },

    {
        "index": 19,
        "name": "Purva Ashadha",
        "lord": "Venus",
        "deity": "Apah",
        "symbol": "Fan",
        "gana": "Manushya",
        "yoni": "Monkey",
        "nadi": "Madhya",
        "varna": "Kshatriya",
        "element": "Air",
        "nature": "Fierce",
        "quality": "Invincible",
    },

    {
        "index": 20,
        "name": "Uttara Ashadha",
        "lord": "Sun",
        "deity": "Vishvadevas",
        "symbol": "Elephant Tusk",
        "gana": "Manushya",
        "yoni": "Mongoose",
        "nadi": "Antya",
        "varna": "Kshatriya",
        "element": "Air",
        "nature": "Fixed",
        "quality": "Victorious",
    },

    {
        "index": 21,
        "name": "Shravana",
        "lord": "Moon",
        "deity": "Vishnu",
        "symbol": "Ear",
        "gana": "Deva",
        "yoni": "Monkey",
        "nadi": "Antya",
        "varna": "Mleccha",
        "element": "Air",
        "nature": "Movable",
        "quality": "Learning",
    },

    {
        "index": 22,
        "name": "Dhanishtha",
        "lord": "Mars",
        "deity": "Vasus",
        "symbol": "Drum",
        "gana": "Rakshasa",
        "yoni": "Lion",
        "nadi": "Madhya",
        "varna": "Vaishya",
        "element": "Ether",
        "nature": "Movable",
        "quality": "Wealth",
    },

    {
        "index": 23,
        "name": "Shatabhisha",
        "lord": "Rahu",
        "deity": "Varuna",
        "symbol": "Circle",
        "gana": "Rakshasa",
        "yoni": "Horse",
        "nadi": "Adi",
        "varna": "Butcher",
        "element": "Ether",
        "nature": "Movable",
        "quality": "Healing",
    },

    {
        "index": 24,
        "name": "Purva Bhadrapada",
        "lord": "Jupiter",
        "deity": "Aja Ekapada",
        "symbol": "Sword",
        "gana": "Manushya",
        "yoni": "Lion",
        "nadi": "Adi",
        "varna": "Brahmin",
        "element": "Ether",
        "nature": "Fierce",
        "quality": "Transformative",
    },

    {
        "index": 25,
        "name": "Uttara Bhadrapada",
        "lord": "Saturn",
        "deity": "Ahir Budhnya",
        "symbol": "Back Legs of Funeral Cot",
        "gana": "Manushya",
        "yoni": "Cow",
        "nadi": "Madhya",
        "varna": "Kshatriya",
        "element": "Ether",
        "nature": "Fixed",
        "quality": "Deep",
    },

    {
        "index": 26,
        "name": "Revati",
        "lord": "Mercury",
        "deity": "Pushan",
        "symbol": "Fish",
        "gana": "Deva",
        "yoni": "Elephant",
        "nadi": "Antya",
        "varna": "Vaishya",
        "element": "Ether",
        "nature": "Soft",
        "quality": "Nourishing",
    },

]


# ============================================================
# LORD SEQUENCE
#
# Vimshottari sequence
# ============================================================

NAKSHATRA_LORDS = [

    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",

    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",

    "Ketu",
    "Venus",
    "Sun",
    "Moon",
    "Mars",
    "Rahu",
    "Jupiter",
    "Saturn",
    "Mercury",

]


# ============================================================
# VIMSHOTTARI YEARS
# ============================================================

VIMSHOTTARI_YEARS = {

    "Ketu": 7,

    "Venus": 20,

    "Sun": 6,

    "Moon": 10,

    "Mars": 7,

    "Rahu": 18,

    "Jupiter": 16,

    "Saturn": 19,

    "Mercury": 17,

}


# ============================================================
# GET NAKSHATRA
# ============================================================

def get_nakshatra(
    longitude
):
    """
    Convert sidereal longitude into:

        Nakshatra
        Nakshatra index
        Pada
        Nakshatra lord
        Position inside Nakshatra

    Longitude:
        0 - 360 degrees
    """

    try:

        longitude = float(
            longitude
        )

    except (
        TypeError,
        ValueError
    ):

        raise ValueError(
            "Longitude must be a number."
        )


    # Normalize longitude

    longitude = longitude % 360.0


    # Calculate Nakshatra index

    index = int(
        longitude
        / NAKSHATRA_SIZE
    )


    # Safety

    if index >= 27:

        index = 26


    nakshatra = NAKSHATRAS[
        index
    ].copy()


    # Position inside Nakshatra

    start = (
        index
        * NAKSHATRA_SIZE
    )

    end = (
        start
        + NAKSHATRA_SIZE
    )

    position = (
        longitude
        - start
    )


    # Pada

    pada = int(
        position
        / PADA_SIZE
    ) + 1


    if pada > 4:

        pada = 4


    pada_start = (
        (pada - 1)
        * PADA_SIZE
    )

    pada_position = (
        position
        - pada_start
    )


    # Add calculated values

    nakshatra[
        "start_degree"
    ] = start

    nakshatra[
        "end_degree"
    ] = end

    nakshatra[
        "position"
    ] = position

    nakshatra[
        "pada"
    ] = pada

    nakshatra[
        "pada_position"
    ] = pada_position

    nakshatra[
        "lord_years"
    ] = VIMSHOTTARI_YEARS.get(
        nakshatra[
            "lord"
        ],
        0
    )


    return nakshatra


# ============================================================
# GET NAKSHATRA BY NAME
# ============================================================

def get_nakshatra_by_name(
    name
):
    """
    Find Nakshatra by name.
    """

    if not name:

        return None


    name = str(
        name
    ).strip().lower()


    for nakshatra in NAKSHATRAS:

        if nakshatra[
            "name"
        ].lower() == name:

            return nakshatra.copy()


    return None


# ============================================================
# GET NAKSHATRA BY INDEX
# ============================================================

def get_nakshatra_by_index(
    index
):
    """
    Find Nakshatra by index.
    """

    try:

        index = int(
            index
        )

    except (
        TypeError,
        ValueError
    ):

        return None


    if not 0 <= index < 27:

        return None


    return NAKSHATRAS[
        index
    ].copy()


# ============================================================
# GET NAKSHATRA LORD
# ============================================================

def get_nakshatra_lord(
    longitude
):
    """
    Return Nakshatra lord directly.
    """

    data = get_nakshatra(
        longitude
    )

    return data[
        "lord"
    ]


# ============================================================
# GET PADA
# ============================================================

def get_pada(
    longitude
):
    """
    Return Nakshatra Pada.
    """

    data = get_nakshatra(
        longitude
    )

    return data[
        "pada"
    ]


# ============================================================
# ANALYZE PLANET
# ============================================================

def analyze_planet_nakshatra(
    planet
):
    """
    Add detailed Nakshatra information to
    a planetary dictionary.

    Works with:

        longitude

    or

        sign_index + degree
    """

    if not isinstance(
        planet,
        dict
    ):

        raise TypeError(
            "Planet must be a dictionary."
        )


    result = planet.copy()


    longitude = result.get(
        "longitude"
    )


    # --------------------------------------------------------
    # If absolute longitude is unavailable,
    # calculate it from sign + degree.
    # --------------------------------------------------------

    if longitude is None:

        sign_index = result.get(
            "sign_index"
        )

        degree = result.get(
            "degree"
        )

        if (
            sign_index is not None
            and degree is not None
        ):

            longitude = (
                int(sign_index) * 30.0
                + float(degree)
            )


    if longitude is None:

        return result


    # --------------------------------------------------------
    # Calculate Nakshatra
    # --------------------------------------------------------

    data = get_nakshatra(
        longitude
    )


    # --------------------------------------------------------
    # Add fields
    # --------------------------------------------------------

    result[
        "nakshatra"
    ] = data[
        "name"
    ]

    result[
        "nakshatra_index"
    ] = data[
        "index"
    ]

    result[
        "nakshatra_lord"
    ] = data[
        "lord"
    ]

    result[
        "pada"
    ] = data[
        "pada"
    ]

    result[
        "nakshatra_deity"
    ] = data[
        "deity"
    ]

    result[
        "nakshatra_symbol"
    ] = data[
        "symbol"
    ]

    result[
        "nakshatra_gana"
    ] = data[
        "gana"
    ]

    result[
        "nakshatra_yoni"
    ] = data[
        "yoni"
    ]

    result[
        "nakshatra_nadi"
    ] = data[
        "nadi"
    ]

    result[
        "nakshatra_varna"
    ] = data[
        "varna"
    ]

    result[
        "nakshatra_element"
    ] = data[
        "element"
    ]

    result[
        "nakshatra_nature"
    ] = data[
        "nature"
    ]

    result[
        "nakshatra_quality"
    ] = data[
        "quality"
    ]

    result[
        "nakshatra_start"
    ] = data[
        "start_degree"
    ]

    result[
        "nakshatra_end"
    ] = data[
        "end_degree"
    ]

    result[
        "nakshatra_position"
    ] = data[
        "position"
    ]

    result[
        "pada_position"
    ] = data[
        "pada_position"
    ]

    result[
        "nakshatra_lord_years"
    ] = data[
        "lord_years"
    ]


    return result


# ============================================================
# ANALYZE ALL PLANETS
# ============================================================

def analyze_planets_nakshatra(
    planets
):
    """
    Add Nakshatra information to all planets.
    """

    if not isinstance(
        planets,
        list
    ):

        raise TypeError(
            "Planets must be a list."
        )


    return [

        analyze_planet_nakshatra(
            planet
        )

        for planet in planets

    ]


# ============================================================
# GET MOON BIRTH NAKSHATRA
# ============================================================

def get_birth_nakshatra(
    planets
):
    """
    Find Moon's Nakshatra.

    This is the Janma Nakshatra.
    """

    if not isinstance(
        planets,
        list
    ):

        return None


    for planet in planets:

        if planet.get(
            "name"
        ) == "Moon":

            longitude = planet.get(
                "longitude"
            )

            if longitude is None:

                sign_index = planet.get(
                    "sign_index"
                )

                degree = planet.get(
                    "degree"
                )

                if (
                    sign_index is not None
                    and degree is not None
                ):

                    longitude = (
                        int(sign_index) * 30
                        + float(degree)
                    )


            if longitude is not None:

                return get_nakshatra(
                    longitude
                )


    return None


# ============================================================
# GET NAKSHATRA SUMMARY
# ============================================================

def nakshatra_summary(
    longitude
):
    """
    Return a concise user-friendly summary.
    """

    data = get_nakshatra(
        longitude
    )


    return {

        "nakshatra":
            data["name"],

        "lord":
            data["lord"],

        "pada":
            data["pada"],

        "deity":
            data["deity"],

        "symbol":
            data["symbol"],

        "gana":
            data["gana"],

        "yoni":
            data["yoni"],

        "nadi":
            data["nadi"],

        "element":
            data["element"],

        "nature":
            data["nature"],

    }


# ============================================================
# GET ALL NAKSHATRAS
# ============================================================

def get_all_nakshatras():
    """
    Return all 27 Nakshatras.
    """

    return [

        nakshatra.copy()

        for nakshatra in NAKSHATRAS

    ]


# ============================================================
# VALIDATE LONGITUDE
# ============================================================

def validate_longitude(
    longitude
):
    """
    Check whether longitude is valid.
    """

    try:

        value = float(
            longitude
        )

    except (
        TypeError,
        ValueError
    ):

        return False


    return 0.0 <= value < 360.0


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()

    print("=" * 75)

    print(
        "AI JYOTISH - NAKSHATRA ENGINE TEST"
    )

    print("=" * 75)


    # --------------------------------------------------------
    # Test longitudes
    # --------------------------------------------------------

    test_longitudes = [

        0.0,

        13.333333,

        26.666666,

        40.0,

        100.0,

        180.0,

        270.0,

        359.9,

    ]


    print()

    print(
        "LONGITUDE -> NAKSHATRA"
    )

    print("-" * 75)


    for longitude in test_longitudes:

        data = get_nakshatra(
            longitude
        )


        print()

        print(
            f"Longitude : {longitude:.6f}°"
        )

        print(
            f"Nakshatra : {data['name']}"
        )

        print(
            f"Lord      : {data['lord']}"
        )

        print(
            f"Pada      : {data['pada']}"
        )

        print(
            f"Start     : {data['start_degree']:.6f}°"
        )

        print(
            f"End       : {data['end_degree']:.6f}°"
        )

        print(
            f"Deity     : {data['deity']}"
        )

        print(
            f"Symbol    : {data['symbol']}"
        )


    # --------------------------------------------------------
    # Test sample planets
    # --------------------------------------------------------

    sample_planets = [

        {
            "name": "Sun",
            "longitude": 26.613390,
            "sign": "Mesha",
            "sign_index": 0,
            "degree": 26.613390,
        },

        {
            "name": "Moon",
            "longitude": 78.245000,
            "sign": "Mithuna",
            "sign_index": 2,
            "degree": 18.245000,
        },

        {
            "name": "Mars",
            "longitude": 290.500000,
            "sign": "Makara",
            "sign_index": 9,
            "degree": 20.500000,
        },

    ]


    print()

    print(
        "PLANETARY NAKSHATRA ANALYSIS"
    )

    print("-" * 75)


    analyzed = analyze_planets_nakshatra(
        sample_planets
    )


    for planet in analyzed:

        print()

        print(
            f"Planet        : "
            f"{planet.get('name')}"
        )

        print(
            f"Nakshatra     : "
            f"{planet.get('nakshatra')}"
        )

        print(
            f"Nakshatra Lord: "
            f"{planet.get('nakshatra_lord')}"
        )

        print(
            f"Pada          : "
            f"{planet.get('pada')}"
        )

        print(
            f"Deity         : "
            f"{planet.get('nakshatra_deity')}"
        )

        print(
            f"Symbol        : "
            f"{planet.get('nakshatra_symbol')}"
        )


    # --------------------------------------------------------
    # Test Moon
    # --------------------------------------------------------

    moon_nakshatra = get_birth_nakshatra(
        sample_planets
    )


    print()

    print(
        "MOON / JANMA NAKSHATRA"
    )

    print("-" * 75)


    if moon_nakshatra:

        print(
            f"Nakshatra : "
            f"{moon_nakshatra['name']}"
        )

        print(
            f"Lord      : "
            f"{moon_nakshatra['lord']}"
        )

        print(
            f"Pada      : "
            f"{moon_nakshatra['pada']}"
        )


    # --------------------------------------------------------
    # Count check
    # --------------------------------------------------------

    print()

    print(
        f"Total Nakshatras: "
        f"{len(NAKSHATRAS)}"
    )


    if len(NAKSHATRAS) == 27:

        print(
            "✓ 27 NAKSHATRAS VERIFIED"
        )

    else:

        print(
            "✗ NAKSHATRA COUNT ERROR"
        )


    print()

    print("=" * 75)

    print(
        "✓ NAKSHATRA.PY TEST COMPLETED"
    )

    print("=" * 75)

    print()