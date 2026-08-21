import re


def normalize_message(message):
    text = message.lower().strip()

    replacements = {
        "hlo": "hello",
        "hlw": "hello",
        "helo": "hello",
        "hii": "hi",
        "heyy": "hey",
        "hyy": "hi",
        "kya kr": "kya kar",
        "kr": "kar",
        "kro": "karo",
        "rha": "raha",
        "rhi": "rahi",
        "btao": "batao",
        "bta": "bata",
        "mereko": "mujhe",
        "mere ko": "mujhe",
        "apko": "aapko",
        "apne": "aapne",
        "acha": "accha",
        "kese": "kaise",
        "kon": "kaun",
        "koun": "kaun",
    }

    for short, normal in replacements.items():
        text = re.sub(
            rf"\b{re.escape(short)}\b",
            normal,
            text
        )

    return text


def understand_message(message):
    original = message
    normalized = normalize_message(message)

    return {
        "original": original,
        "normalized": normalized
    }
