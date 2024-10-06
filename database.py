import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        priority TEXT NOT NULL,
        responsible TEXT NOT NULL,
        due_date TEXT NOT NULL,
        status TEXT DEFAULT 'Pendente',
        completed_by TEXT,
        completed_at TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

create_database()
