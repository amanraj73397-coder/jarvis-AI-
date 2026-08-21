from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import os

from database import init_database
from auth import signup_user, login_user
from ai import normalize_message
from tools import google_search, youtube_url, google_url, calculator


app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "jarvis-development-secret"
)

# Database तैयार करो
init_database()


def jarvis_reply(message):
    original = message.strip()
    cmd = normalize_message(original)

    if not cmd:
        return "Haan, bolo. Main sun raha hoon. 🙂"

    # Greetings
    if cmd in ["hello", "hi", "hey", "namaste"]:
        return "Hello! 👋 Main JARVIS hoon. Kaise help karun?"

    # Casual conversation
    if any(x in cmd for x in [
        "kaise ho",
        "how are you",
        "kya haal hai",
        "sab theek hai"
    ]):
        return "Main bilkul badhiya hoon! 😄 Tum kaise ho?"

    if any(x in cmd for x in [
        "tumhara naam",
        "tumhara name",
        "who are you",
        "tum kaun ho"
    ]):
        return "Mera naam JARVIS hai. 🤖"

    if any(x in cmd for x in [
        "thanks",
        "thank you",
        "shukriya"
    ]):
        return "You're welcome! 😄"

    if cmd in ["bye", "goodbye", "good bye"]:
        return "Bye! 👋 Phir milte hain."

    # Time
    if any(x in cmd for x in [
        "time",
        "samay",
        "waqt",
        "kitna time",
        "kya time hai",
        "time batao"
    ]):
        current_time = datetime.now().strftime("%I:%M %p")
        return f"Abhi {current_time} baj rahe hain. ⏰"

    # Date
    if any(x in cmd for x in [
        "date",
        "tarikh",
        "tareekh",
        "aaj ki date",
        "aaj ki tarikh"
    ]):
        current_date = datetime.now().strftime("%d %B %Y")
        return f"Aaj {current_date} hai. 📅"

    # YouTube
    if (
        "youtube" in cmd
        and any(x in cmd for x in ["open", "khol", "kholo"])
    ):
        return {
            "type": "link",
            "text": "YouTube kholo ▶️",
            "url": youtube_url()
        }

    # Google
    if (
        "google" in cmd
        and any(x in cmd for x in ["open", "khol", "kholo"])
    ):
        return {
            "type": "link",
            "text": "Google kholo 🔎",
            "url": google_url()
        }

    # Search
    search_prefixes = [
        "search ",
        "search karo ",
        "google par ",
        "google pe ",
        "dhundo ",
        "dhoondo "
    ]

    for prefix in search_prefixes:
        if cmd.startswith(prefix):
            query = original[len(prefix):].strip()

            if query:
                return {
                    "type": "link",
                    "text": f"'{query}' search karo 🔎",
                    "url": google_search(query)
                }

    # Calculator
    if cmd.startswith("calculate "):
        expression = cmd[len("calculate "):].strip()
        result = calculator(expression)

        return f"Answer: {result} 🧮"

    # Capabilities
    if any(x in cmd for x in [
        "kya kar sakte ho",
        "what can you do",
        "help"
    ]):
        return (
            "Main normal conversation, Hinglish commands, "
            "time/date, Google search, YouTube, Google aur "
            "basic calculations handle kar sakta hoon. 🤖"
        )

    return (
        "Hmm 🤔 main abhi is baat ka exact answer nahi jaanta. "
        "Thoda doosre words mein pooch kar dekho."
    )


# -------------------------
# HOME
# -------------------------

@app.route("/")
def home():

    if not session.get("logged_in"):
        return render_template("login.html")

    return render_template("index.html")


# -------------------------
# SIGNUP
# -------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")

    data = request.get_json() or {}

    email = data.get("email", "").strip()
    password = data.get("password", "")

    success, message = signup_user(email, password)

    return jsonify({
        "success": success,
        "message": message
    })


# -------------------------
# LOGIN
# -------------------------

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json() or {}

    email = data.get("email", "").strip()
    password = data.get("password", "")

    success, message = login_user(email, password)

    if success:
        session["logged_in"] = True
        session["email"] = email

    return jsonify({
        "success": success,
        "message": message
    })


# -------------------------
# CHAT
# -------------------------

@app.route("/chat", methods=["POST"])
def chat():

    if not session.get("logged_in"):
        return jsonify({
            "reply": "Please login first."
        }), 401

    data = request.get_json() or {}

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "reply": "Kuch message likho. 🙂"
        })

    reply = jarvis_reply(message)

    return jsonify({
        "reply": reply
    })


# -------------------------
# LOGOUT
# -------------------------

@app.route("/logout")
def logout():

    session.clear()

    return jsonify({
        "success": True
    })


# -------------------------
# START SERVER
# -------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
