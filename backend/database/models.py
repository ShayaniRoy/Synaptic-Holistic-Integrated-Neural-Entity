import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")


# =========================
# CONNECTION
# =========================
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# INIT DATABASE
# =========================
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # CHAT HISTORY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        response TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# =========================
# USER FUNCTIONS
# =========================
def create_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()
        return True

    except sqlite3.IntegrityError:
        return False


def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()
    return user


# =========================
# CHAT FUNCTIONS
# =========================
def save_chat(username, message, response):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chats (username, message, response)
        VALUES (?, ?, ?)
    """, (username, message, response))

    conn.commit()
    conn.close()


def get_chat_history(username, limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM chats
        WHERE username = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (username, limit))

    chats = cursor.fetchall()
    conn.close()

    return chats[::-1]  # oldest → newest