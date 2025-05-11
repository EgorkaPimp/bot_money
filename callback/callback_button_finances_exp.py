import datetime

from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
import asyncio

from CallbackDF import CallbackDataFilter
from ClassCallback import View

import db.database, db.serch_match

router = Router()
stop_flag = asyncio.Event()

class FinStates(StatesGroup):
    waiting_month = State()
    waiting_day_month = State()
    waiting_year = State()

def fin_callbacks(dp):
    dp.include_router(router)


@router.callback_query(CallbackDataFilter("fin_day_exp"))
async def fin_callback_day(callback: types.CallbackQuery, state: FSMContext):
    data_month = (datetime.datetime.now()).strftime("%m")
    data_day = (datetime.datetime.now()).strftime("%d")
    data_year = (datetime.datetime.now()).strftime("%y")
    user_id = callback.from_user.id
    categories = db.serch_match.view_categories(user_id, 'expenses')
    view_end, view_sum, graph = View.view_cat(categories, user_id, 'expenses', data_month, data_day, data_year)
    if graph is not None:
        await callback.message.answer_photo(graph)
        View.del_graph(user_id)
    await callback.message.edit_text(f'Ваши расходы на сегодня _{data_day}\\{data_month}\\{data_year}_: \n'
                                     f'{view_end}\n'
                                     f'_Всего потрачено: {view_sum}_', parse_mode="Markdown")
    await state.clear()

@router.callback_query(CallbackDataFilter("fin_pick_day_exp"))
async def fin_day_pick_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите нужную дату\n"
                                     "_Пример: 01-01-25_", parse_mode="Markdown")
    await state.set_state(FinStates.waiting_day_month)


@router.message(FinStates.waiting_day_month)
async def fin_callback_pick_day(message: types.Message, state: FSMContext):
    data_month = ((message.text).split("-"))[1]
    data_day = ((message.text).split("-"))[0]
    data_year = ((message.text).split("-"))[2]
    user_id = message.from_user.id
    categories = db.serch_match.view_categories(user_id, 'expenses')
    view_end, view_sum, graph = View.view_cat(categories, user_id, 'expenses', data_month, data_day, data_year)
    if graph is not None:
        await message.answer_photo(graph)
    await message.answer(f'Ваши расходы на дату _{data_day}\\{data_month}\\{data_year}_: \n'
                                    f'{view_end}\n'
                                    f'_Всего потрачено: {view_sum}_', parse_mode="Markdown")
    await state.clear()

@router.callback_query(CallbackDataFilter("fin_month_exp"))
async def fin_callback_month(callback: types.CallbackQuery, state: FSMContext):
    data_month = (datetime.datetime.now()).strftime("%m")
    data_year = (datetime.datetime.now()).strftime("%y")
    user_id = callback.from_user.id
    categories = db.serch_match.view_categories(user_id, 'expenses')
    view_end, view_sum, graph = View.view_cat(categories, user_id, 'expenses', data_month,  data_year=data_year)
    if graph is not None:
        await callback.message.answer_photo(graph)
        View.del_graph(user_id)
    await callback.message.edit_text(f'Ваши расходы на текущей месяц _{data_month}_: \n'
                                    f'{view_end}\n'
                                    f'_Всего потрачено: {view_sum}_', parse_mode="Markdown")
    await state.clear()

@router.callback_query(CallbackDataFilter("fin_pick_month_exp"))
async def fin_pick_m_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите нужный месяц\n"
                                     "_Пример: 01-25_", parse_mode="Markdown")
    await state.set_state(FinStates.waiting_month)


@router.message(FinStates.waiting_month)
async def fin_callback_pick_month(message: types.Message, state: FSMContext):
    data_month = ((message.text).split("-"))[0]
    data_year = ((message.text).split("-"))[1]
    user_id = message.from_user.id
    categories = db.serch_match.view_categories(user_id, 'expenses')
    view_end, view_sum, graph = View.view_cat(categories, user_id, 'expenses', data_month,  data_year=data_year)
    if graph is not None:
        await message.answer_photo(graph)
        View.del_graph(user_id)
    await message.answer(f'Ваши расходы на _{data_month}\\{data_year}_: \n'
                                    f'{view_end}\n'
                                    f'_Всего потрачено: {view_sum}_', parse_mode="Markdown")
    await state.clear()

@router.callback_query(CallbackDataFilter("view_fin_ear"))
async def fin_pick_m_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите нужный год\n"
                                     "_Пример: 25_\n"
                                     "Если год текущей введите _*_", parse_mode="Markdown")
    await state.set_state(FinStates.waiting_year)


@router.message(FinStates.waiting_year)
async def fin_callback_pick_month(message: types.Message, state: FSMContext):
    if message.text == '*':
        data_year = (message.date.date()).strftime("%y")
    else:
        data_year = message.text
    user_id = message.from_user.id
    categories = db.serch_match.view_categories(user_id, 'expenses')
    view_end, view_sum, graph = View.view_cat(categories, user_id, 'expenses', data_year=data_year)
    if graph is not None:
        await message.answer_photo(graph)
    await message.answer(f'Ваши расходы на _{data_year}_ год: \n'
                                    f'{view_end}\n'
                                    f'_Всего потрачено: {view_sum}_', parse_mode="Markdown")
    await state.clear()