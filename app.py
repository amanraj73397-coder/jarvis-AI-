from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import urllib.parse
import webbrowser

app = Flask(__name__)

app.secret_key = "jarvis-secret-key"

CORRECT_NAME = "Aman"
CORRECT_PASSWORD = "aman ji"


def jarvis_reply(message):

    cmd = message.lower().strip()

    # -------------------------
    # GREETING
    # -------------------------

    if any(word in cmd for word in [
        "hello",
        "hi",
        "hlo",
        "hii",
        "hey",
        "heyy",
        "helo",
        "namaste"
    ]):
        return "Hello! 👋 Main Jarvis hoon. Kaise help karun?"


    # -------------------------
    # TIME
    # -------------------------

    if (
        "time" in cmd
        or "samay" in cmd
        or "waqt" in cmd
        or "kya time hai" in cmd
        or "kitna time hua" in cmd
        or "time batao" in cmd
        or "abhi time" in cmd
        or "current time" in cmd
    ):
        current_time = datetime.now().strftime("%I:%M %p")

        return f"Abhi {current_time} baj rahe hain. ⏰"


    # -------------------------
    # DATE
    # -------------------------

    if (
        "date" in cmd
        or "tarikh" in cmd
        or "tareekh" in cmd
        or "aaj ki date" in cmd
        or "aaj ki tarikh" in cmd
        or "aaj kya date hai" in cmd
        or "aaj kaun si date hai" in cmd
        or "date batao" in cmd
    ):
        current_date = datetime.now().strftime("%d %B %Y")

        return f"Aaj {current_date} hai. 📅"


    # -------------------------
    # YOUTUBE
    # -------------------------

    if (
        "youtube" in cmd
        and (
            "open" in cmd
            or "khol" in cmd
            or "kholo" in cmd
            or "chalao" in cmd
        )
    ):
        webbrowser.open("https://www.youtube.com")

        return "Bilkul! YouTube khol diya. ▶️"


    # -------------------------
    # GOOGLE
    # -------------------------

    if (
        "google" in cmd
        and (
            "open" in cmd
            or "khol" in cmd
            or "kholo" in cmd
        )
    ):
        webbrowser.open("https://www.google.com")

        return "Bilkul! Google khol diya. 🔎"


    # -------------------------
    # SEARCH
    # -------------------------

    if cmd.startswith("search "):

        query = message[7:].strip()

        if query:

            url = (
                "https://www.google.com/search?q="
                + urllib.parse.quote(query)
            )

            webbrowser.open(url)

            return f"Maine Google par '{query}' search kar diya. 🔎"

        return "Bilkul, batao kya search karna hai?"


    # -------------------------
    # NORMAL CONVERSATION
    # -------------------------

    if "kaise ho" in cmd:
        return "Main bilkul badhiya hoon! 😄 Tum kaise ho?"


    if "tumhara naam" in cmd:
        return "Mera naam Jarvis hai. 🤖"


    if "kya kar sakte ho" in cmd:
        return (
            "Main time aur date bata sakta hoon, "
            "websites open kar sakta hoon aur basic "
            "baaton ka jawab de sakta hoon."
        )


    # -------------------------
    # UNKNOWN MESSAGE
    # -------------------------

    return (
        "Hmm, ye baat main abhi nahi samajh paya. "
        "Thoda alag tarike se batao."
    )


# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():

    if not session.get("logged_in"):
        return render_template("login.html")

    return render_template("index.html")


# -------------------------
# LOGIN
# -------------------------

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    name = data.get("name", "").strip()

    password = data.get("password", "")


    if (
        name.lower() == CORRECT_NAME.lower()
        and password == CORRECT_PASSWORD
    ):

        session["logged_in"] = True

        return jsonify({
            "success": True
        })


    return jsonify({
        "success": False,
        "message": "Wrong name or password. Access denied."
    })


# -------------------------
# CHAT
# -------------------------

@app.route("/chat", methods=["POST"])
def chat():

    if not session.get("logged_in"):

        return jsonify({
            "reply": "Access denied."
        }), 401


    data = request.get_json()

    message = data.get("message", "")

    reply = jarvis_reply(message)


    return jsonify({
        "reply": reply
    })


# -------------------------
# START SERVER
# -------------------------

if __name__ == "__main__":

    app.run(debug=True)
    