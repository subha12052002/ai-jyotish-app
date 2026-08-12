import os
import json

from dotenv import load_dotenv
from google import genai


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# GEMINI API KEY
# =========================================================

api_key = os.getenv(
    "GEMINI_API_KEY"
)


# =========================================================
# GEMINI CLIENT
# =========================================================

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

    # =====================================================
    # CHECK API KEY
    # =====================================================

    if client is None:

        return {

            "success": False,

            "message":
                "Gemini API key is not configured."

        }


    # =====================================================
    # CONVERT KUNDLI TO JSON
    # =====================================================

    try:

        chart_json = json.dumps(
            kundli,
            indent=2,
            default=str
        )

    except Exception:

        chart_json = str(
            kundli
        )


    # =====================================================
    # AI PROMPT
    # =====================================================

    prompt = f"""
You are AI Jyotish, an assistant specializing
in traditional Indian/Vedic astrology.

Use the following calculated Kundli data
to answer the user's question.

KUNDLI DATA:

{chart_json}


USER QUESTION:

{user_question}


IMPORTANT RULES:

- Present astrology as a traditional or spiritual
  interpretation, not scientific certainty.
- Do not make medical, legal or financial guarantees.
- Do not frighten the user.
- Do not claim unavoidable death or disaster.
- Do not invent planetary positions that are not
  present in the supplied Kundli data.
- Explain important chart factors clearly.
- Keep the answer friendly and practical.
- If the available chart data is insufficient,
  clearly say so instead of inventing information.


ANSWER STRUCTURE:

1. Short answer
2. Astrological interpretation
3. Important chart factors
4. Practical guidance


Keep the answer easy to understand.

Answer the user's actual question directly.
"""


    # =====================================================
    # CALL GEMINI
    # =====================================================

    try:

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt

        )


        # =================================================
        # GET TEXT
        # =================================================

        answer = getattr(
            response,
            "text",
            None
        )


        if not answer:

            return {

                "success": False,

                "message":
                    "Gemini returned an empty response."

            }


        # =================================================
        # SUCCESS
        # =================================================

        return {

            "success": True,

            "answer":
                answer.strip()

        }


    # =====================================================
    # GEMINI ERROR
    # =====================================================

    except Exception as error:

        print("")
        print("=" * 70)
        print(
            "GEMINI API ERROR"
        )
        print("=" * 70)

        print(
            str(error)
        )

        print("=" * 70)


        return {

            "success": False,

            "message":
                str(error)

        }