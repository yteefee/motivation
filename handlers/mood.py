from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.user import get_mood_keyboard, get_main_keyboard
from utils.states import MoodStates

router = Router()  # Это ключевая строка, которую нужно добавить

@router.message(F.text == "😊 Трекер настроения")
async def mood_tracker_start(message: Message):
    await message.answer("Как твое настроение сегодня?", reply_markup=get_mood_keyboard())

@router.message(F.text.in_(["😊 Хорошее", "😐 Нормальное", "😕 Плохое"]))
async def save_mood(message: Message):
    mood_map = {
        "😊 Хорошее": 2,
        "😐 Нормальное": 1,
        "😕 Плохое": 0
    }
    
    mood_value = mood_map[message.text]
    response = f"Спасибо! Твое настроение ({message.text}) сохранено."
    await message.answer(response, reply_markup=get_main_keyboard())

__all__ = ['router']  # Не забудьте добавить экспорт