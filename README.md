# AI Jyotish

AI-powered Vedic astrology web application.

## Technology

- Python
- Flask
- HTML
- CSS
- JavaScript
- Swiss Ephemeris
- Google Gemini
- Geopy

## Project Structure

AI-JYOTISH-APP/

backend/
    app.py
    ephemeris.py
    ai_astrologer.py
    requirements.txt
    .env

frontend/
    index.html
    style.css
    script.js

.gitignore
README.md


## Installation

Open a terminal inside the backend folder.

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install packages:

pip install -r requirements.txt


## API Key

Create:

backend/.env

Add:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE


## Run

Inside backend:

python app.py


Then open:

http://127.0.0.1:5000


## Important

The application is intended for educational and spiritual
exploration. Astrological interpretations should not be
treated as scientific predictions or professional advice.