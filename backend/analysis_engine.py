"""
AI JYOTISH
Complete Astrology Analysis Engine

This module combines all existing astrology engines
into one complete analysis pipeline.

Gemini is NOT used in this file.

The flow is:

Birth Details
     ↓
Kundli Calculation
     ↓
Analysis Engine
     ↓
Planets
Nakshatra
Houses
Aspects
Dignity
Combustion
Shadbala
Ashtakavarga
Navamsa
Dasha
Yoga
     ↓
Complete Analysis
     ↓
Gemini 2.5 Flash
"""


from datetime import datetime


# =========================================================
# IMPORT ASTROLOGY MODULES
# =========================================================

from planets import (
    analyze_planets,
)

from nakshatra import (
    analyze_planets_nakshatra,
)

from houses import (
    build_house_analysis,
)
from bhavbala import (
    build_bhava_bala_analysis,
)

from aspects import (
    build_aspect_analysis,
)

from dignity import (
    build_dignity_analysis,
)

from combustion import (
    build_combustion_table,
)

from shadbala import (
    build_shadbala_analysis,
)

from ashtakavarga import (
    build_ashtakavarga_analysis,
)

from divisional_charts import (
    build_navamsa,
)

from dasha import (
    get_current_dasha,
)

from yoga import (
    detect_yogas,
)


# =========================================================
# ENGINE VERSION
# =========================================================

ANALYSIS_ENGINE_VERSION = "1.0.1"


# =========================================================
# SAFE COPY
# =========================================================

def copy_planets(planets):
    """
    Create a safe copy of planetary data.

    This prevents analysis functions from accidentally
    modifying the original Kundli data.
    """

    if not isinstance(planets, list):
        return []

    copied = []

    for planet in planets:

        if isinstance(planet, dict):
            copied.append(
                dict(planet)
            )

        else:
            copied.append(
                planet
            )

    return copied


# =========================================================
# SAFE MODULE EXECUTION
# =========================================================

def run_module(
    module_name,
    function,
    *args,
    **kwargs
):
    """
    Execute an analysis function safely.

    If one analysis module fails, the rest of the
    Kundli analysis can continue.
    """

    try:

        result = function(
            *args,
            **kwargs
        )

        return {
            "success": True,
            "data": result,
            "error": None,
        }

    except Exception as exc:

        print()
        print(
            f"[WARNING] {module_name} analysis failed"
        )

        print(
            f"Error: {type(exc).__name__}: {exc}"
        )

        return {
            "success": False,
            "data": None,
            "error": (
                f"{type(exc).__name__}: "
                f"{str(exc)}"
            ),
        }


# =========================================================
# VALIDATE CHART
# =========================================================

def validate_chart(chart):
    """
    Validate the basic Kundli structure.
    """

    errors = []

    if not isinstance(chart, dict):

        return {
            "valid": False,
            "errors": [
                "Chart must be a dictionary."
            ],
        }

    # -----------------------------------------------------
    # PLANETS
    # -----------------------------------------------------

    if "planets" not in chart:

        errors.append(
            "Planet data is missing."
        )

    elif not isinstance(
        chart["planets"],
        list
    ):

        errors.append(
            "Planet data must be a list."
        )

    # -----------------------------------------------------
    # ASCENDANT
    # -----------------------------------------------------

    if "ascendant" not in chart:

        errors.append(
            "Ascendant data is missing."
        )

    elif not isinstance(
        chart["ascendant"],
        dict
    ):

        errors.append(
            "Ascendant must be a dictionary."
        )

    # -----------------------------------------------------
    # JULIAN DAY
    # -----------------------------------------------------

    if "julian_day" not in chart:

        errors.append(
            "Julian day is missing."
        )

    return {
        "valid":
            len(errors) == 0,

        "errors":
            errors,
    }


# =========================================================
# BASIC ANALYSIS
# =========================================================

def build_basic_analysis(chart):
    """
    Build basic information about the Kundli.
    """

    ascendant = chart.get(
        "ascendant",
        {}
    )

    planets = chart.get(
        "planets",
        []
    )

    houses = chart.get(
        "houses",
        []
    )

    return {

        "birth": {

            "name":
                chart.get(
                    "name"
                ),

            "date":
                chart.get(
                    "birth_date"
                ),

            "time":
                chart.get(
                    "birth_time"
                ),

            "place":
                chart.get(
                    "place"
                ),

            "latitude":
                chart.get(
                    "latitude"
                ),

            "longitude":
                chart.get(
                    "longitude"
                ),

            "timezone":
                chart.get(
                    "timezone"
                ),

        },

        "ascendant":
            ascendant,

        "sun_sign":
            chart.get(
                "sun_sign"
            ),

        "moon_sign":
            chart.get(
                "moon_sign"
            ),

        "planet_count":
            len(planets),

        "house_count":
            len(houses),

        "calculation":
            chart.get(
                "calculation",
                {}
            ),

    }


# =========================================================
# PLANET ANALYSIS
# =========================================================

def build_planet_engine_analysis(chart):

    planets = copy_planets(
        chart.get(
            "planets",
            []
        )
    )

    return run_module(
        "Planets",
        analyze_planets,
        planets
    )


# =========================================================
# NAKSHATRA ANALYSIS
# =========================================================

def build_nakshatra_engine_analysis(chart):

    planets = copy_planets(
        chart.get(
            "planets",
            []
        )
    )

    return run_module(
        "Nakshatra",
        analyze_planets_nakshatra,
        planets
    )


# =========================================================
# HOUSE ANALYSIS
# =========================================================

def build_house_engine_analysis(chart):

    planets = copy_planets(
        chart.get(
            "planets",
            []
        )
    )

    houses = chart.get(
        "houses",
        []
    )

    ascendant = chart.get(
        "ascendant",
        {}
    )

    ascendant_sign_index = (
        ascendant.get(
            "sign_index"
        )
    )

    # -----------------------------------------------------
    # Try common house-analysis signatures
    # -----------------------------------------------------

    attempts = [

        (
            houses,
            planets,
            ascendant_sign_index
        ),

        (
            chart,
        ),

        (
            planets,
            ascendant_sign_index
        ),

        (
            planets,
            houses,
            ascendant_sign_index
        ),

    ]

    for args in attempts:

        try:

            result = build_house_analysis(
                *args
            )

            return {
                "success": True,
                "data": result,
                "error": None,
            }

        except TypeError:

            continue

        except Exception as exc:

            return {
                "success": False,
                "data": None,
                "error":
                    f"{type(exc).__name__}: "
                    f"{str(exc)}",
            }


    return {
        "success": False,
        "data": None,
        "error":
            "Could not match build_house_analysis signature.",
    }
# =========================================================
# BHAVA BALA ANALYSIS
# =========================================================

def build_bhava_bala_engine_analysis(
    chart,
    shadbala_analysis=None,
    aspect_analysis=None,
):
    """
    Build Bhava Bala analysis.

    Bhava Bala is calculated separately from the
    normal house analysis.

    It can use:
        - Kundli chart
        - Shadbala data
        - Planetary aspect data
    """

    try:

        shadbala_data = None

        if isinstance(
            shadbala_analysis,
            dict
        ):

            shadbala_data = (
                shadbala_analysis.get(
                    "data"
                )
            )

        aspect_data = None

        if isinstance(
            aspect_analysis,
            dict
        ):

            aspect_data = (
                aspect_analysis.get(
                    "data"
                )
            )

        result = build_bhava_bala_analysis(
            chart,
            shadbala_data,
            aspect_data,
        )

        return {
            "success": True,
            "data": result,
            "error": None,
        }

    except Exception as exc:

        print()
        print(
            "[WARNING] Bhava Bala analysis failed"
        )

        print(
            f"Error: {type(exc).__name__}: {exc}"
        )

        return {
            "success": False,
            "data": None,
            "error":
                f"{type(exc).__name__}: "
                f"{str(exc)}",
        }


# =========================================================
# ASPECT ANALYSIS
# =========================================================

def build_aspect_engine_analysis(chart):

    planets = copy_planets(
        chart.get(
            "planets",
            []
        )
    )

    return run_module(
        "Aspects",
        build_aspect_analysis,
        planets
    )


# =========================================================
# DIGNITY ANALYSIS
# =========================================================

def build_dignity_engine_analysis(chart):

    planets = copy_planets(
        chart.get(
            "planets",
            []
        )
    )

    return run_module(
        "Dignity",
        build_dignity_analysis,
        planets
    )


# =========================================================
# COMBUSTION ANALYSIS
# =========================================================

def build_combustion_engine_analysis(chart):

    planets = copy_planets(
        chart.get(
            "planets",
            []
        )
    )

    return run_module(
        "Combustion",
        build_combustion_table,
        planets
    )


# =========================================================
# SHADBALA ANALYSIS
# =========================================================

def build_shadbala_engine_analysis(chart):

    planets = copy_planets(
        chart.get(
            "planets",
            []
        )
    )

    # First try chart-aware calculation.
    try:

        result = build_shadbala_analysis(
            planets,
            chart
        )

        return {
            "success": True,
            "data": result,
            "error": None,
        }

    except TypeError:

        pass

    except Exception as exc:

        return {
            "success": False,
            "data": None,
            "error":
                f"{type(exc).__name__}: "
                f"{str(exc)}",
        }


    # Try planets-only calculation.
    return run_module(
        "Shadbala",
        build_shadbala_analysis,
        planets
    )


# =========================================================
# ASHTAKAVARGA ANALYSIS
# =========================================================

def build_ashtakavarga_engine_analysis(chart):

    planets = copy_planets(
        chart.get(
            "planets",
            []
        )
    )

    ascendant = chart.get(
        "ascendant",
        {}
    )

    ascendant_sign_index = (
        ascendant.get(
            "sign_index"
        )
    )

    # -----------------------------------------------------
    # Try planets + ascendant sign
    # -----------------------------------------------------

    try:

        result = build_ashtakavarga_analysis(
            planets,
            ascendant_sign_index
        )

        return {
            "success": True,
            "data": result,
            "error": None,
        }

    except TypeError:

        pass

    except Exception as exc:

        return {
            "success": False,
            "data": None,
            "error":
                f"{type(exc).__name__}: "
                f"{str(exc)}",
        }


    # -----------------------------------------------------
    # Try planets only
    # -----------------------------------------------------

    return run_module(
        "Ashtakavarga",
        build_ashtakavarga_analysis,
        planets
    )


# =========================================================
# NAVAMSA ANALYSIS
# =========================================================

def build_navamsa_engine_analysis(chart):

    planets = copy_planets(
        chart.get(
            "planets",
            []
        )
    )

    return run_module(
        "Navamsa",
        build_navamsa,
        planets
    )


# =========================================================
# DASHA ANALYSIS
# =========================================================

def build_dasha_engine_analysis(chart):

    julian_day = chart.get(
        "julian_day"
    )

    if julian_day is None:

        return {
            "success": False,
            "data": None,
            "error":
                "Julian day is missing.",
        }

    return run_module(
        "Dasha",
        get_current_dasha,
        julian_day
    )


# =========================================================
# YOGA ANALYSIS
# =========================================================

def build_yoga_engine_analysis(chart):

    return run_module(
        "Yoga",
        detect_yogas,
        chart
    )


# =========================================================
# COMPLETE ANALYSIS
# =========================================================

def build_complete_analysis(chart):
    """
    Main integration function.

    This combines every astrology engine into
    one complete analysis object.
    """

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    validation = validate_chart(
        chart
    )

    if not validation["valid"]:

        raise ValueError(
            "Invalid chart: "
            + "; ".join(
                validation["errors"]
            )
        )


    print()
    print("=" * 70)
    print(
        "AI JYOTISH COMPLETE ANALYSIS"
    )
    print("=" * 70)


    # -----------------------------------------------------
    # MAIN ANALYSIS OBJECT
    # -----------------------------------------------------

    analysis = {

        "analysis_engine": {

            "name":
                "AI Jyotish Analysis Engine",

            "version":
                ANALYSIS_ENGINE_VERSION,

            "generated_at":
                datetime.utcnow().isoformat()
                + "Z",

        },

        "basic":
            build_basic_analysis(
                chart
            ),

    }


    # =====================================================
    # 1. PLANETS
    # =====================================================

    print(
        "[1/11] Calculating planets..."
    )

    planet_analysis = (
        build_planet_engine_analysis(
            chart
        )
    )

    analysis["planets"] = (
        planet_analysis
    )


    # =====================================================
    # 2. NAKSHATRA
    # =====================================================

    print(
        "[2/11] Calculating nakshatras..."
    )

    nakshatra_analysis = (
        build_nakshatra_engine_analysis(
            chart
        )
    )

    analysis["nakshatra"] = (
        nakshatra_analysis
    )


    # =====================================================
    # 3. HOUSES
    # =====================================================

    print(
        "[3/11] Calculating houses..."
    )

    house_analysis = (
        build_house_engine_analysis(
            chart
        )
    )

    analysis["houses"] = (
        house_analysis
    )


    # =====================================================
    # 4. ASPECTS
    # =====================================================

    print(
        "[4/11] Calculating aspects..."
    )

    aspect_analysis = (
        build_aspect_engine_analysis(
            chart
        )
    )

    analysis["aspects"] = (
        aspect_analysis
    )


    # =====================================================
    # 5. DIGNITY
    # =====================================================

    print(
        "[5/11] Calculating dignity..."
    )

    dignity_analysis = (
        build_dignity_engine_analysis(
            chart
        )
    )

    analysis["dignity"] = (
        dignity_analysis
    )


    # =====================================================
    # 6. COMBUSTION
    # =====================================================

    print(
        "[6/11] Calculating combustion..."
    )

    combustion_analysis = (
        build_combustion_engine_analysis(
            chart
        )
    )

    analysis["combustion"] = (
        combustion_analysis
    )


    # =====================================================
    # 7. SHADBALA
    # =====================================================

    print(
        "[7/11] Calculating Shadbala..."
    )

    shadbala_analysis = (
        build_shadbala_engine_analysis(
            chart
        )
    )

    analysis["shadbala"] = (
        shadbala_analysis
    )
    # =====================================================
    # BHAVA BALA
    # =====================================================

    print(
        "[7B] Calculating Bhava Bala..."
    )

    bhava_bala_analysis = (
        build_bhava_bala_engine_analysis(
            chart,
            shadbala_analysis,
            aspect_analysis,
        )
    )

    analysis["bhava_bala"] = (
        bhava_bala_analysis)
    

    



    # =====================================================
    # 8. ASHTAKAVARGA
    # =====================================================

    print(
        "[8/11] Calculating Ashtakavarga..."
    )

    ashtakavarga_analysis = (
        build_ashtakavarga_engine_analysis(
            chart
        )
    )

    analysis["ashtakavarga"] = (
        ashtakavarga_analysis
    )


    # =====================================================
    # 9. NAVAMSA
    # =====================================================

    print(
        "[9/11] Calculating Navamsa..."
    )

    navamsa_analysis = (
        build_navamsa_engine_analysis(
            chart
        )
    )

    analysis["navamsa"] = (
        navamsa_analysis
    )


    # =====================================================
    # 10. DASHA
    # =====================================================

    print(
        "[10/11] Calculating Vimshottari Dasha..."
    )

    dasha_analysis = (
        build_dasha_engine_analysis(
            chart
        )
    )

    analysis["dashas"] = (
        dasha_analysis
    )


    # =====================================================
    # 11. YOGA
    # =====================================================

    print(
        "[11/11] Detecting Yogas..."
    )

    yoga_analysis = (
        build_yoga_engine_analysis(
            chart
        )
    )

    analysis["yogas"] = (
        yoga_analysis
    )


    # =====================================================
    # MODULE STATUS
    # =====================================================

    module_status = {

        "planets":
            planet_analysis["success"],

        "nakshatra":
            nakshatra_analysis["success"],

        "houses":
            house_analysis["success"],

        "aspects":
            aspect_analysis["success"],

        "dignity":
            dignity_analysis["success"],

        "combustion":
            combustion_analysis["success"],

        "shadbala":
            shadbala_analysis["success"],

        "ashtakavarga":
            ashtakavarga_analysis["success"],

        "navamsa":
            navamsa_analysis["success"],

        "dashas":
            dasha_analysis["success"],

        "yogas":
            yoga_analysis["success"],

    }


    successful_modules = sum(

        1

        for status
        in module_status.values()

        if status

    )


    total_modules = len(
        module_status
    )


    # =====================================================
    # SUMMARY
    # =====================================================

    analysis["summary"] = {

        "modules":
            module_status,

        "successful_modules":
            successful_modules,

        "total_modules":
            total_modules,

        "completion_percentage":
            round(
                (
                    successful_modules
                    / total_modules
                ) * 100,
                2
            ),

        "complete":
            successful_modules
            == total_modules,

    }


    # =====================================================
    # COMPLETION
    # =====================================================

    print()
    print("=" * 70)

    print(
        "ANALYSIS COMPLETE"
    )

    print(
        f"Successful modules: "
        f"{successful_modules}/{total_modules}"
    )

    print(
        f"Completion: "
        f"{analysis['summary']['completion_percentage']}%"
    )

    print("=" * 70)


    return analysis


# =========================================================
# ATTACH ANALYSIS TO CHART
# =========================================================

def attach_complete_analysis(chart):
    """
    Add the complete analysis directly to the
    existing Kundli dictionary.

    Result:

        chart["analysis"]
    """

    analysis = build_complete_analysis(
        chart
    )

    chart["analysis"] = analysis

    return chart


# =========================================================
# BUILD AI-READY CHART
# =========================================================

def build_ai_ready_chart(chart):
    """
    Prepare a complete chart for Gemini.

    Returns:

        {
            "chart": original_chart,
            "analysis": complete_analysis
        }
    """

    analysis = build_complete_analysis(
        chart
    )

    return {

        "chart":
            chart,

        "analysis":
            analysis,

    }


# =========================================================
# GET MODULE STATUS
# =========================================================

def get_analysis_status(analysis):
    """
    Return a simple module status report.
    """

    if not isinstance(
        analysis,
        dict
    ):

        return {}

    summary = analysis.get(
        "summary",
        {}
    )

    return summary.get(
        "modules",
        {}
    )


# =========================================================
# CHECK WHETHER ANALYSIS IS COMPLETE
# =========================================================

def is_analysis_complete(analysis):
    """
    Return True when all modules completed successfully.
    """

    if not isinstance(
        analysis,
        dict
    ):

        return False

    summary = analysis.get(
        "summary",
        {}
    )

    return bool(
        summary.get(
            "complete",
            False
        )
    )


# =========================================================
# STANDALONE IMPORT TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print(
        "AI JYOTISH ANALYSIS ENGINE TEST"
    )
    print("=" * 70)

    print()
    print(
        "Analysis engine imported successfully."
    )

    print(
        "Engine version:",
        ANALYSIS_ENGINE_VERSION
    )

    print()
    print(
        "Loaded modules:"
    )

    print(
        "  [OK] Planets"
    )

    print(
        "  [OK] Nakshatra"
    )

    print(
        "  [OK] Houses"
    )

    print(
        "  [OK] Aspects"
    )

    print(
        "  [OK] Dignity"
    )

    print(
        "  [OK] Combustion"
    )

    print(
        "  [OK] Shadbala"
    )

    print(
        "  [OK] Ashtakavarga"
    )

    print(
        "  [OK] Navamsa"
    )

    print(
        "  [OK] Dasha"
    )

    print(
        "  [OK] Yoga"
    )

    print()
    print("=" * 70)
    print(
        "ANALYSIS ENGINE IMPORT TEST COMPLETED"
    )
    print("=" * 70)