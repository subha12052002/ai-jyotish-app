# =========================================================
# AI JYOTISH
# dasha.py
#
# Vimshottari Dasha
# Lahiri Sidereal Zodiac
# =========================================================

from datetime import datetime, timedelta, timezone

import swisseph as swe


# =========================================================
# SIDEREAL SETTINGS
# =========================================================

swe.set_sid_mode(
    swe.SIDM_LAHIRI
)


# =========================================================
# VIMSHOTTARI DASHA
# =========================================================

DASHA_YEARS = {

    "Ketu": 7,

    "Venus": 20,

    "Sun": 6,

    "Moon": 10,

    "Mars": 7,

    "Rahu": 18,

    "Jupiter": 16,

    "Saturn": 19,

    "Mercury": 17

}


# =========================================================
# DASHA ORDER
# =========================================================

DASHA_ORDER = [

    "Ketu",

    "Venus",

    "Sun",

    "Moon",

    "Mars",

    "Rahu",

    "Jupiter",

    "Saturn",

    "Mercury"

]


# =========================================================
# NAKSHATRAS
# =========================================================

NAKSHATRAS = [

    {
        "name": "Ashwini",
        "lord": "Ketu"
    },

    {
        "name": "Bharani",
        "lord": "Venus"
    },

    {
        "name": "Krittika",
        "lord": "Sun"
    },

    {
        "name": "Rohini",
        "lord": "Moon"
    },

    {
        "name": "Mrigashira",
        "lord": "Mars"
    },

    {
        "name": "Ardra",
        "lord": "Rahu"
    },

    {
        "name": "Punarvasu",
        "lord": "Jupiter"
    },

    {
        "name": "Pushya",
        "lord": "Saturn"
    },

    {
        "name": "Ashlesha",
        "lord": "Mercury"
    },

    {
        "name": "Magha",
        "lord": "Ketu"
    },

    {
        "name": "Purva Phalguni",
        "lord": "Venus"
    },

    {
        "name": "Uttara Phalguni",
        "lord": "Sun"
    },

    {
        "name": "Hasta",
        "lord": "Moon"
    },

    {
        "name": "Chitra",
        "lord": "Mars"
    },

    {
        "name": "Swati",
        "lord": "Rahu"
    },

    {
        "name": "Vishakha",
        "lord": "Jupiter"
    },

    {
        "name": "Anuradha",
        "lord": "Saturn"
    },

    {
        "name": "Jyeshtha",
        "lord": "Mercury"
    },

    {
        "name": "Mula",
        "lord": "Ketu"
    },

    {
        "name": "Purva Ashadha",
        "lord": "Venus"
    },

    {
        "name": "Uttara Ashadha",
        "lord": "Sun"
    },

    {
        "name": "Shravana",
        "lord": "Moon"
    },

    {
        "name": "Dhanishta",
        "lord": "Mars"
    },

    {
        "name": "Shatabhisha",
        "lord": "Rahu"
    },

    {
        "name": "Purva Bhadrapada",
        "lord": "Jupiter"
    },

    {
        "name": "Uttara Bhadrapada",
        "lord": "Saturn"
    },

    {
        "name": "Revati",
        "lord": "Mercury"
    }

]


# =========================================================
# NAKSHATRA SIZE
# =========================================================

NAKSHATRA_SIZE = 360.0 / 27.0


# =========================================================
# VIMSHOTTARI TOTAL
# =========================================================

TOTAL_DASHA_YEARS = 120


# =========================================================
# YEAR LENGTH
# =========================================================

# Tropical/sidereal dasha calculations traditionally use
# a 365.25-day approximation for converting dasha years
# into calendar dates.

DAYS_PER_YEAR = 365.25


# =========================================================
# SAFE SWISS EPHEMERIS RESULT
# =========================================================

def _calc_ut_values(
    jd,
    planet_id,
    flags
):
    """
    Handle different pyswisseph return formats.

    Some installations return:

        (values, return_flags)

    Others may return:

        (values, return_flags, warning)

    We only need values.
    """

    result = swe.calc_ut(
        jd,
        planet_id,
        flags
    )

    if (
        isinstance(result, tuple)
        and len(result) >= 1
        and isinstance(
            result[0],
            (tuple, list)
        )
    ):

        return result[0]

    if (
        isinstance(result, (tuple, list))
        and len(result) >= 4
        and all(
            isinstance(
                value,
                (int, float)
            )
            for value in result
        )
    ):

        return result

    raise RuntimeError(
        "Unexpected Swiss Ephemeris "
        f"calc_ut() result format: {result!r}"
    )


# =========================================================
# JULIAN DAY → DATETIME UTC
# =========================================================

def _datetime_from_julian_day(
    jd
):
    """
    Convert Julian Day into a UTC datetime.
    """

    year, month, day, hour = swe.revjul(
        jd,
        swe.GREG_CAL
    )

    hour_int = int(hour)

    minutes_float = (
        hour - hour_int
    ) * 60.0

    minute_int = int(
        minutes_float
    )

    seconds_float = (
        minutes_float - minute_int
    ) * 60.0

    second_int = int(
        seconds_float
    )

    microsecond = int(
        (
            seconds_float
            - second_int
        ) * 1_000_000
    )

    # Handle rounding overflow
    if microsecond >= 1_000_000:

        microsecond -= 1_000_000

        second_int += 1

    if second_int >= 60:

        second_int = 0

        minute_int += 1

    if minute_int >= 60:

        minute_int = 0

        hour_int += 1

    if hour_int >= 24:

        base = datetime(
            int(year),
            int(month),
            int(day),
            tzinfo=timezone.utc
        )

        base += timedelta(
            days=1
        )

        return base

    return datetime(
        int(year),
        int(month),
        int(day),
        hour_int,
        minute_int,
        second_int,
        microsecond,
        tzinfo=timezone.utc
    )


# =========================================================
# GET MOON LONGITUDE
# =========================================================

def get_moon_longitude(
    jd
):
    """
    Get the sidereal Moon longitude.

    Lahiri ayanamsha is used.
    """

    swe.set_sid_mode(
        swe.SIDM_LAHIRI
    )

    flags = (
        swe.FLG_MOSEPH
        | swe.FLG_SIDEREAL
        | swe.FLG_SPEED
    )

    values = _calc_ut_values(
        jd,
        swe.MOON,
        flags
    )

    longitude = float(
        values[0]
    )

    return longitude % 360.0


# =========================================================
# GET NAKSHATRA
# =========================================================

def get_nakshatra(
    moon_longitude
):
    """
    Determine Moon's Nakshatra from sidereal longitude.
    """

    longitude = (
        float(moon_longitude)
        % 360.0
    )

    nakshatra_index = int(
        longitude
        / NAKSHATRA_SIZE
    )

    # Safety
    if nakshatra_index < 0:

        nakshatra_index = 0

    if nakshatra_index > 26:

        nakshatra_index = 26

    nakshatra_start = (
        nakshatra_index
        * NAKSHATRA_SIZE
    )

    position_in_nakshatra = (
        longitude
        - nakshatra_start
    )

    fraction_completed = (
        position_in_nakshatra
        / NAKSHATRA_SIZE
    )

    fraction_remaining = (
        1.0
        - fraction_completed
    )

    nakshatra = NAKSHATRAS[
        nakshatra_index
    ]

    return {

        "index":
            nakshatra_index,

        "name":
            nakshatra["name"],

        "lord":
            nakshatra["lord"],

        "longitude":
            round(
                longitude,
                6
            ),

        "fraction_completed":
            round(
                fraction_completed,
                8
            ),

        "fraction_remaining":
            round(
                fraction_remaining,
                8
            )

    }


# =========================================================
# DASHA START INDEX
# =========================================================

def get_dasha_start_index(
    lord
):
    """
    Find the position of a Mahadasha lord
    in the Vimshottari sequence.
    """

    return DASHA_ORDER.index(
        lord
    )


# =========================================================
# NEXT DASHA LORD
# =========================================================

def next_dasha_lord(
    lord
):
    """
    Return the next Mahadasha lord.
    """

    index = get_dasha_start_index(
        lord
    )

    next_index = (
        index + 1
    ) % len(DASHA_ORDER)

    return DASHA_ORDER[
        next_index
    ]


# =========================================================
# ADD YEARS
# =========================================================

def add_dasha_years(
    date,
    years
):
    """
    Convert Vimshottari years into calendar date.
    """

    return date + timedelta(
        days=(
            float(years)
            * DAYS_PER_YEAR
        )
    )


# =========================================================
# FORMAT DATE
# =========================================================

def format_date(
    date
):
    """
    Format date for JSON.
    """

    return date.strftime(
        "%Y-%m-%d"
    )


# =========================================================
# GENERATE MAHADASHA TIMELINE
# =========================================================

def generate_mahadasha_timeline(
    birth_datetime,
    starting_lord,
    balance_years
):
    """
    Generate the complete Vimshottari Mahadasha
    sequence beginning at birth.

    The first Mahadasha contains only its remaining
    balance at birth.
    """

    timeline = []

    current_start = (
        birth_datetime
    )

    lord = starting_lord

    for index in range(
        len(DASHA_ORDER)
    ):

        if index == 0:

            duration_years = (
                float(balance_years)
            )

        else:

            duration_years = float(
                DASHA_YEARS[lord]
            )

        current_end = add_dasha_years(
            current_start,
            duration_years
        )

        timeline.append({

            "lord":
                lord,

            "duration_years":
                round(
                    duration_years,
                    6
                ),

            "start":
                format_date(
                    current_start
                ),

            "end":
                format_date(
                    current_end
                ),

            "start_datetime":
                current_start.isoformat(),

            "end_datetime":
                current_end.isoformat()

        })

        current_start = (
            current_end
        )

        lord = next_dasha_lord(
            lord
        )

    return timeline


# =========================================================
# FIND CURRENT MAHADASHA
# =========================================================

def find_current_mahadasha(
    timeline,
    current_datetime
):
    """
    Find the Mahadasha active on the requested date.
    """

    for period in timeline:

        start = datetime.fromisoformat(
            period["start_datetime"]
        )

        end = datetime.fromisoformat(
            period["end_datetime"]
        )

        if (
            start
            <= current_datetime
            < end
        ):

            return period

    return None


# =========================================================
# GENERATE ANTARDASHA
# =========================================================

def generate_antardasha(
    mahadasha
):
    """
    Generate all nine Antardashas inside
    a Mahadasha.

    Duration:

        MD years × AD lord years / 120
    """

    md_lord = mahadasha[
        "lord"
    ]

    md_start = datetime.fromisoformat(
        mahadasha[
            "start_datetime"
        ]
    )

    md_end = datetime.fromisoformat(
        mahadasha[
            "end_datetime"
        ]
    )

    md_years = float(
        mahadasha[
            "duration_years"
        ]
    )

    start_index = get_dasha_start_index(
        md_lord
    )

    periods = []

    current_start = (
        md_start
    )

    for offset in range(
        len(DASHA_ORDER)
    ):

        ad_index = (
            start_index + offset
        ) % len(DASHA_ORDER)

        ad_lord = DASHA_ORDER[
            ad_index
        ]

        # Standard Vimshottari
        # Antardasha duration.
        duration_years = (
            md_years
            * DASHA_YEARS[ad_lord]
            / TOTAL_DASHA_YEARS
        )

        current_end = add_dasha_years(
            current_start,
            duration_years
        )

        # Make sure the final period ends
        # exactly with Mahadasha.
        if offset == len(DASHA_ORDER) - 1:

            current_end = md_end

        periods.append({

            "lord":
                ad_lord,

            "duration_years":
                round(
                    duration_years,
                    8
                ),

            "start":
                format_date(
                    current_start
                ),

            "end":
                format_date(
                    current_end
                ),

            "start_datetime":
                current_start.isoformat(),

            "end_datetime":
                current_end.isoformat()

        })

        current_start = (
            current_end
        )

    return periods


# =========================================================
# FIND CURRENT ANTARDASHA
# =========================================================

def find_current_antardasha(
    periods,
    current_datetime
):
    """
    Find currently active Antardasha.
    """

    for period in periods:

        start = datetime.fromisoformat(
            period["start_datetime"]
        )

        end = datetime.fromisoformat(
            period["end_datetime"]
        )

        if (
            start
            <= current_datetime
            < end
        ):

            return period

    return None


# =========================================================
# CURRENT DASHA
# =========================================================

def get_current_dasha(
    birth_julian_day,
    calculation_julian_day=None
):
    """
    Calculate current Vimshottari Dasha.

    Parameters
    ----------
    birth_julian_day:
        Julian Day of birth.

    calculation_julian_day:
        Julian Day for the date on which the current
        dasha should be calculated.

        If omitted, today's UTC date/time is used.

    Returns
    -------
    dict
        Complete Dasha information.

    The existing app calls:

        get_current_dasha(chart["julian_day"])

    so this function remains compatible with that call.
    """

    # -----------------------------------------------------
    # Birth date/time
    # -----------------------------------------------------

    birth_datetime = (
        _datetime_from_julian_day(
            birth_julian_day
        )
    )

    # -----------------------------------------------------
    # Calculation date
    # -----------------------------------------------------

    if calculation_julian_day is None:

        current_datetime = datetime.now(
            timezone.utc
        )

    else:

        current_datetime = (
            _datetime_from_julian_day(
                calculation_julian_day
            )
        )

    # -----------------------------------------------------
    # Moon longitude
    # -----------------------------------------------------

    moon_longitude = get_moon_longitude(
        birth_julian_day
    )

    # -----------------------------------------------------
    # Nakshatra
    # -----------------------------------------------------

    nakshatra = get_nakshatra(
        moon_longitude
    )

    starting_lord = nakshatra[
        "lord"
    ]

    # -----------------------------------------------------
    # Remaining Mahadasha
    # -----------------------------------------------------

    starting_dasha_years = float(
        DASHA_YEARS[starting_lord]
    )

    balance_years = (
        starting_dasha_years
        * nakshatra[
            "fraction_remaining"
        ]
    )

    # -----------------------------------------------------
    # Generate timeline
    # -----------------------------------------------------

    timeline = generate_mahadasha_timeline(
        birth_datetime,
        starting_lord,
        balance_years
    )

    # -----------------------------------------------------
    # Current Mahadasha
    # -----------------------------------------------------

    current_mahadasha = (
        find_current_mahadasha(
            timeline,
            current_datetime
        )
    )

    # -----------------------------------------------------
    # Current Antardasha
    # -----------------------------------------------------

    current_antardasha = None

    all_antardashas = []

    if current_mahadasha:

        all_antardashas = (
            generate_antardasha(
                current_mahadasha
            )
        )

        current_antardasha = (
            find_current_antardasha(
                all_antardashas,
                current_datetime
            )
        )

    # -----------------------------------------------------
    # Current values
    # -----------------------------------------------------

    current_mahadasha_lord = None

    current_antardasha_lord = None

    if current_mahadasha:

        current_mahadasha_lord = (
            current_mahadasha[
                "lord"
            ]
        )

    if current_antardasha:

        current_antardasha_lord = (
            current_antardasha[
                "lord"
            ]
        )

    # -----------------------------------------------------
    # Return
    # -----------------------------------------------------

    return {

        "system":
            "Vimshottari",

        "total_years":
            TOTAL_DASHA_YEARS,

        "birth_datetime":
            birth_datetime.isoformat(),

        "calculation_datetime":
            current_datetime.isoformat(),

        "moon_longitude":
            round(
                moon_longitude,
                6
            ),

        "nakshatra":
            nakshatra,

        "starting_lord":
            starting_lord,

        "starting_dasha_years":
            starting_dasha_years,

        "balance_years":
            round(
                balance_years,
                6
            ),

        "current_mahadasha":
            current_mahadasha,

        "current_mahadasha_lord":
            current_mahadasha_lord,

        "current_antardasha":
            current_antardasha,

        "current_antardasha_lord":
            current_antardasha_lord,

        "mahadasha_timeline":
            timeline,

        "antardashas":
            all_antardashas

    }


# =========================================================
# SIMPLE DASHA SUMMARY
# =========================================================

def get_dasha_summary(
    birth_julian_day
):
    """
    Small helper for displaying Dasha information
    in the frontend.
    """

    dasha = get_current_dasha(
        birth_julian_day
    )

    return {

        "starting_lord":
            dasha[
                "starting_lord"
            ],

        "nakshatra":
            dasha[
                "nakshatra"
            ]["name"],

        "moon_longitude":
            dasha[
                "moon_longitude"
            ],

        "current_mahadasha":
            dasha[
                "current_mahadasha_lord"
            ],

        "current_antardasha":
            dasha[
                "current_antardasha_lord"
            ]

    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(
        "AI Jyotish Dasha module loaded."
    )

    print(
        "Vimshottari sequence:"
    )

    print(
        " → ".join(
            DASHA_ORDER
        )
    )