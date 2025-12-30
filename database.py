import sqlite3

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    currency TEXT,
    amount_sgd REAL,
    category TEXT,
    remark TEXT,
    date TEXT
)
""")

conn.commit()
conn.close()
