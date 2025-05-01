import asyncio
import logging

from aiogram import types
from aiogram.filters import Command

import inline_button
from db.serch_match import user_nick
from db.database import delete_user

from aiogram.fsm.context import FSMContext

import callback_button

async def register_handlers(dp):
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(cmd_help, Command('help'))
    dp.message.register(cmd_add_category_exp, Command('categories_exp'))
    dp.message.register(cmd_add_category_inc, Command('categories_inc'))
    dp.message.register(cmd_del_ac, Command('del_ac'))
    dp.message.register(cmd_stop, Command('stop'))
    dp.message.register(cmd_register, Command('register'))



async def cmd_help(message: types.Message):
    user = message
    print(user)
    print(message.from_user.id)
    await message.answer('Types message!')

async def cmd_register(message: types.Message):
    await message.answer(f'Время регистрации:',
                         reply_markup=inline_button.start_inline())

async def  cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    await message.answer(f'Привет {user_name} {user_last_name}!\n'
                         f'Для начала необходимо зарегистрироваться.\n'
                         f'Нажмите соответствующую кнопку',
                         reply_markup=inline_button.start_inline())

async def cmd_add_category_exp(message: types.Message):
    await message.answer('Время поработать с категориями расходов! 💸💸💸',
                         reply_markup=inline_button.categories_exp())

async def cmd_add_category_inc(message: types.Message):
    await message.answer('Время поработать с категориями доходов! 💸💸💸',
                         reply_markup=inline_button.categories_inc())

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

async def cmd_stop(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('👌')
    logging.info('add categories stoped')