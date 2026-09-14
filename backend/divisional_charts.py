from ephemeris import SIGNS


# =========================================================
# NAVAMSA SIGN
# =========================================================

def navamsa_sign(longitude):

    # -----------------------------------------------------
    # RASHI
    # -----------------------------------------------------

    sign_index = int(

        (longitude % 360) // 30

    )


    # -----------------------------------------------------
    # DEGREE INSIDE SIGN
    # -----------------------------------------------------

    degree = longitude % 30


    # -----------------------------------------------------
    # NAVAMSA PART
    # -----------------------------------------------------

    part = int(

        degree / (30 / 9)

    )


    # -----------------------------------------------------
    # SIGN TYPE
    #
    # 0 = movable
    # 1 = fixed
    # 2 = dual
    # -----------------------------------------------------

    element_type = sign_index % 3


    if element_type == 0:

        # Movable

        start = sign_index


    elif element_type == 1:

        # Fixed

        start = (
            sign_index + 8
        ) % 12


    else:

        # Dual

        start = (
            sign_index + 4
        ) % 12


    # -----------------------------------------------------
    # NAVAMSA SIGN
    # -----------------------------------------------------

    nav_index = (

        start + part

    ) % 12


    return {

        "sign":
            SIGNS[nav_index],

        "sign_index":
            nav_index,

        "navamsa":
            part + 1

    }


# =========================================================
# BUILD NAVAMSA
# =========================================================

def build_navamsa(planets):

    return [

        {

            "name": planet["name"],

            **navamsa_sign(
                planet["longitude"]
            )

        }

        for planet in planets

    ]