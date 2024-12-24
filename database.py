import sqlite3
import hashlib

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.create_user_table()

    def create_user_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password):
        hashed_password = self.hash_password(password)
        try:
            self.conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                            (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        hashed_password = self.hash_password(password)
        cursor = self.conn.execute("SELECT * FROM users WHERE username=? AND password=?", 
                                 (username, hashed_password))
        return cursor.fetchone() is not None

    def __del__(self):
        self.conn.close()
