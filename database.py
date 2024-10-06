import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')  # Nome do arquivo do banco de dados
    cursor = conn.cursor()

    # Criar tabela tasks
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            responsible TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Banco de dados criado com sucesso.")
