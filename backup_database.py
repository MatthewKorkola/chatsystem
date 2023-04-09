# Multiuser chating system backup database
# Backup databse store all messges from backup server
# by Zhenrui Zhang

import sqlite3

class BackupDatabase:
    def __init__(self):
        self.create_table()

    def create_table(self):
        # define out file name backup.db
        with sqlite3.connect('backup.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS message_history (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                message TEXT NOT NULL)''')
            conn.commit()

    # store all messages in the table
    def store_message(self, username, message):
        with sqlite3.connect('backup.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO message_history (username, message) VALUES (?, ?)", (username, message))
            conn.commit()

    # get all messages in the table so far
    def get_all_message_history(self):
        with sqlite3.connect('backup.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, message FROM message_history")
            rows = cursor.fetchall()
        return rows