import sqlite3

class DatabaseManager:
    def __init__(self, db_path="espacio_creativo.db"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def execute(self, query, params=(), commit=False):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query, params)
        if commit:
            conn.commit()
        return cur