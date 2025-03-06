import sqlite3

def init_db():
    conn=sqlite3.connect("crowd_data.db")
    cursor=conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS crowd (id INTEGER PRIMARY KEY AUTOINCREMENT,gate TEXT NOT NULL,count INTEGER NOT NULL,timestamp TEXT NOT NULL)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
