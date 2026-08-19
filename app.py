from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import urllib.parse
import os

app = Flask(__name__)

# Secret key को Render Environment Variable में रखना बेहतर है
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

CORRECT_NAME = os.environ.get("JARVIS_NAME", "Aman")
CORRECT_PASSWORD = os.environ.get("JARVIS_PASSWORD", "aman ji")


def normalize(text):
    """Common typing mistakes और Hinglish को थोड़ा normalize करता है."""
    text = text.lower().strip()

    replacements = {
        "hlw": "hello",
        "hlo": "hello",
        "helo": "hello",
        "hii": "hi",
        "heyy": "hey",
        "hy": "hi",
        "hyy": "hi",
        "gm": "good morning",
        "gn": "good night",
        "thx": "thanks",
        "tnx": "thanks",
        "pls": "please",
        "plz": "please",
        "kese": "kaise",
        "kaise": "kaise",
        "kon": "kaun",
        "koun": "kaun",
        "kr": "kar",
        "kro": "karo",
        "btao": "batao",
        "btana": "batana",
        "acha": "accha",
        "accha": "accha",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def jarvis_reply(message):
    cmd = normalize(message)

    if not cmd:
        return "Haan, bolo. Main sun raha hoon. 🙂"

    # -------------------------
    # GREETINGS
    # -------------------------

    greetings = [
        "hello",
        "hi",
        "hey",
        "namaste",
        "good morning",
        "good afternoon",
        "good evening",
        "good night",
    ]

    if cmd in greetings or any(cmd.startswith(g + " ") for g in greetings):
        if "good morning" in cmd:
            return "Good morning! ☀️ Main Jarvis hoon. Kaise help karun?"
        if "good afternoon" in cmd:
            return "Good afternoon! 😄 Main Jarvis hoon. Bolo kya karna hai?"
        if "good evening" in cmd:
            return "Good evening! 🌆 Bolo, main kya help karun?"
        if "good night" in cmd:
            return "Good night! 🌙 Achhi neend lena."
        return "Hello! 👋 Main Jarvis hoon. Kaise help karun?"

    # -------------------------
    # HOW ARE YOU
    # -------------------------

    if any(x in cmd for x in [
        "kaise ho",
        "kese ho",
        "how are you",
        "kya haal hai",
        "haal kya hai",
        "sab theek hai"
    ]):
        return "Main bilkul badhiya hoon! 😄 Tum batao, kaise ho?"

    # -------------------------
    # NAME / IDENTITY
    # -------------------------

    if any(x in cmd for x in [
        "tumhara naam",
        "tumhara name",
        "what is your name",
        "who are you",
        "tum kon ho",
        "tum kaun ho"
    ]):
        return "Mera naam JARVIS hai. 🤖"

    if any(x in cmd for x in [
        "kisne banaya",
        "tumhe kisne banaya",
        "who made you",
        "who created you"
    ]):
        return "Mujhe Aman ne banaya hai. 🚀"

    # -------------------------
    # THANKS
    # -------------------------

    if any(x in cmd for x in [
        "thanks",
        "thank you",
        "thankyou",
        "shukriya",
        "dhanyawad"
    ]):
        return "You're welcome! 😄 Aur kuch chahiye?"

    # -------------------------
    # BYE
    # -------------------------

    if cmd in [
        "bye",
        "goodbye",
        "good bye",
        "see you",
        "see ya",
        "tata"
    ]:
        return "Bye! 👋 Phir milte hain."

    # -------------------------
    # TIME
    # -------------------------

    if any(x in cmd for x in [
        "time",
        "samay",
        "waqt",
        "kitna time",
        "kya time hai",
        "time batao",
        "abhi time"
    ]):
        current_time = datetime.now().strftime("%I:%M %p")
        return f"Abhi {current_time} baj rahe hain. ⏰"

    # -------------------------
    # DATE
    # -------------------------

    if any(x in cmd for x in [
        "date",
        "tarikh",
        "tareekh",
        "aaj ki date",
        "aaj ki tarikh",
        "aaj kya date hai",
        "date batao"
    ]):
        current_date = datetime.now().strftime("%d %B %Y")
        return f"Aaj {current_date} hai. 📅"

    # -------------------------
    # CAPABILITIES
    # -------------------------

    if any(x in cmd for x in [
        "kya kar sakte ho",
        "what can you do",
        "tum kya kar sakte ho",
        "tumhare features",
        "help"
    ]):
        return (
            "Main greetings aur normal baatein samajh sakta hoon, "
            "time/date bata sakta hoon, Google search ke liye help kar sakta hoon, "
            "aur kai common commands handle kar sakta hoon. 🤖"
        )

    # -------------------------
    # GOOGLE
    # -------------------------

    if (
        "google" in cmd
        and any(x in cmd for x in ["open", "khol", "kholo"])
    ):
        return "Google kholne ke liye yahan click karo: https://www.google.com"

    # -------------------------
    # YOUTUBE
    # -------------------------

    if (
        "youtube" in cmd
        and any(x in cmd for x in ["open", "khol", "kholo", "chalao"])
    ):
        return "YouTube kholne ke liye yahan click karo: https://www.youtube.com"

    # -------------------------
    # SEARCH
    # -------------------------

    search_words = [
        "search ",
        "google par ",
        "google pe ",
        "search karo ",
        "dhundo ",
        "dhoondo "
    ]

    for word in search_words:
        if cmd.startswith(word):
            query = message[len(word):].strip()

            if query:
                url = (
                    "https://www.google.com/search?q="
                    + urllib.parse.quote(query)
                )

                return f"Ye search karo: {url}"

    # -------------------------
    # SIMPLE COMMON QUESTIONS
    # -------------------------

    if any(x in cmd for x in [
        "bore ho raha",
        "boring",
        "bore ho rha"
    ]):
        return "Bore ho rahe ho? 😄 Mujhse baat karo ya koi interesting topic try karte hain."

    if any(x in cmd for x in [
        "mujhe help chahiye",
        "help chahiye",
        "meri help karo",
        "can you help me"
    ]):
        return "Bilkul! 😄 Batao kis cheez mein help chahiye?"

    if any(x in cmd for x in [
        "good job",
        "nice",
        "awesome",
        "great"
    ]):
        return "Thank you! 😄"

    if any(x in cmd for x in [
        "tum smart ho",
        "you are smart",
        "smart ho"
    ]):
        return "Thank you! 😄 Main aur smart banne ki koshish kar raha hoon."

    # -------------------------
    # CALCULATOR - BASIC
    # -------------------------

    if cmd.startswith("calculate "):
        expression = cmd.replace("calculate ", "", 1).strip()

        allowed = "0123456789+-*/().% "

        if expression and all(char in allowed for char in expression):
            try:
                result = eval(expression, {"__builtins__": {}}, {})
                return f"Answer: {result} 🧮"
            except Exception:
                return "Calculation samajh nahi aaya. Example: calculate 25 + 15"

        return "Calculation mein sirf numbers aur + - * / use karo."

    # -------------------------
    # DEFAULT
    # -------------------------

    return (
        "Hmm 🤔 main abhi us baat ka exact answer nahi jaanta. "
        "Tum thoda simple ya doosre words mein pooch sakte ho."
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
# LOGIN
# -------------------------

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

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

    data = request.get_json() or {}
    message = data.get("message", "").strip()

    return jsonify({
        "reply": jarvis_reply(message)
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


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
