import sqlite3
from pathlib import Path
import sys
import os

# Добавляем корень проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config import config

def init_database():
    # Указываем путь к базе данных в корне проекта
    db_path = project_root / config.DB_NAME
    print(f"Создаю БД по пути: {db_path}")
    
    try:
        
        # Создаем подключение к базе
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Создаем таблицы
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_text TEXT NOT NULL,
            author TEXT
        );
                             
        
        CREATE TABLE IF NOT EXISTS tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tip_text TEXT NOT NULL,
            category TEXT
        );
                             
        CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        registration_date TEXT DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            duration INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS user_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            challenge_id INTEGER,
            start_date TEXT,
            completed INTEGER DEFAULT 0
        );
        ''')
        
        # Очищаем таблицы перед добавлением данных
        cursor.execute("DELETE FROM quotes")
        cursor.execute("DELETE FROM tips")
        cursor.execute("DELETE FROM challenges")
        
        # Добавляем тестовые цитаты
        quotes = [
            ("Дорогу осилит идущий", "Лао-Цзы"),
            ("Успех — это способность идти от неудачи к неудаче", "Уинстон Черчилль"),
            ("Не откладывай на завтра то, что можно сделать сегодня", "Бенджамин Франклин")
        ]
        cursor.executemany(
            'INSERT INTO quotes (quote_text, author) VALUES (?, ?)',
            quotes
        )
        
        # Добавляем тестовые советы
        tips = [
            ("Начинайте день с самого важного задания", "продуктивность"),
            ("Делайте перерывы каждые 45 минут работы", "здоровье"),
            ("Пейте воду в течение дня", "здоровье"),
            ("Записывайте свои цели", "мотивация"),
            ("Практикуйте благодарность каждый день", "психология")
        ]
        cursor.executemany(
            'INSERT INTO tips (tip_text, category) VALUES (?, ?)',
            tips
        )
        
        # Добавляем тестовые челленджи
        challenges = [
            ("30 дней спорта", "Ежедневная тренировка 20 минут", 30),
            ("21 день чтения", "Читать 30 страниц в день", 21),
            ("7 дней воды", "Пить 2 литра воды ежедневно", 7),
            ("14 дней раннего подъема", "Просыпаться в 6 утра", 14),
            ("5 дней без соцсетей", "Не заходить в соцсети с 9 до 18", 5)
        ]
        cursor.executemany(
            'INSERT INTO challenges (title, description, duration) VALUES (?, ?, ?)',
            challenges
        )
        
        conn.commit()
        print("✅ База успешно инициализирована!")
        print(f"- Добавлено цитат: {len(quotes)}")
        print(f"- Добавлено советов: {len(tips)}")
        print(f"- Добавлено челленджей: {len(challenges)}")
        print(f"Размер файла БД: {os.path.getsize(db_path)} байт")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_database()