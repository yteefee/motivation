def create_tables(cursor):
    # Создаём таблицу цитат
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote_text TEXT NOT NULL,
        author TEXT,
        category TEXT
    )''')
    
    # Создаём таблицу советов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tip_text TEXT NOT NULL,
        category TEXT
    )''')
    
    # Создаём таблицу челленджей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        duration INTEGER
    )''')
    
    # Создаём таблицу пользовательских челленджей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        challenge_id INTEGER,
        start_date TEXT,
        completed INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (challenge_id) REFERENCES challenges (id)
    )''')