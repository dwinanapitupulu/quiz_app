import sqlite3

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    db.commit()


if __name__ == "__main__":
    init_db()
