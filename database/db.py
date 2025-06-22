import sqlite3
from pathlib import Path
from .models import create_tables

class Database:
    def __init__(self, db_name: str):
        self.db_path = Path(__file__).parent.parent / db_name
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        create_tables(self.cursor)
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()