from token_file import read_file
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
my_token = read_file()

async def main():
    bot = Bot(token=my_token)
    dp = Dispatcher()

    from callback_button import register_callbacks
    from handlers import register_handlers
    register_callbacks(dp)
    await register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())