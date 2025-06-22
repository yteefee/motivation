from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.user import get_main_keyboard
from database.db import Database
from config import config
from datetime import datetime
import random
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.user import get_main_keyboard
from config import config

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    with Database(config.DB_NAME) as db:
        db.cursor.execute(
            'INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)',
            (message.from_user.id, message.from_user.username, message.from_user.first_name)
        )
        db.conn.commit()
    
    keyboard = get_main_keyboard()
    if message.from_user.id == config.ADMIN_ID:
        keyboard.keyboard.append(["👨‍💻 Админ-панель"])
    
    await message.answer(
        f"Привет, {message.from_user.first_name}!",
        reply_markup=keyboard
    )


@router.message(Command("start"))
async def cmd_start(message: Message):
    try:
        with Database(config.DB_NAME) as db:
            db.cursor.execute(
                'INSERT OR IGNORE INTO users (user_id, username, first_name, registration_date) VALUES (?, ?, ?, ?)',
                (
                    message.from_user.id,
                    message.from_user.username,
                    message.from_user.first_name,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
            )
            db.conn.commit()
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    
    # Создаем клавиатуру
    keyboard = get_main_keyboard()
    
    # Если пользователь - админ, добавляем кнопку админки
    if message.from_user.id == config.ADMIN_ID:
        keyboard.keyboard.append(["👨‍💻 Админ-панель"])
    
    await message.answer(
        f"Привет, {message.from_user.first_name}!",
        reply_markup=keyboard
    )

# Обработчик кнопки "Назад"
@router.message(F.text == "🔙 Назад")
async def back_to_main(message: Message):
    await message.answer(
        "Возвращаюсь в главное меню",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "🎯 Получить цитату")
async def send_quote(message: Message):
    try:
        with Database(config.DB_NAME) as db:
            print("Пытаюсь получить цитату из базы...")  # Логирование
            db.cursor.execute('SELECT quote_text, author FROM quotes')
            all_quotes = db.cursor.fetchall()
            print(f"Найдено цитат: {len(all_quotes)}")  # Логирование
            
            if not all_quotes:
                await message.answer("База цитат пуста")
                return
                
            quote = random.choice(all_quotes)
            response = f'"{quote[0]}"'
            if quote[1]:
                response += f'\n— {quote[1]}'
                
            await message.answer(response)
            
    except Exception as e:
        print(f"Ошибка при получении цитаты: {e}")  # Логирование
        await message.answer("Ошибка при получении цитаты")

@router.message(F.text == "💡 Случайный совет")
async def send_tip(message: Message):
    try:
        with Database(config.DB_NAME) as db:
            db.cursor.execute('''
                SELECT tip_text, category FROM tips 
                ORDER BY RANDOM() LIMIT 1
            ''')
            tip = db.cursor.fetchone()
            
            if not tip:
                await message.answer("Советы пока не добавлены. Попробуйте позже.")
                return
                
            response = tip[0]
            if tip[1]:
                response += f"\n\n🔹 Категория: {tip[1]}"
                
            await message.answer(response)
            
    except Exception as e:
        await message.answer("Ошибка при получении совета")
        print(f"Ошибка в send_tip: {e}")