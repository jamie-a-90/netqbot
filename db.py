import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user text, userid text, qlimit text, shift text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    def insert(self, user, userid, qlimit, shift):
        self.cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?)",
                         (user, userid, qlimit, shift))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM users WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, user, userid, qlimit, shift):
        self.cur.execute("UPDATE users SET user = ?, userid = ?, qlimit = ?, shift = ? WHERE id = ?",
                         (user, userid, qlimit, shift, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

