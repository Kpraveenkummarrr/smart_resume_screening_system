import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
  username TEXT,
  password TEXT
)
""")

cur.execute("INSERT INTO users VALUES (?,?)", ("admin","admin"))

conn.commit()
conn.close()

print("✅ Database & user created")
