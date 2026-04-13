import sqlite3
conn=sqlite3.connect("users.db")
cursor=conn.cursor()
cursor.execute("ALTER TABLE problems ADD COLUMN status TEXT DEFAULT 'NOt Solved'")
conn.commit()
conn.close()
print("column added!")

