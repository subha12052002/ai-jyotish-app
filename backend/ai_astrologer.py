"""
AI JYOTISH
Gemini AI Astrologer

Uses Google Gemini 3.7 Flash.
"""

import os
import json
from dotenv import load_dotenv
from google import genai

# Load .env BEFORE reading environment variables
load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash"
)


# ============================================================
# GEMINI CLIENT
# ============================================================

client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        print("[OK] Gemini client initialized")
        print(f"[OK] Gemini model: {MODEL}")
    except Exception as exc:
        print("[WARNING] Gemini client initialization failed")
        print(f"Error: {type(exc).__name__}: {exc}")
        client = None
else:
    print("[WARNING] GEMINI_API_KEY is not configured")


# ============================================================
# CHART CLEANER
# ============================================================

def make_json_safe(data):
    """
    Convert chart data into JSON-safe Python objects.
    """

    if data is None:
        return None

    if isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, dict):
        return {
            str(key): make_json_safe(value)
            for key, value in data.items()
        }

    if isinstance(data, (list, tuple)):
        return [
            make_json_safe(value)
            for value in data
        ]

    try:
        return float(data)
    except Exception:
        return str(data)


# ============================================================
# CHART SUMMARY
# ============================================================

def build_chart_context(chart):
    """
    Convert complete Kundli + analysis into a clean JSON context
    for Gemini.
    """

    safe_chart = make_json_safe(chart)

    return json.dumps(
        safe_chart,
        indent=2,
        ensure_ascii=False
    )


# ============================================================
# SYSTEM PROMPT
# ============================================================

def build_system_prompt():
    return """
You are AI Jyotish, an advanced Vedic astrology assistant.

You analyze a person's Kundli using traditional Vedic astrology
principles.

The chart data provided to you may contain:

- Birth details
- Ascendant
- Planetary positions
- Houses
- Nakshatras
- Planetary dignity
- Combustion
- Aspects
- Shadbala
- Ashtakavarga
- Navamsa
- Vimshottari Dasha
- Yogas
- Other calculated astrology information

IMPORTANT RULES:

1. Use the supplied calculated chart data.
2. Do not invent planetary positions.
3. Do not invent birth information.
4. Do not claim calculations that are not present in the chart.
5. Clearly distinguish calculated facts from interpretation.
6. Give explanations in simple language.
7. When discussing timing, use the supplied Dasha information.
8. Consider the Ascendant, Moon, Sun, houses, lords, aspects,
   dignity, Nakshatra, Navamsa, Yogas and Dashas together.
9. Avoid absolute guarantees about the future.
10. Present astrology as traditional/spiritual guidance rather
    than scientific certainty.

When answering a user's question:

- First understand the question.
- Identify the relevant chart factors.
- Explain the astrological reasoning.
- Give a practical interpretation.
- If the chart does not contain enough information, say so.

You are an astrology assistant, not a medical, legal or financial
professional.
"""


# ============================================================
# BUILD USER PROMPT
# ============================================================

def build_user_prompt(question, chart):
    chart_context = build_chart_context(chart)

    return f"""
Here is the person's complete Vedic astrology chart:

================ CHART DATA ================

{chart_context}

================ USER QUESTION ================

{question}

================ INSTRUCTIONS ================

Answer the user's question using the supplied Kundli.

Explain:

1. What chart factors are relevant.
2. What those factors traditionally indicate.
3. How those factors relate to the user's question.
4. The overall interpretation.
5. Any important limitations or uncertainty.

Do not invent information that is not present in the chart.

Give the answer in a clear and natural way.
"""


# ============================================================
# GEMINI REQUEST
# ============================================================

def ask_gemini(prompt):
    """
    Send a prompt to Gemini.
    """

    if not API_KEY:
        return {
            "success": False,
            "answer": (
                "Gemini API key is not configured. "
                "Please configure GEMINI_API_KEY in your .env file."
            ),
            "error": "GEMINI_API_KEY missing"
        }

    if client is None:
        return {
            "success": False,
            "answer": (
                "Gemini client could not be initialized."
            ),
            "error": "Gemini client unavailable"
        }

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        text = getattr(response, "text", None)

        if not text:
            return {
                "success": False,
                "answer": "Gemini returned an empty response.",
                "error": "Empty Gemini response"
            }

        return {
            "success": True,
            "answer": text.strip(),
            "error": None
        }

    except Exception as exc:

        print()
        print("[WARNING] Gemini request failed")
        print(f"Error: {type(exc).__name__}: {exc}")
        print()

        return {
            "success": False,
            "answer": (
                "I could not contact Gemini right now. "
                "Please try again."
            ),
            "error": f"{type(exc).__name__}: {str(exc)}"
        }


# ============================================================
# MAIN AI ASTROLOGER FUNCTION
# ============================================================

def answer_question(question, chart):
    """
    Main function used by Flask /api/ai/ask.

    Parameters:
        question: User's astrology question
        chart: Complete Kundli dictionary

    Returns:
        Dictionary containing Gemini answer.
    """

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    if not question:
        return {
            "success": False,
            "answer": "Please enter a question.",
            "error": "Question is empty"
        }

    if not isinstance(question, str):
        question = str(question)

    question = question.strip()

    if not question:
        return {
            "success": False,
            "answer": "Please enter a question.",
            "error": "Question is empty"
        }

    # --------------------------------------------------------
    # Validate chart
    # --------------------------------------------------------

    if not isinstance(chart, dict):
        return {
            "success": False,
            "answer": "A valid Kundli is required.",
            "error": "Invalid chart"
        }

    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    try:

        prompt = build_system_prompt()

        prompt += "\n\n"

        prompt += build_user_prompt(
            question,
            chart
        )

    except Exception as exc:

        return {
            "success": False,
            "answer": "Could not prepare the astrology analysis.",
            "error": f"{type(exc).__name__}: {str(exc)}"
        }

    # --------------------------------------------------------
    # Ask Gemini
    # --------------------------------------------------------

    result = ask_gemini(prompt)

    return result


# ============================================================
# SIMPLE TEST
# ============================================================

def test_gemini():
    """
    Simple Gemini connection test.
    """

    result = ask_gemini(
        "Say exactly: AI Jyotish Gemini connection successful."
    )

    print()
    print("=" * 60)
    print("GEMINI TEST")
    print("=" * 60)

    if result["success"]:
        print("[OK] Gemini response:")
        print(result["answer"])
    else:
        print("[FAILED]")
        print(result["error"])

    print("=" * 60)
    print()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("AI JYOTISH - AI ASTROLOGER TEST")
    print("=" * 60)

    print()
    print("Gemini API configured:", bool(API_KEY))
    print("Gemini model:", MODEL)
    print("answer_question:", callable(answer_question))

    print()

    if API_KEY:
        test_gemini()
    else:
        print("[WARNING] Add GEMINI_API_KEY to .env first.")

    print("=" * 60)