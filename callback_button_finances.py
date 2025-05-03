import datetime
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

class FinStates(StatesGroup):
    waiting_month = State()
    waiting_day_month = State()

@router.callback_query(CallbackDataFilter("fin_month_exp"))
async def fin_callback_month(callback: types.CallbackQuery, state: FSMContext):
    view_test = {}
    data_month = (datetime.datetime.now()).strftime("%m")
    user_id = callback.from_user.id
    view_end = ''
    categories = db.serch_match.view_categories(user_id, 'expenses')
    for category in categories:
        sum_month = db.serch_match.search_money_month(user_id, category[0],
                                                data_month, 'expenses')
        sum_all = 0
        for sum_cat in sum_month:
            sum_all = sum_all + sum_cat[0]
        view_test.setdefault(category[0], sum_all)
    for i in view_test:
        line = f"*{i}* - {view_test[i]} \n"
        view_end = view_end + line
    await callback.message.edit_text(f'Ваши расходы на текущей месяц _{data_month}_: \n'
                                  f'{view_end}', parse_mode="Markdown")

@router.callback_query(CallbackDataFilter("fin_pick_month_exp"))
async def fin_pick_m_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите нужный месяц\n"
                                     "_Пример: 01_", parse_mode="Markdown")
    await state.set_state(FinStates.waiting_month)


@router.message(FinStates.waiting_month)
async def fin_callback_pick_month(message: types.Message):
    view_test = {}
    data_month = message.text
    user_id = message.from_user.id
    view_end = ''
    categories = db.serch_match.view_categories(user_id, 'expenses')
    for category in categories:
        sum_month = db.serch_match.search_money_month(user_id, category[0],
                                                data_month, 'expenses')
        sum_all = 0
        for sum_cat in sum_month:
            sum_all = sum_all + sum_cat[0]
        view_test.setdefault(category[0], sum_all)
    for i in view_test:
        line = f"*{i}* - {view_test[i]} \n"
        view_end = view_end + line
    await message.answer(f'Ваши расходы на текущей месяц _{data_month}_: \n'
                                  f'{view_end}', parse_mode="Markdown")

@router.callback_query(CallbackDataFilter("fin_day_exp"))
async def fin_callback_day(callback: types.CallbackQuery, state: FSMContext):
    view_test = {}
    data_month = (datetime.datetime.now()).strftime("%m")
    data_day = (datetime.datetime.now()).strftime("%d")
    user_id = callback.from_user.id
    view_end = ''
    categories = db.serch_match.view_categories(user_id, 'expenses')
    for category in categories:
        sum_month = db.serch_match.search_money_day(user_id, category[0],
                                                data_month, data_day, 'expenses')
        sum_all = 0
        for sum_cat in sum_month:
            sum_all = sum_all + sum_cat[0]
        view_test.setdefault(category[0], sum_all)
    for i in view_test:
        line = f"*{i}* - {view_test[i]} \n"
        view_end = view_end + line
    await callback.message.edit_text(f'Ваши расходы на сегодня _{data_month}_: \n'
                                  f'{view_end}', parse_mode="Markdown")

@router.callback_query(CallbackDataFilter("fin_pick_day_exp"))
async def fin_day_pick_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите нужный месяц и дату\n"
                                     "_Пример: 14-01_", parse_mode="Markdown")
    await state.set_state(FinStates.waiting_day_month)


@router.message(FinStates.waiting_day_month)
async def fin_callback_pick_day(message: types.Message):
    view_test = {}
    data_month = ((message.text).split("-"))[1]
    data_day = ((message.text).split("-"))[0]
    user_id = message.from_user.id
    view_end = ''
    categories = db.serch_match.view_categories(user_id, 'expenses')
    for category in categories:
        sum_month = db.serch_match.search_money_day(user_id, category[0],
                                                data_month, data_day, 'expenses')
        sum_all = 0
        for sum_cat in sum_month:
            sum_all = sum_all + sum_cat[0]
        view_test.setdefault(category[0], sum_all)
    for i in view_test:
        line = f"*{i}* - {view_test[i]} \n"
        view_end = view_end + line
    await message.answer(f'Ваши расходы на дату _{data_day}\\{data_month}_: \n'
                                  f'{view_end}', parse_mode="Markdown")



def fin_callbacks(dp):
    dp.include_router(router)