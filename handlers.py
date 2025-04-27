import logging

from aiogram import types
from aiogram.filters import Command

import inline_button
from db.serch_match import user_nick
from db.database import delete_user


async def register_handlers(dp):
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(cmd_help, Command('help'))
    dp.message.register(cmd_add_category_exp, Command('categories'))
    dp.message.register(cmd_del_ac, Command('del_ac'))



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

async def cmd_add_category_exp(message: types.Message):
    await message.answer('Время паработать с категориями!',
                         reply_markup=inline_button.categories_inline())

async def cmd_del_ac(message: types.Message):
    user_id = message.from_user.id
    nick = user_nick(user_id)
    user_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    delete_user(user_id)
    logging.info(f'User {user_id}:{user_name}_{user_last_name} deleted')
    await message.answer(f'Уважаемый/ая {user_name} {user_last_name} \n'
                         f'Ваш аккаунт {nick} удален! \n'
                         f'Все расходы, и категории удалены безвозвратно')