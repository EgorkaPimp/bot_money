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

class CategoriesStates(StatesGroup):
    add_categories_inc = State()
    del_category_inc = State()

def cat_inc_callbacks(dp):
    dp.include_router(router)

@router.callback_query(CallbackDataFilter("add_category_inc"))
async def categories_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Добавление категорий: \n"
                                  "Введите название:")
    await state.set_state(CategoriesStates.add_categories_inc)

@router.callback_query(CallbackDataFilter("del_category_inc"))
async def categories_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Удаление категорий: \n"
                                  "Введите название:")
    await state.set_state(CategoriesStates.del_category_inc)

@router.message(CategoriesStates.add_categories_inc)
async def add_cat_inc(message: types.Message):
    user_id = message.from_user.id
    category = message.text
    if db.serch_match.user_exists(user_id):
        nick = db.serch_match.user_nick(user_id)
        if db.serch_match.user_categories(user_id, category.lower(), 'income'):
            logging.info(f'category user was created')
            await message.answer(f"Категория .{category} уже существует")
        else:
            await db.database.add_category(category.lower(), user_id, nick, 'income')
            await message.answer(f"Категория .{category} добавлена. \n"
                                 f"Для ввода следующей категории, введите название\n"
                                 f"Для остановки введите /stop")
    else:
        await  message.answer('Вы не зарегестрированы!\n'
                              'Для работы с категориями зарегестрируйтесь.\n'
                              '/register')

@router.message(CategoriesStates.del_category_inc)
async def del_cat_inc(message: types.Message):
    user_id = message.from_user.id
    category = message.text
    if db.serch_match.user_exists(user_id):
        if db.serch_match.user_categories(user_id, category.lower(), 'income'):
            await db.database.delete_category(user_id, category.lower(), 'income')
            await message.answer(f"Категория .{category} удалена. \n"
                                 f"Для ввода следующей категории, введите название\n"
                                 f"Для остановки введите /stop")
        else:
            logging.info(f"Category ~{category}~ don't search")
            await message.answer(f"Категория .{category} не найдена.")
    else:
        await  message.answer('Вы не зарегестрированы!\n'
                              'Для работы с категориями зарегестрируйтесь.\n'
                              '/register')

@router.callback_query(CallbackDataFilter("view_category_inc"))
async def categories_callback(callback: types.CallbackQuery):
    view_categories = ''
    user_id = callback.from_user.id
    categories = db.serch_match.view_categories(user_id, 'income')
    for category in categories:
        view_categories = view_categories + f'{category[0].title()}' + '\n'
    await callback.message.edit_text(f'Ваши категории: \n{view_categories}')