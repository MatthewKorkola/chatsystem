import sqlite3

class BackupDatabase:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with sqlite3.connect('backup.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                message TEXT NOT NULL)''')
            conn.commit()

    def store_message(self, username, message):
        with sqlite3.connect('backup.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (username, message) VALUES (?, ?)",
                           (username, message))
            conn.commit()

    def get_messages(self, username):
        with sqlite3.connect('backup.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT message FROM messages WHERE username = ?", (username,))
            rows = cursor.fetchall()
        return rows

    def get_all_messages(self):
        with sqlite3.connect('backup.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, message FROM messages ORDER BY username, id")
            rows = cursor.fetchall()
        return rows
