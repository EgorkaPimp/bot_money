import logging
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.filters import Filter
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
import asyncio
from CallbackDF import CallbackDataFilter

from pyexpat.errors import messages

import db.database, db.serch_match
import inline_button

router = Router()

stop_flag = asyncio.Event()
class Add_Finance(StatesGroup):
    waiting_exp = State()
    waiting_inc = State()
    waiting_data_exp = State()
    waiting_data_inc = State()
    waiting_comment_exp = State()
    waiting_comment_inc = State()

def add_fin_callbacks(dp):
    dp.include_router(router)

@router.callback_query(F.data.startswith('add_exp_'))
async def add_exp(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[-1]
    await state.update_data(category=category)
    await state.set_state(Add_Finance.waiting_exp)
    await callback.message.edit_text(f"Введите сумму для {category}:")

@router.callback_query(F.data.startswith('add_inc_'))
async def add_exp(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[-1]
    await state.update_data(category=category)
    await state.set_state(Add_Finance.waiting_inc)
    await callback.message.edit_text(f"Введите сумму для {category}:")

@router.message(Add_Finance.waiting_exp)
async def del_cat_inc(message: types.Message, state: FSMContext):
    sum_exp = message.text
    await state.update_data(sum_exp=sum_exp)
    await state.set_state(Add_Finance.waiting_data_exp)
    await message.answer('Введите дату в формате _ДЕНЬ-МЕСЯЦ-ГОД_ \n'
                         'Пример _01-01-25_ \n'
                         'Для ввода сегоднящней даты введите _*_',
                         parse_mode="Markdown")

@router.message(Add_Finance.waiting_inc)
async def del_cat_inc(message: types.Message, state: FSMContext):
    sum_exp = message.text
    await state.update_data(sum_exp=sum_exp)
    await state.set_state(Add_Finance.waiting_data_inc)
    await message.answer('Введите дату в формате _ДЕНЬ-МЕСЯЦ-ГОД_ \n'
                         'Пример _01-01-25_ \n'
                         'Для ввода сегоднящней даты введите _*_',
                         parse_mode="Markdown")

@router.message(Add_Finance.waiting_data_exp)
async def del_cat_inc(message: types.Message, state: FSMContext):
    data_exp = message.text
    if data_exp == "*":
        data_day = (message.date.date()).strftime("%d")
        data_month = (message.date.date()).strftime("%m")
        data_year = (message.date.date()).strftime("%y")
    else:
        data_day = (data_exp.split('-'))[0]
        data_month = (data_exp.split('-'))[1]
        data_year = (data_exp.split('-'))[2]
    await state.update_data(data_day=data_day,
                            data_month=data_month,
                            data_year=data_year)
    await state.set_state(Add_Finance.waiting_comment_exp)
    await message.answer('Введите коментарий к трате:')

@router.message(Add_Finance.waiting_data_inc)
async def del_cat_inc(message: types.Message, state: FSMContext):
    data_exp = message.text
    if data_exp == "*":
        data_day = (message.date.date()).strftime("%d")
        data_month = (message.date.date()).strftime("%m")
        data_year = (message.date.date()).strftime("%y")
    else:
        data_day = (data_exp.split('-'))[0]
        data_month = (data_exp.split('-'))[1]
        data_year = (data_exp.split('-'))[2]
    await state.update_data(data_day=data_day,
                            data_month=data_month,
                            data_year=data_year)
    await state.set_state(Add_Finance.waiting_comment_inc)
    await message.answer('Введите коментарий к зароботку:')

@router.message(Add_Finance.waiting_comment_exp)
async def del_cat_inc(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    category = data['category']
    sum_exp = data['sum_exp']
    data_day = data['data_day']
    data_month = data['data_month']
    data_year = data['data_year']
    comment = message.text
    await db.database.add_exp(user_id, category, sum_exp,
                              data_day, data_month, data_year, comment, 'expenses')
    await message.answer(f'Добавлена трата: \n'
                         f'*{category}*: {sum_exp} \n'
                         f'*Дата:* {data_day}/{data_month} \n'
                         f'_{comment}_', parse_mode="Markdown")
    await state.clear()

@router.message(Add_Finance.waiting_comment_inc)
async def del_cat_inc(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    category = data['category']
    sum_exp = data['sum_exp']
    data_day = data['data_day']
    data_month = data['data_month']
    data_year = data['data_year']
    comment = message.text
    await db.database.add_exp(user_id, category, sum_exp,
                              data_day, data_month, data_year, comment, 'income')
    await message.answer(f'Добавлено поступление: \n'
                         f'*{category}*: {sum_exp} \n'
                         f'*Дата:* {data_day}/{data_month}/{data_year} \n'
                         f'_{comment}_', parse_mode="Markdown")
    await state.clear()