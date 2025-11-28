import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS secrets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    flag TEXT NOT NULL
                )''')

    # Insert dummy data
    data = [
        ('Project Alpha', 'Top secret project regarding AI', 'FLAG{fake_flag_1}'),
        ('Operation Neon', 'Cybersecurity initiative', 'FLAG{fake_flag_2}'),
        ('The Archive', 'Old records from 1990', 'FLAG{fake_flag_3}'),
        ('Super Secret', 'Do not look here', 'flag{n1c3_SQL_qu3rying_capabilities}'),
    ]

    c.executemany('INSERT INTO secrets (name, description, flag) VALUES (?, ?, ?)', data)

    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == '__main__':
    init_db()
