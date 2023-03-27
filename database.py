# Multiuser chating system database
# Define functions for account information 
# by Zhenrui

# import library
import sqlite3

class Database:
    # create table for store information
    def __init__(self):
        self.create_table()

    def create_table(self):
        # define out file name user.db
        with sqlite3.connect('users.db') as conn:
            cursor=conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY NOT NULL,
                                password TEXT NOT NULL)''')
            conn.commit()

    def add_user(self, username, password):
        try:
            with sqlite3.connect('users.db') as conn:
                cursor=conn.cursor()
                # add new information in table
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                               (username, password))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def remove_user(self, username):
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            # delete user information
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()

    def check_password(self, username, password):
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            # get password for sepecific user account
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            row=cursor.fetchone()
        if row:
            # if match
            return row[0] == password
        return False

    def show_db(self):
        with sqlite3.connect('users.db') as conn:
            cursor=conn.cursor()
            # show database table content
            cursor.execute("SELECT * FROM users")
            rows=cursor.fetchall()
        return rows
