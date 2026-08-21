import urllib.parse


def google_search(query):
    query = query.strip()

    if not query:
        return None

    return (
        "https://www.google.com/search?q="
        + urllib.parse.quote(query)
    )


def youtube_url():
    return "https://www.youtube.com"


def google_url():
    return "https://www.google.com"


def calculator(expression):
    allowed = "0123456789+-*/().% "

    if not expression:
        return "Invalid calculation."

    if not all(char in allowed for char in expression):
        return "Calculation mein sirf numbers aur + - * / use karo."

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )
        return str(result)

    except Exception:
        return "Calculation samajh nahi aaya."
