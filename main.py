import logging
from aiogram import Bot, Dispatcher
from config import config
from handlers import common_router, admin_router, challenges_router, mood_router



async def main():
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=config.BOT_TOKEN, default=config.bot_properties)
    dp = Dispatcher()
    
    dp.include_router(common_router)
    dp.include_router(admin_router)
    dp.include_router(challenges_router)
    dp.include_router(mood_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())