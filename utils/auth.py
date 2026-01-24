import sqlite3

def validate_user(username, password):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    result = cur.fetchone()
    conn.close()
    return result
