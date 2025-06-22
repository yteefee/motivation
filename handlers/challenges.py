from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from config import config
from datetime import datetime, timedelta

router = Router()

@router.message(F.text == "🏆 Челленджи")
async def show_challenges_menu(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Мои челленджи", callback_data="my_challenges")],
        [InlineKeyboardButton(text="➕ Доступные челленджи", callback_data="available_challenges")]
    ])
    await message.answer("Выберите действие:", reply_markup=keyboard)

@router.callback_query(F.data == "available_challenges")
async def show_available_challenges(callback: CallbackQuery):
    with Database(config.DB_NAME) as db:
        db.cursor.execute("SELECT id, title, description FROM challenges")
        challenges = db.cursor.fetchall()
    
    if not challenges:
        await callback.message.answer("Нет доступных челленджей")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=title, callback_data=f"join_{id}")]
        for id, title, _ in challenges
    ])
    
    challenges_list = "\n".join(
        f"• {title} - {description}" 
        for _, title, description in challenges
    )
    
    await callback.message.edit_text(
        f"Доступные челленджи:\n\n{challenges_list}",
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("join_"))
async def join_challenge(callback: CallbackQuery):
    challenge_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id
    
    with Database(config.DB_NAME) as db:
        # Проверяем, не участвует ли уже
        db.cursor.execute('''
        SELECT 1 FROM user_challenges 
        WHERE user_id=? AND challenge_id=? AND completed=0
        ''', (user_id, challenge_id))
        
        if db.cursor.fetchone():
            await callback.answer("Вы уже участвуете в этом челлендже!")
            return
        
        # Добавляем челлендж
        db.cursor.execute('''
        INSERT INTO user_challenges (user_id, challenge_id, start_date)
        VALUES (?, ?, ?)
        ''', (user_id, challenge_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        db.conn.commit()
        
        # Получаем название
        db.cursor.execute('SELECT title FROM challenges WHERE id=?', (challenge_id,))
        title = db.cursor.fetchone()[0]
        
        await callback.message.edit_text(
            f"🎉 Вы начали челлендж: {title}!\n"
            "Следите за прогрессом в разделе 'Мои челленджи'"
        )

@router.callback_query(F.data == "my_challenges")
async def show_user_challenges(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    with Database(config.DB_NAME) as db:
        db.cursor.execute('''
        SELECT c.title, c.duration, uc.start_date 
        FROM user_challenges uc
        JOIN challenges c ON uc.challenge_id = c.id
        WHERE uc.user_id=? AND uc.completed=0
        ''', (user_id,))
        
        challenges = db.cursor.fetchall()
    
    if not challenges:
        await callback.message.edit_text("У вас нет активных челленджей")
        return
    
    response = "Ваши активные челленджи:\n\n"
    for title, duration, start_date in challenges:
        start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = start + timedelta(days=duration)
        days_left = (end_date - datetime.now()).days
        
        response += (
            f"🏅 {title}\n"
            f"⏳ Осталось дней: {max(0, days_left)}\n"
            f"📅 Завершение: {end_date.strftime('%d.%m.%Y')}\n\n"
        )
    
    await callback.message.edit_text(response)