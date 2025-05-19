# init_db.py
import sqlite3
from pathlib import Path

db_path = Path("database/stories.db")
db_path.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt TEXT,
    story TEXT,
    pdf_path TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()
print("✅ Veritabanı başarıyla oluşturuldu.")
