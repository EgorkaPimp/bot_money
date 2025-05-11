import datetime
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
import asyncio

from CallbackDF import CallbackDataFilter

import db.database, db.serch_match

router = Router()

stop_flag = asyncio.Event()

class FinStates(StatesGroup):
    waiting_month_inc = State()
    waiting_day_month_inc = State()
    waiting_year_inc = State()

def fin_callbacks_inc(dp):
    dp.include_router(router)

def view_cat(categories, user_id, type_cat, data_month=None, data_day=None, data_year=None):
    view_map = {}
    view_end = ""
    view_sum = 0
    for category in categories:
        sum_month = db.serch_match.search_money(user_id, category[0],
                                                    data_month, data_day, data_year, type_cat)
        sum_all = 0
        for sum_cat in sum_month:
            if ',' in sum_cat[0]:
                value = float(sum_cat[0].replace(',', '.'))
            else:
                value = sum_cat[0]
            print(value)
            sum_all = sum_all + value
        view_map.setdefault(category[0], sum_all)
    for i in view_map:
        line = f"*{i}* - {view_map[i]} \n"
        view_end = view_end + line
        view_sum = view_sum + view_map[i]
    return view_end, view_sum

@router.callback_query(CallbackDataFilter("fin_day_inc"))
async def fin_callback_day(callback: types.CallbackQuery, state: FSMContext):
    data_month = (datetime.datetime.now()).strftime("%m")
    data_day = (datetime.datetime.now()).strftime("%d")
    data_year = (datetime.datetime.now()).strftime("%y")
    user_id = callback.from_user.id
    categories = db.serch_match.view_categories(user_id, 'income')
    view_end, view_sum = view_cat(categories, user_id, 'income', data_month, data_day, data_year)
    await callback.message.edit_text(f'Ваш доход на сегодня _{data_month}_: \n'
                                    f'{view_end}\n'
                                    f'_Всего заработано: {view_sum}_', parse_mode="Markdown")
    await state.clear()

@router.callback_query(CallbackDataFilter("fin_pick_day_inc"))
async def fin_day_pick_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите нужную дату\n"
                                     "_Пример: 01-01-25_", parse_mode="Markdown")
    await state.set_state(FinStates.waiting_day_month_inc)


@router.message(FinStates.waiting_day_month_inc)
async def fin_callback_pick_day(message: types.Message, state: FSMContext):
    data_month = ((message.text).split("-"))[1]
    data_day = ((message.text).split("-"))[0]
    data_year = ((message.text).split("-"))[2]
    user_id = message.from_user.id
    categories = db.serch_match.view_categories(user_id, 'income')
    view_end, view_sum = view_cat(categories, user_id, 'income', data_month, data_day, data_year)
    await message.answer(f'Ваш доход на дату _{data_day}\\{data_month}\\{data_year}_: \n'
                                    f'{view_end}\n'
                                    f'_Всего заработано: {view_sum}_', parse_mode="Markdown")
    await state.clear()

@router.callback_query(CallbackDataFilter("fin_month_inc"))
async def fin_callback_month(callback: types.CallbackQuery, state: FSMContext):
    data_month = (datetime.datetime.now()).strftime("%m")
    data_year = (datetime.datetime.now()).strftime("%y")
    user_id = callback.from_user.id
    categories = db.serch_match.view_categories(user_id, 'income')
    view_end, view_sum = view_cat(categories, user_id, 'income', data_month, data_year=data_year)
    await callback.message.edit_text(f'Ваш доход на текущей месяц _{data_month}_: \n'
                                    f'{view_end}\n'
                                    f'_Всего заработано: {view_sum}_', parse_mode="Markdown")
    await state.clear()

@router.callback_query(CallbackDataFilter("fin_pick_month_inc"))
async def fin_pick_m_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите нужный месяц\n"
                                     "_Пример: 01-25_", parse_mode="Markdown")
    await state.set_state(FinStates.waiting_month_inc)


@router.message(FinStates.waiting_month_inc)
async def fin_callback_pick_month(message: types.Message, state: FSMContext):
    data_month = ((message.text).split("-"))[0]
    data_year = ((message.text).split("-"))[1]
    user_id = message.from_user.id
    categories = db.serch_match.view_categories(user_id, 'income')
    view_end, view_sum = view_cat(categories, user_id, 'income', data_month, data_year=data_year)
    await message.answer(f'Ваш доход _{data_month}\\{data_year}_: \n'
                                    f'{view_end}\n'
                                    f'_Всего заработано: {view_sum}_', parse_mode="Markdown")
    await state.clear()

@router.callback_query(CallbackDataFilter("view_fin_ear_inc"))
async def fin_pick_m_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите нужный год\n"
                                     "_Пример: 01_\n"
                                     "Если год текущей введите _*_", parse_mode="Markdown")
    await state.set_state(FinStates.waiting_year_inc)


@router.message(FinStates.waiting_year_inc)
async def fin_callback_pick_month(message: types.Message, state: FSMContext):
    if message.text == '*':
        data_year = (message.date.date()).strftime("%y")
    else:
        data_year = message.text
    user_id = message.from_user.id
    categories = db.serch_match.view_categories(user_id, 'income')
    view_end, view_sum = view_cat(categories, user_id, 'income', data_year=data_year)
    await message.answer(f'Ваш доход на _{data_year}_ год: \n'
                                    f'{view_end}\n'
                                    f'_Всего заработано: {view_sum}_', parse_mode="Markdown")
    await state.clear()