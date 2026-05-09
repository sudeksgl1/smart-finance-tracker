import sqlite3

def connect():
    conn = sqlite3.connect("data.db")
    return conn

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount REAL,
        category TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_transaction(type, amount, category, date):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions (type, amount, category, date)
    VALUES (?, ?, ?, ?)
    """, (type, amount, category, date))

    conn.commit()
    conn.close()

    
def get_transactions():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()

    conn.close()
    return data

def delete_transaction(transaction_id):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))

    conn.commit()
    conn.close()

