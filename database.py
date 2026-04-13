import sqlite3
def create_table():
    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
        
    )
    """)
    conn.commit()
    conn.close()
create_table()