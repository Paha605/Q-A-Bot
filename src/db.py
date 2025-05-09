import asyncio
import sqlite3
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Database:
    def __init__(self, db_file=None):
        if db_file is None:
            db_dir = r"C:\Users\Pavel\OneDrive\Рабочий стол\Algoritms\Algoritms 1.0\Q&A\.venv\Lib"
            os.makedirs(db_dir, exist_ok=True)
            self.db_file = os.path.join(db_dir, "questions.db")
        else:
            self.db_file = db_file

        self.create_table()

    def create_connection(self):
        return sqlite3.connect(self.db_file)

    def create_table(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    question TEXT
                )
            """)

        conn.commit()
        conn.close()

    def add_question(self, date, question):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO questions (date, question)
            VALUES (?, ?)
        """, (date, question))
        conn.commit()
        conn.close()

    def get_question(self, date):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE date = ?", (date,))
        user = cursor.fetchone()
        conn.close()
        return user

    def get_all_question(self):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT question FROM questions')
        users = cursor.fetchall()
        conn.close()
        return [user[0] for user in users]

    def clear_db(self):
        conn = self.create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table_name in tables:
            # Удаляем все записи из каждой таблицы
            cursor.execute(f"DELETE FROM {table_name[0]};")

        conn.commit()
        conn.close()
        print("Database cleared..")

    async def clear_time(self):
        # Создание планировщика
        scheduler = AsyncIOScheduler()

        # Добавление задания, которое выполняется каждые 90 дней
        scheduler.add_job(self.clear_db, trigger='interval', days=21)

        # Запуск планировщика
        scheduler.start()