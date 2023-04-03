# Multiuser chating system backup server
# Backup Server can read messages from primary server and store them in backup database
# by Zhenrui

# import library
import sqlite3

class BackupServer:
    # create table for store information
    def __init__(self):
        self.create_table()

    def create_table(self):
        # define backup_messages.db for message history
        with sqlite3.connect('backup_messages.db') as conn:
            cursor=conn.cursor()
            # id as key stands for timestamp
            cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                message TEXT NOT NULL)''')
            conn.commit()

    def store_message(self, username, message):
        # store messages in the table
        with sqlite3.connect('backup_messages.db') as conn:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO messages (username, message) VALUES (?, ?)",
                           (username, message))
            conn.commit()

    def get_messages(self):
        # get all messages store in table so far
        with sqlite3.connect('backup_messages.db') as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM messages")
            rows=cursor.fetchall()
        return rows