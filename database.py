import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "jarvis.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def create_user(email, password):
    email = email.strip().lower()

    password_hash = generate_password_hash(password)

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (?, ?)
            """,
            (email, password_hash)
        )

        connection.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        connection.close()


def verify_user(email, password):
    email = email.strip().lower()

    connection = get_connection()

    user = connection.execute(
        """
        SELECT * FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    if user and check_password_hash(
        user["password_hash"],
        password
    ):
        return True

    return False
