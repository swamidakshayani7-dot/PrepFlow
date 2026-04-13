import sqlite3
conn=sqlite3.connect("users.db")
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS problems(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT
                   )
                   """)
conn.commit()
conn.close()
print("Problems table created!")

