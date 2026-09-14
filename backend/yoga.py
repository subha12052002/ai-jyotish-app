def detect_yogas(chart):

    planets = {

        planet["name"]: planet

        for planet in chart["planets"]

    }


    yogas = []


    # =====================================================
    # GAJA KESARI YOGA
    # =====================================================

    moon_house = planets[
        "Moon"
    ]["house"]


    jupiter_house = planets[
        "Jupiter"
    ]["house"]


    distance = (

        (
            jupiter_house
            - moon_house
        ) % 12

    ) + 1


    if distance in (
        1,
        4,
        7,
        10
    ):

        yogas.append({

            "name":
                "Gaja Kesari Yoga",

            "type":
                "Prosperity",

            "description":
                (
                    "Jupiter is placed in a kendra "
                    "from the Moon, traditionally "
                    "associated with wisdom, reputation "
                    "and supportive growth."
                )

        })


    # =====================================================
    # BUDHA ADITYA YOGA
    # =====================================================

    if (

        planets["Sun"]["sign_index"]

        ==

        planets["Mercury"]["sign_index"]

    ):

        yogas.append({

            "name":
                "Budha Aditya Yoga",

            "type":
                "Intelligence",

            "description":
                (
                    "Sun and Mercury occupy the same "
                    "sign, traditionally associated "
                    "with intellect, communication "
                    "and analytical ability."
                )

        })


    # =====================================================
    # CHANDRA MANGALA YOGA
    # =====================================================

    if (

        planets["Moon"]["sign_index"]

        ==

        planets["Mars"]["sign_index"]

    ):

        yogas.append({

            "name":
                "Chandra Mangala Yoga",

            "type":
                "Finance",

            "description":
                (
                    "Moon and Mars share a sign, "
                    "traditionally associated with "
                    "initiative, enterprise and "
                    "material drive."
                )

        })


    # =====================================================
    # 9TH HOUSE EMPHASIS
    # =====================================================

    ninth_house_planets = [

        planet["name"]

        for planet in chart["planets"]

        if planet["house"] == 9

    ]


    if ninth_house_planets:

        yogas.append({

            "name":
                "Dharma Focus",

            "type":
                "Purpose",

            "description":
                (
                    "Planetary emphasis appears in "
                    f"the 9th house "
                    f"({', '.join(ninth_house_planets)}), "
                    "traditionally connected with "
                    "learning, principles and "
                    "long-distance horizons."
                )

        })


    # =====================================================
    # NO SIMPLIFIED YOGA
    # =====================================================

    if not yogas:

        yogas.append({

            "name":
                "Chart Highlights",

            "type":
                "General",

            "description":
                (
                    "No simplified named yoga was "
                    "detected by this starter rule set. "
                    "A complete Jyotish engine can add "
                    "many more classical conditions."
                )

        })


    return yogas