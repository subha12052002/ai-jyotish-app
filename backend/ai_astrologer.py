import os
import json

from google import genai


# =========================================================
# GEMINI CLIENT
# =========================================================

api_key = os.getenv(
    "GEMINI_API_KEY"
)

client = None

if api_key:

    client = genai.Client(
        api_key=api_key
    )


# =========================================================
# AI ASTROLOGER
# =========================================================

def ask_astrologer(
    user_question,
    kundli
):

    if client is None:

        return {
            "success": False,
            "message":
                "Gemini API key is not configured."
        }

    chart_json = json.dumps(
        kundli,
        indent=2
    )

    prompt = f"""
You are an AI assistant specializing
in traditional Indian/Vedic astrology.

The following is calculated chart data:

{chart_json}

User question:

{user_question}

Important rules:

- Present astrology as a traditional/spiritual
  interpretation, not scientific certainty.
- Do not make medical, legal or financial guarantees.
- Do not frighten the user.
- Do not claim unavoidable death or disaster.
- Explain important chart factors clearly.
- Keep the answer friendly and practical.

Structure:

1. Short answer
2. Astrological interpretation
3. Important chart factors
4. Practical guidance

Keep the answer easy to understand.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "success": True,
            "answer": response.text
        }

    except Exception as error:

        return {
            "success": False,
            "message": str(error)
        }