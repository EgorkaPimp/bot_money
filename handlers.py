import logging
import time
from email.message import Message

from aiogram import types
from aiogram.filters import Command

import db.database



async def register_handlers(dp):
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(cmd_help, Command('help'))

async def cmd_help(message: types.Message):
    user = message
    print(user)
    print(message.from_user.id)
    await message.answer('Types message!')

async def  cmd_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    start_data = (message.date.date()).strftime("%D")
    time_register = (message.date.time()).strftime("%H:%M:%S")
    await message.answer(f'Hello! {user_name} {user_last_name}')
    await db.database.add_user(user_id, 'God', user_name,
                               user_last_name, start_data, time_register)

