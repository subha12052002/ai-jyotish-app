def get_d9_sign(longitude):
    """
    Basic Navamsa sign calculation.

    This is a foundation for the D9 chart.
    """

    longitude = float(longitude) % 360

    sign_index = int(
        longitude // 30
    )

    degree = longitude % 30

    navamsa_number = int(
        degree / (30 / 9)
    )

    navamsa_sign = (
        sign_index * 9
        + navamsa_number
    ) % 12

    signs = [
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
        "Pisces"
    ]

    return signs[
        navamsa_sign
    ]


def create_navamsa(planets):

    result = {}

    for name, data in planets.items():

        longitude = data.get(
            "longitude"
        )

        if longitude is None:
            continue

        result[name] = {
            "sign": get_d9_sign(
                longitude
            )
        }

    return result