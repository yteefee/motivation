from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

def get_admin_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [
        "📝 Добавить цитату",
        "📝 Добавить совет",
        "📊 Статистика",
        "🔙 На главную"
    ]
    for button in buttons:
        builder.button(text=button)
    builder.adjust(2, 2)
    return builder.as_markup(resize_keyboard=True)