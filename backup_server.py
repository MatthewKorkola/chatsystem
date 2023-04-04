# Multiuser chating system backup server
# Backup Server can read messages from primary server and store them in backup database
# by Zhenrui

# import library
from queue import Queue
import sqlite3

class BackupServer:
    def __init__(self):
        self.create_table()  # Create the table for storing messages
        self.message_queue = Queue()  # New: Initialize a message queue for storing new messages

    def create_table(self):
        # Create the SQLite database table if it doesn't exist
        with sqlite3.connect('backup_messages.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                message TEXT NOT NULL)''')
            conn.commit()

    def store_message(self, username, message):
        # Store the message in the SQLite database
        with sqlite3.connect('backup_messages.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (username, message) VALUES (?, ?)",
                           (username, message))
            conn.commit()

        # New: Store the message in the message queue for broadcasting
        self.message_queue.put((username, message))

    def get_messages(self):
        # Retrieve all messages stored in the SQLite database
        with sqlite3.connect('backup_messages.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM messages")
            rows = cursor.fetchall()
        return rows

    def get_new_messages(self):
        # New: Retrieve new messages from the message queue and return them as a list
        new_messages = []
        while not self.message_queue.empty():
            new_messages.append(self.message_queue.get())
        return new_messages
