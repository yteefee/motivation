from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

class Config:
    BOT_TOKEN = "7869438826:AAGaLosBwVXxQ83Ywydht4vrMc3NBFui3eQ"
    ADMIN_ID = 5533141496
    DB_NAME = "database\motivator.db"
    
    bot_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)

config = Config()