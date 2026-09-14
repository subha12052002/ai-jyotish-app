"""
AI Jyotish - AI Prompt Builder

Converts calculated Vedic astrology data into structured
prompts for the AI astrologer.

This module does NOT call an AI API.
It only prepares high-quality context and prompts.

The actual AI/API communication will be handled by
ai_astrologer.py.
"""

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are AI Jyotish, an expert Vedic astrology interpretation
assistant.

Your task is to interpret a calculated Vedic astrology chart
using traditional Jyotish principles.

IMPORTANT RULES:

1. Use the supplied calculated chart data as the source of truth.
2. Do not invent planetary positions, houses, dashas, yogas,
   nakshatras, or degrees that are not present in the data.
3. Clearly distinguish calculated facts from interpretation.
4. Use Vedic / sidereal astrology terminology.
5. Consider:
   - Lagna
   - Houses
   - House lords
   - Planetary placements
   - Planetary dignity
   - Nakshatras
   - Aspects
   - Combustion
   - Shadbala
   - Ashtakavarga
   - Yogas
   - Vimshottari Dasha
   - Navamsa when available
6. Never present astrology as scientifically proven fact.
7. Avoid deterministic statements such as "this will definitely
   happen."
8. Use phrases such as:
   - "This may indicate..."
   - "Traditionally, this placement is associated with..."
   - "This suggests a tendency toward..."
9. When discussing difficult placements, remain balanced and
   explain both challenges and constructive possibilities.
10. Do not create fear regarding death, severe illness,
    accidents, disasters, or other catastrophic events.
11. Do not claim certainty about marriage, divorce, death,
    pregnancy, wealth, criminal activity, or medical outcomes.
12. For health-related questions, provide only traditional
    astrological interpretation and recommend qualified
    professional medical advice for actual health concerns.
13. For financial questions, provide general astrological
    interpretation, not guaranteed financial predictions.
14. Give practical, constructive guidance.
15. Explain technical Jyotish terms in simple language when
    appropriate.

The response should be clear, structured, useful, and personalized
to the supplied chart.
"""


# ============================================================
# GENERAL PROMPT
# ============================================================

GENERAL_PROMPT = """
Analyze the following Vedic astrology chart.

Provide:

1. Overall chart overview
2. Personality tendencies
3. Strongest planetary influences
4. Challenging planetary influences
5. Important houses
6. Important yogas
7. Nakshatra interpretation
8. Current Mahadasha / Antardasha
9. Important strengths and weaknesses
10. Practical guidance

Do not invent information that is absent from the chart.
"""


# ============================================================
# PERSONALITY PROMPT
# ============================================================

PERSONALITY_PROMPT = """
Analyze the person's personality using the supplied Vedic chart.

Focus on:

1. Ascendant
2. Ascendant lord
3. Moon sign
4. Moon nakshatra
5. Sun
6. Strong planets
7. Weak planets
8. Important planetary aspects
9. Relevant yogas

Explain:

- Basic personality
- Emotional nature
- Thinking style
- Communication style
- Strengths
- Weaknesses
- Social behavior
- Natural talents

Keep the interpretation balanced and avoid deterministic claims.
"""


# ============================================================
# CAREER PROMPT
# ============================================================

CAREER_PROMPT = """
Analyze career and professional tendencies from the supplied
Vedic astrology chart.

Focus especially on:

1. 10th house
2. 10th lord
3. 6th house
4. 7th house
5. 2nd house
6. 11th house
7. Sun
8. Saturn
9. Mercury
10. Jupiter
11. Relevant yogas
12. Shadbala
13. Current and upcoming dashas

Discuss:

- Suitable career environments
- Leadership potential
- Technical / analytical tendencies
- Business potential
- Job vs entrepreneurship tendencies
- Career strengths
- Potential professional challenges
- Periods that may traditionally support career development

Do not guarantee employment, promotions, business success,
or income.
"""


# ============================================================
# EDUCATION PROMPT
# ============================================================

EDUCATION_PROMPT = """
Analyze education and learning tendencies using the supplied
Vedic astrology chart.

Focus on:

1. 2nd house
2. 4th house
3. 5th house
4. 9th house
5. Mercury
6. Jupiter
7. Moon
8. Relevant Nakshatras
9. Planetary strength
10. Current Dasha

Discuss:

- Learning style
- Academic strengths
- Concentration tendencies
- Analytical ability
- Creative ability
- Higher education tendencies
- Areas of study that may suit the chart

Avoid guaranteeing academic results.
"""


# ============================================================
# RELATIONSHIP PROMPT
# ============================================================

RELATIONSHIP_PROMPT = """
Analyze relationship and marriage tendencies from the supplied
Vedic astrology chart.

Focus on:

1. 5th house
2. 7th house
3. 7th lord
4. Venus
5. Jupiter
6. Moon
7. Relevant aspects
8. Relevant yogas
9. Navamsa if available
10. Current Dasha

Discuss:

- Relationship style
- Emotional needs
- Communication
- Partner qualities traditionally associated with the chart
- Relationship strengths
- Potential challenges
- Areas requiring maturity and communication

Do not make deterministic claims about marriage, divorce,
or exact timing.
"""


# ============================================================
# FINANCE PROMPT
# ============================================================

FINANCE_PROMPT = """
Analyze financial tendencies using the supplied Vedic chart.

Focus on:

1. 2nd house
2. 2nd lord
3. 5th house
4. 9th house
5. 11th house
6. 11th lord
7. Jupiter
8. Venus
9. Mercury
10. Shadbala
11. Ashtakavarga
12. Current Dasha

Discuss:

- Earning tendencies
- Saving tendencies
- Financial discipline
- Business vs salary tendencies
- Wealth-supporting planetary factors
- Potential financial challenges
- Periods that may traditionally be supportive

Do not guarantee profits, wealth, investment returns, or financial
success. Avoid specific investment instructions.
"""


# ============================================================
# HEALTH PROMPT
# ============================================================

HEALTH_PROMPT = """
Provide a traditional Vedic astrology interpretation related to
general wellness tendencies.

Focus on:

1. Ascendant
2. Ascendant lord
3. 6th house
4. 8th house
5. 12th house
6. Sun
7. Moon
8. Relevant planetary afflictions
9. Planetary strength
10. Current Dasha

IMPORTANT:

Do not diagnose diseases.
Do not predict death.
Do not claim that a planetary placement causes a medical
condition.

Use language such as:

"This traditional astrological framework associates this
placement with..."

For actual symptoms or medical concerns, recommend consultation
with a qualified healthcare professional.
"""


# ============================================================
# DASHĀ PROMPT
# ============================================================

DASHA_PROMPT = """
Analyze the supplied Vimshottari Dasha information.

Explain:

1. Current Mahadasha
2. Current Antardasha
3. Planet ruling the period
4. Natal placement of that planet
5. House ownership
6. Planetary dignity
7. Nakshatra
8. Aspects
9. Shadbala
10. Relevant yogas

Then discuss the likely themes of the period.

Do not give guaranteed event predictions.
"""


# ============================================================
# YOGA PROMPT
# ============================================================

YOGA_PROMPT = """
Analyze the important yogas detected in the supplied Vedic chart.

For each yoga:

1. Explain what the yoga means.
2. Explain which planets create it.
3. Explain the houses/signs involved.
4. Explain whether the planets appear strong or weak.
5. Explain how the yoga may manifest.
6. Mention relevant Dasha activation when possible.

Do not exaggerate weak or partially formed yogas.
"""


# ============================================================
# TRANSIT PROMPT
# ============================================================

TRANSIT_PROMPT = """
Analyze the supplied transit information together with the natal
Vedic chart.

Consider:

1. Natal planetary positions
2. Current transiting planets
3. Houses affected
4. Natal planetary strength
5. Ashtakavarga scores
6. Current Mahadasha
7. Current Antardasha

Explain the major themes and areas of attention.

Do not present transit interpretations as guaranteed events.
"""


# ============================================================
# NAVAMSA PROMPT
# ============================================================

NAVAMSA_PROMPT = """
Analyze the supplied Navamsa (D9) information.

Use it together with the Rashi chart.

Focus on:

1. Navamsa Ascendant if available
2. Planetary Navamsa signs
3. Planetary dignity
4. Marriage and partnership themes
5. Dharma and maturity
6. Strength confirmation from Rashi and Navamsa

Do not interpret Navamsa in isolation when relevant Rashi
information is available.
"""


# ============================================================
# QUESTION PROMPT
# ============================================================

QUESTION_PROMPT = """
Answer the user's astrology question using the supplied
calculated Vedic chart.

User question:

{question}

Instructions:

1. Directly answer the question.
2. Use relevant chart factors only.
3. Mention the planetary/houses/yogas supporting the interpretation.
4. Explain uncertainty where appropriate.
5. Do not invent missing chart information.
6. Avoid deterministic predictions.
7. Keep the answer practical and understandable.
"""


# ============================================================
# CHART SERIALIZATION
# ============================================================

def safe_value(value):
    """Convert values into prompt-safe text."""

    if value is None:
        return "Not available"

    if isinstance(value, bool):
        return "Yes" if value else "No"

    if isinstance(value, float):
        return round(value, 4)

    return value


def format_dict(data, indent=0):
    """Recursively format dictionaries."""

    if not isinstance(data, dict):
        return str(safe_value(data))

    lines = []

    for key, value in data.items():

        label = str(key).replace(
            "_",
            " ",
        ).title()

        if isinstance(value, dict):

            lines.append(
                " " * indent + f"{label}:"
            )

            lines.append(
                format_dict(
                    value,
                    indent + 2,
                )
            )

        elif isinstance(value, list):

            lines.append(
                " " * indent + f"{label}:"
            )

            for item in value:

                if isinstance(item, dict):

                    lines.append(
                        format_dict(
                            item,
                            indent + 2,
                        )
                    )

                else:

                    lines.append(
                        " " * (indent + 2)
                        + str(safe_value(item))
                    )

        else:

            lines.append(
                " " * indent
                + f"{label}: {safe_value(value)}"
            )

    return "\n".join(lines)


def format_planets(planets):
    """Format planetary information."""

    if not planets:
        return "No planetary data available."

    lines = []

    for planet in planets:

        if not isinstance(planet, dict):
            continue

        name = planet.get(
            "name",
            "Unknown",
        )

        sign = planet.get(
            "sign",
            "Unknown",
        )

        degree = planet.get(
            "degree",
            "Unknown",
        )

        house = planet.get(
            "house",
            planet.get(
                "house_number",
                "Unknown",
            ),
        )

        retrograde = planet.get(
            "retrograde",
            False,
        )

        lines.append(
            f"- {name}: "
            f"Sign={sign}, "
            f"Degree={degree}, "
            f"House={house}, "
            f"Retrograde={retrograde}"
        )

        # Include calculated analysis if present.
        for field in (
            "dignity",
            "combustion",
            "shadbala",
            "nakshatra",
        ):

            if field in planet:

                lines.append(
                    f"  {field.title()}: "
                    f"{planet[field]}"
                )

    return "\n".join(lines)


# ============================================================
# CHART CONTEXT
# ============================================================

def build_chart_context(chart):
    """
    Convert the complete chart into AI-readable context.
    """

    if not isinstance(chart, dict):
        return "No chart data supplied."

    sections = []

    sections.append(
        "=== BIRTH INFORMATION ==="
    )

    birth_info = chart.get(
        "birth_info"
    )

    if birth_info:
        sections.append(
            format_dict(
                birth_info
            )
        )

    sections.append(
        "\n=== ASCENDANT ==="
    )

    ascendant = chart.get(
        "ascendant"
    )

    if isinstance(ascendant, dict):
        sections.append(
            format_dict(
                ascendant
            )
        )

    else:
        sections.append(
            str(
                safe_value(
                    ascendant
                )
            )
        )

    sections.append(
        "\n=== PLANETS ==="
    )

    sections.append(
        format_planets(
            chart.get(
                "planets",
                []
            )
        )
    )

    for key, title in [
        ("houses", "HOUSES"),
        ("nakshatras", "NAKSHATRAS"),
        ("dashas", "DASHAS"),
        ("yogas", "YOGAS"),
        ("dignity", "DIGNITY"),
        ("combustion", "COMBUSTION"),
        ("shadbala", "SHADBALA"),
        ("ashtakavarga", "ASHTAKAVARGA"),
        ("navamsa", "NAVAMSA"),
        ("aspects", "ASPECTS"),
    ]:

        if key not in chart:
            continue

        sections.append(
            f"\n=== {title} ==="
        )

        sections.append(
            format_dict(
                chart[key]
            )
        )

    return "\n".join(
        sections
    )


# ============================================================
# MASTER PROMPT BUILDER
# ============================================================

PROMPT_MAP = {
    "general": GENERAL_PROMPT,
    "personality": PERSONALITY_PROMPT,
    "career": CAREER_PROMPT,
    "education": EDUCATION_PROMPT,
    "relationship": RELATIONSHIP_PROMPT,
    "marriage": RELATIONSHIP_PROMPT,
    "finance": FINANCE_PROMPT,
    "money": FINANCE_PROMPT,
    "health": HEALTH_PROMPT,
    "dasha": DASHA_PROMPT,
    "yoga": YOGA_PROMPT,
    "transit": TRANSIT_PROMPT,
    "navamsa": NAVAMSA_PROMPT,
}


def get_topic_prompt(topic):
    """Return prompt template for a topic."""

    if not topic:
        return GENERAL_PROMPT

    topic = str(
        topic
    ).strip().lower()

    return PROMPT_MAP.get(
        topic,
        GENERAL_PROMPT,
    )


def build_analysis_prompt(
    chart,
    topic="general",
):
    """
    Build a complete AI analysis prompt.
    """

    chart_context = build_chart_context(
        chart
    )

    topic_prompt = get_topic_prompt(
        topic
    )

    return f"""
{topic_prompt}

=== CALCULATED CHART DATA ===

{chart_context}

=== END CHART DATA ===

Provide the interpretation now.
"""


def build_question_prompt(
    chart,
    question,
):
    """Build a custom user-question prompt."""

    chart_context = build_chart_context(
        chart
    )

    return (
        QUESTION_PROMPT.format(
            question=question
        )
        + "\n\n"
        + "=== CALCULATED CHART DATA ===\n\n"
        + chart_context
        + "\n\n=== END CHART DATA ==="
    )


# ============================================================
# AI RESPONSE STRUCTURE
# ============================================================

def get_response_structure(topic):
    """
    Return recommended response sections.
    """

    topic = (
        str(topic).strip().lower()
        if topic
        else "general"
    )

    structures = {

        "general": [
            "Overall Chart",
            "Personality",
            "Planetary Strengths",
            "Important Houses",
            "Yogas",
            "Dashas",
            "Key Guidance",
        ],

        "personality": [
            "Core Personality",
            "Emotional Nature",
            "Thinking Style",
            "Strengths",
            "Challenges",
            "Practical Guidance",
        ],

        "career": [
            "Career Overview",
            "Professional Strengths",
            "Suitable Work Areas",
            "Job vs Business",
            "Career Challenges",
            "Dasha Influence",
            "Practical Guidance",
        ],

        "education": [
            "Learning Style",
            "Academic Strengths",
            "Study Tendencies",
            "Suitable Fields",
            "Challenges",
            "Practical Guidance",
        ],

        "relationship": [
            "Relationship Nature",
            "Emotional Needs",
            "Partner Tendencies",
            "Relationship Strengths",
            "Challenges",
            "Practical Guidance",
        ],

        "marriage": [
            "Marriage Overview",
            "Partner Tendencies",
            "Relationship Dynamics",
            "Strengths",
            "Potential Challenges",
            "Dasha Influence",
            "Practical Guidance",
        ],

        "finance": [
            "Financial Overview",
            "Earning Tendencies",
            "Saving Tendencies",
            "Financial Strengths",
            "Potential Challenges",
            "Dasha Influence",
            "Practical Guidance",
        ],

        "health": [
            "Traditional Wellness Interpretation",
            "Planetary Factors",
            "Potential Tendencies",
            "General Wellness Guidance",
            "Professional Medical Disclaimer",
        ],

        "dasha": [
            "Current Mahadasha",
            "Current Antardasha",
            "Planetary Influence",
            "Main Themes",
            "Opportunities",
            "Challenges",
            "Practical Guidance",
        ],

        "yoga": [
            "Important Yogas",
            "Formation",
            "Strength",
            "Potential Manifestation",
            "Dasha Activation",
        ],

        "transit": [
            "Current Transit Themes",
            "Affected Houses",
            "Ashtakavarga Support",
            "Dasha Interaction",
            "Opportunities",
            "Areas of Attention",
        ],

        "navamsa": [
            "Navamsa Overview",
            "Planetary Strength",
            "Marriage Themes",
            "Dharma and Maturity",
            "Rashi-D9 Comparison",
        ],
    }

    return structures.get(
        topic,
        structures["general"],
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("AI PROMPTS MODULE TEST")
    print("=" * 70)

    sample_chart = {

        "birth_info": {
            "date": "1998-01-15",
            "time": "10:30",
            "latitude": 22.57,
            "longitude": 88.36,
        },

        "ascendant": {
            "sign": "Aries",
            "sign_index": 0,
            "degree": 15.5,
        },

        "planets": [
            {
                "name": "Sun",
                "sign": "Capricorn",
                "sign_index": 9,
                "degree": 1.2,
                "house": 10,
                "retrograde": False,
            },
            {
                "name": "Moon",
                "sign": "Taurus",
                "sign_index": 1,
                "degree": 12.5,
                "house": 2,
                "retrograde": False,
            },
            {
                "name": "Mars",
                "sign": "Scorpio",
                "sign_index": 7,
                "degree": 8.2,
                "house": 8,
                "retrograde": False,
            },
        ],

        "dashas": {
            "mahadasha": "Jupiter",
            "antardasha": "Venus",
        },

        "yogas": [
            "Example Yoga"
        ],

    }

    # --------------------------------------------------------
    # General prompt
    # --------------------------------------------------------

    prompt = build_analysis_prompt(
        sample_chart,
        "general",
    )

    print("\nGENERAL PROMPT CREATED")
    print("-" * 70)

    print(
        prompt[:1500]
    )

    # --------------------------------------------------------
    # Career prompt
    # --------------------------------------------------------

    career_prompt = build_analysis_prompt(
        sample_chart,
        "career",
    )

    print("\nCAREER PROMPT CREATED")
    print("-" * 70)

    print(
        career_prompt[:500]
    )

    # --------------------------------------------------------
    # Question prompt
    # --------------------------------------------------------

    question_prompt = build_question_prompt(
        sample_chart,
        "What career direction may suit me?",
    )

    print("\nQUESTION PROMPT CREATED")
    print("-" * 70)

    print(
        question_prompt[:500]
    )

    # --------------------------------------------------------
    # Response structure
    # --------------------------------------------------------

    print("\nRESPONSE STRUCTURE")
    print("-" * 70)

    for section in get_response_structure(
        "career"
    ):
        print(
            f"- {section}"
        )

    print("\n" + "=" * 70)
    print("AI PROMPTS MODULE TEST COMPLETED")
    print("=" * 70)