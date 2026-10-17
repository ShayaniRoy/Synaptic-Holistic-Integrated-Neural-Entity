import sqlite3

DB_NAME = "users.db"

# ----------------------
# INIT DATABASE
# ----------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # User Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # History Table (Added)
    # Stores the prompt, the AI response, and timestamps
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        user_msg TEXT,
        ai_reply TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(username) REFERENCES users(username)
    )
    """)

    conn.commit()
    conn.close()


# ----------------------
# CREATE USER
# ----------------------
def create_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# ----------------------
# GET USER
# ----------------------
def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cur.fetchone()
    conn.close()

    return user

# ----------------------
# HISTORY LOGIC (NEW)
# ----------------------

def save_chat(username, user_msg, ai_reply):
    """Saves a single interaction to the history table"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO history (username, user_msg, ai_reply) VALUES (?, ?, ?)",
            (username, user_msg, ai_reply)
        )
        conn.commit()
    except Exception as e:
        print(f"Error saving history: {e}")
    finally:
        conn.close()

def get_history(username):
    """Retrieves all past messages for a specific user"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # We select user_msg and ai_reply to display in the dashboard
    cur.execute(
        "SELECT user_msg, ai_reply FROM history WHERE username = ? ORDER BY timestamp ASC",
        (username,)
    )
    
    rows = cur.fetchall()
    conn.close()
    return rows