import os

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "jarvis-development-secret"
)

DATABASE_PATH = os.environ.get(
    "DATABASE_PATH",
    "jarvis.db"
)

APP_NAME = "JARVIS AI"
