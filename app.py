from flask import Flask, request, render_template_string
from openai import OpenAI
import os

client = OpenAI(api_key="DEIN_API_KEY_HIER")
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>KI TEST APP</title>
</head>
<body style="font-family: Arial; text-align:center; background:#111827; color:white; margin-top:60px;">
    <h1>KI TEST APP</h1>
    <p>Wenn du das siehst, ist der neue Code wirklich gespeichert.</p>

    <form method="POST">
        <input name="thema" placeholder="Frag etwas..." style="padding:10px; width:300px;">
        <button type="submit" style="padding:10px;">KI fragen</button>
    </form>

    {% if antwort %}
        <div style="margin:30px auto; width:70%; background:#1f2937; padding:20px; border-radius:10px;">
            <h2>Antwort</h2>
            <p>{{ antwort }}</p>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    antwort = None

    if request.method == "POST":
        thema = request.form["thema"]
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Erkläre Themen einfach für Schüler."},
                    {"role": "user", "content": thema},
                ],
            )
            antwort = response.choices[0].message.content
        except Exception as e:
            antwort = "FEHLER: " + str(e)

    return render_template_string(HTML, antwort=antwort)

if __name__ == "__main__":
    app.run(debug=True)
