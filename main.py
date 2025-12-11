# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import settings
from database.engine import init_db
from bot.handlers import start, quiz


logging.basicConfig(level=logging.INFO)


async def main():
    await init_db()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(quiz.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
