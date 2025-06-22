from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards import get_admin_keyboard
from utils.states import AdminStates  # Измененный импорт
from database.db import Database
from config import config

router = Router()

@router.message(F.text == "👨‍💻 Админ-панель")
async def admin_panel(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        await message.answer("У вас нет доступа к этой команде")
        return
        
    await message.answer(
        "Вы вошли в админ-панель. Выберите действие:",
        reply_markup=get_admin_keyboard()
    )

@router.message(F.text == "📊 Статистика")
async def show_stats(message: Message):
    if message.from_user.id != config.ADMIN_ID:
        return
        
    with Database(config.DB_NAME) as db:
        # Статистика пользователей
        db.cursor.execute("SELECT COUNT(*) FROM users")
        users_count = db.cursor.fetchone()[0]
        
        # Статистика цитат
        db.cursor.execute("SELECT COUNT(*) FROM quotes")
        quotes_count = db.cursor.fetchone()[0]
        
        # Статистика советов
        db.cursor.execute("SELECT COUNT(*) FROM tips")
        tips_count = db.cursor.fetchone()[0]
        
        # Статистика челленджей
        db.cursor.execute("SELECT COUNT(*) FROM challenges")
        challenges_count = db.cursor.fetchone()[0]
        
        db.cursor.execute("""
            SELECT COUNT(*) FROM user_challenges WHERE completed=1
        """)
        completed_challenges = db.cursor.fetchone()[0]
    
    stats_message = (
        "📊 Статистика бота:\n\n"
        f"👤 Пользователей: {users_count}\n"
        f"💬 Цитат: {quotes_count}\n"
        f"💡 Советов: {tips_count}\n"
        f"🏆 Челленджей: {challenges_count}\n"
        f"✅ Завершенных челленджей: {completed_challenges}"
    )
    
    await message.answer(stats_message)

@router.message(F.text == "📝 Добавить цитату")
async def add_quote_start(message: Message, state: FSMContext):
    if message.from_user.id != config.ADMIN_ID:
        return
        
    await message.answer("Введите цитату:")
    await state.set_state(AdminStates.add_quote)

@router.message(AdminStates.add_quote)
async def add_quote_finish(message: Message, state: FSMContext):
    with Database(config.DB_NAME) as db:
        db.cursor.execute(
            "INSERT INTO quotes (quote_text) VALUES (?)",
            (message.text,)
        )
        db.conn.commit()
    
    await message.answer("Цитата успешно добавлена!")
    await state.clear()

@router.message(F.text == "📝 Добавить совет")
async def add_tip_start(message: Message, state: FSMContext):
    if message.from_user.id != config.ADMIN_ID:
        return
        
    await message.answer("Введите совет:")
    await state.set_state(AdminStates.add_tip)

@router.message(AdminStates.add_tip)
async def add_tip_finish(message: Message, state: FSMContext):
    with Database(config.DB_NAME) as db:
        db.cursor.execute(
            "INSERT INTO tips (tip_text) VALUES (?)",
            (message.text,)
        )
        db.conn.commit()
    
    await message.answer("Совет успешно добавлен!")
    await state.clear()

@router.message(F.text == "🔙 На главную")
async def back_to_main(message: Message):
    from keyboards.user import get_main_keyboard
    await message.answer(
        "Возвращаюсь в главное меню",
        reply_markup=get_main_keyboard()
    )