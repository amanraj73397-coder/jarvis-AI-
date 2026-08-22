import os
import re
from openai import OpenAI


# -------------------------
# HINGLISH NORMALIZATION
# -------------------------

def normalize_message(message):
    text = message.lower().strip()

    replacements = {
        "hlo": "hello",
        "hlw": "hello",
        "helo": "hello",
        "helllo": "hello",
        "hii": "hi",
        "hyy": "hi",
        "heyy": "hey",

        "kr": "kar",
        "kro": "karo",
        "krna": "karna",
        "krni": "karni",
        "krta": "karta",
        "krti": "karti",
        "krte": "karte",

        "rha": "raha",
        "rhi": "rahi",
        "rhe": "rahe",

        "bta": "bata",
        "btao": "batao",
        "btana": "batana",

        "m": "main",
        "mai": "main",
        "me": "mein",

        "mujheko": "mujhe",
        "mereko": "mujhe",
        "mere ko": "mujhe",

        "ap": "aap",
        "apko": "aapko",
        "apne": "aapne",

        "acha": "accha",
        "achha": "accha",

        "kese": "kaise",
        "kaise": "kaise",

        "kon": "kaun",
        "koun": "kaun",

        "kya h": "kya hai",
        "kya kr": "kya kar",
    }

    for short, normal in replacements.items():
        text = re.sub(
            rf"\b{re.escape(short)}\b",
            normal,
            text
        )

    return text


# -------------------------
# MESSAGE UNDERSTANDING
# -------------------------

def understand_message(message):
    return {
        "original": message,
        "normalized": normalize_message(message)
    }


# -------------------------
# AI RESPONSE
# -------------------------

def ask_ai(message):

    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        return (
            "Mere AI brain ki API key abhi set nahi hai. "
            "Render mein OPENAI_API_KEY add karni hogi."
        )

    client = OpenAI(api_key=api_key)

    understood = understand_message(message)

    prompt = f"""
You are JARVIS, a friendly AI assistant.

The user normally talks in Hinglish, Roman Hindi,
short forms, spelling mistakes and casual chat.

Understand messages like:
"hlo" = hello
"kya kr rhe ho" = kya kar rahe ho
"tumhe kisne bnaya" = tumhe kisne banaya
"mereko btao" = mujhe batao
"kr skte ho" = kar sakte ho

Do NOT complain about spelling mistakes.
Understand the user's intended meaning from context.

Reply naturally in the same general language/style
the user is using.

Keep normal conversation friendly and easy to understand.
Do not pretend to have abilities you don't actually have.

User's original message:
{understood["original"]}

Normalized version:
{understood["normalized"]}
"""

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        answer = response.output_text.strip()

        if answer:
            return answer

        return "Mujhe abhi proper response nahi mila."

    except Exception as error:

        print("AI ERROR:", error)

        return (
            "AI se response lene mein problem aa gayi. "
            "Thodi der baad try karo."
        )
