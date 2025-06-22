from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [
        "🎯 Получить цитату",
        "💡 Случайный совет",
        "🏆 Челленджи",
        "😊 Трекер настроения"
    ]
    for button in buttons:
        builder.button(text=button)
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)

def get_challenges_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [
        "📋 Активные челленджи",
        "➕ Начать новый челлендж",
        "🔙 Назад"
    ]
    for button in buttons:
        builder.button(text=button)
    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True)

def get_mood_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [
        "😊 Хорошее",
        "😐 Нормальное", 
        "😕 Плохое",
        "🔙 Назад"
    ]
    for button in buttons:
        builder.button(text=button)
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)

__all__ = ['get_main_keyboard', 'get_challenges_keyboard', 'get_mood_keyboard']