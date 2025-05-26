import sqlite3

class Database:
    def __init__(self, db_path="peliculas.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        # Crear tablas si no existen
        pass

    def close(self):
        self.conn.close() 