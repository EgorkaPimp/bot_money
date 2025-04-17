from aiogram import types
from aiogram.filters import Command

import inline_button


async def register_handlers(dp):
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(cmd_help, Command('help'))


async def cmd_help(message: types.Message):
    user = message
    print(user)
    print(message.from_user.id)
    await message.answer('Types message!')


async def  cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    await message.answer(f'Привет {user_name} {user_last_name}!\n'
                         f'Для начала необходимо зарегистрироваться.\n'
                         f'Нажмите соответствующую кнопку',
                         reply_markup=inline_button.start_inline())


