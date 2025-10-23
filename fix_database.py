import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN nickname TEXT UNIQUE")
    conn.commit()
    print("✅ Kolom nickname berhasil ditambahkan!")
except Exception as e:
    print("ℹ️ Kolom nickname mungkin sudah ada atau error lain:", e)

conn.close()