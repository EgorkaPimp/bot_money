import callback.callback_button_register
import callback.callback_button_categories_exp
import callback.callback_button_finances_exp
import callback.callback_button_categoris_inc
import callback.callback_button_finances_inc
import callback.add_finance
from token_file import read_file
import asyncio
import logging
from aiogram import Bot, Dispatcher
from db.create_db import init_db

logging.basicConfig(level=logging.INFO)
my_token = read_file()

async def main():
    init_db()
    bot = Bot(token=my_token)
    dp = Dispatcher()

    from handlers import register_handlers
    callback.callback_button_register.register_callbacks(dp)
    callback.callback_button_categories_exp.cat_exp_callbacks(dp)
    callback.callback_button_finances_exp.fin_callbacks(dp)
    callback.callback_button_categoris_inc.cat_inc_callbacks(dp)
    callback.add_finance.add_fin_callbacks(dp)
    callback.callback_button_finances_inc.fin_callbacks_inc(dp)
    await register_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())