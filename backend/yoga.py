def detect_yogas(kundli):

    planets = kundli.get(
        "planets",
        {}
    )

    yogas = []

    # -----------------------------------------------
    # Basic Gaja Kesari foundation
    # -----------------------------------------------

    moon = planets.get("Moon")
    jupiter = planets.get("Jupiter")

    if moon and jupiter:

        moon_house = moon.get(
            "house"
        )

        jupiter_house = jupiter.get(
            "house"
        )

        if moon_house and jupiter_house:

            distance = (
                jupiter_house
                - moon_house
            ) % 12

            if distance in [0, 4, 8]:

                yogas.append({
                    "name":
                        "Gaja Kesari Yoga",

                    "description":
                        "A traditional Jyotish combination involving Jupiter and Moon."
                })

    return yogas