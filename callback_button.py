import logging
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.filters import Filter
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
import asyncio

import db.database, db.serch_match
import inline_button

router = Router()

stop_flag = asyncio.Event()

class CallbackDataFilter(Filter):
    def __init__(self, data: str) -> None:
        self.data = data

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == self.data

class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    add_categories_ex = State()
    add_categories_inc = State()
    del_category_exp = State()
    del_category_inc = State()
    waiting_exp = State()
    waiting_inc = State()

@router.callback_query(CallbackDataFilter("reg"))
async def registration_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Регистрация: \n"
                                     "Придумайте себе никнейм:")
    await state.set_state(RegistrationStates.waiting_for_name)

@router.callback_query(CallbackDataFilter("view"))
async def registration_callback(callback: types.CallbackQuery):
    await callback.message.answer("Вы просматриваете фнкционал, "
                                  "что бы я нача считать ваши деньгии, "
                                  "надо зарегистрироватьяс.")

@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: types.Message):
    nik_name = message.text
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    start_data = (message.date.date()).strftime("%D")
    time_register = (message.date.time()).strftime("%H:%M:%S")
    result = await db.database.add_user(user_id, nik_name, user_name,
                               user_last_name, start_data, time_register)
    if result:
        await message.answer('Вы успешно зарегистрировались 👏👏👏\n')
    else:
        nick = db.serch_match.user_nick(user_id)
        await message.answer(f'Вы уже были зарегестрированы!🫣 \nВаш ник: {nick}\n')

@router.callback_query(CallbackDataFilter("add_category_exp"))
async def categories_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Добавление категорий: \n"
                                  "Введите название:")
    await state.set_state(RegistrationStates.add_categories_ex)

@router.callback_query(CallbackDataFilter("add_category_inc"))
async def categories_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Добавление категорий: \n"
                                  "Введите название:")
    await state.set_state(RegistrationStates.add_categories_inc)

@router.callback_query(CallbackDataFilter("del_category_exp"))
async def categories_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Удаление категорий: \n"
                                  "Введите название:")
    await state.set_state(RegistrationStates.del_category_exp)

@router.callback_query(CallbackDataFilter("del_category_inc"))
async def categories_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Удаление категорий: \n"
                                  "Введите название:")
    await state.set_state(RegistrationStates.del_category_inc)

@router.callback_query(CallbackDataFilter("del_category_inc"))
async def categories_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Удаление категорий: \n"
                                  "Введите название:")
    await state.set_state(RegistrationStates.del_category_inc)

@router.callback_query(CallbackDataFilter("view_category_exp"))
async def categories_callback(callback: types.CallbackQuery):
    view_categories = ''
    user_id = callback.from_user.id
    categories = db.serch_match.view_categories(user_id, 'expenses')
    for category in categories:
        view_categories = view_categories + f'.{category[0].title()}' + '\n'
    await callback.message.edit_text(f'Ваши категории: \n{view_categories}')

@router.callback_query(CallbackDataFilter("view_category_inc"))
async def categories_callback(callback: types.CallbackQuery):
    view_categories = ''
    user_id = callback.from_user.id
    categories = db.serch_match.view_categories(user_id, 'income')
    for category in categories:
        view_categories = view_categories + f'{category[0].title()}' + '\n'
    await callback.message.edit_text(f'Ваши категории: \n{view_categories}')

@router.callback_query(F.data.startswith('add_exp_'))
async def add_exp(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[-1]
    await state.update_data(category=category)
    await state.set_state(RegistrationStates.waiting_exp)
    await callback.message.edit_text(f"Введите сумму для {category}:")

@router.callback_query(F.data.startswith('add_inc_'))
async def add_exp(callback: types.CallbackQuery, state: FSMContext):
    category = callback.data.split("_")[-1]
    await state.update_data(category=category)
    await state.set_state(RegistrationStates.waiting_inc)
    await callback.message.edit_text(f"Введите сумму для {category}:")

@router.message(RegistrationStates.add_categories_ex)
async def add_cat_exp(message: types.Message, ):
    user_id = message.from_user.id
    category = message.text
    if db.serch_match.user_exists(user_id):
        nick = db.serch_match.user_nick(user_id)
        if db.serch_match.user_categories(user_id, category.lower(), 'expenses'):
            logging.info(f'category user was created')
            await message.answer(f"Категория .{category} уже существует")
        else:
            await db.database.add_category(category.lower(), user_id, nick, 'expenses')
            await message.answer(f"Категория .{category} добавлена. \n"
                                 f"Для ввода следующей категории, введите название\n"
                                 f"Для остановки введите /stop")
    else:
        await  message.answer('Вы не зарегестрированы!\n'
                              'Для работы с категориями зарегестрируйтесь.\n'
                              '/register')

@router.message(RegistrationStates.add_categories_inc)
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

@router.message(RegistrationStates.del_category_exp)
async def del_cat_exp(message: types.Message):
    user_id = message.from_user.id
    category = message.text
    if db.serch_match.user_exists(user_id):
        if db.serch_match.user_categories(user_id, category.lower(), 'expenses'):
            await db.database.delete_category(user_id, category.lower(), 'expenses')
            await message.answer(f"Категория .{category} удалена. \n"
                                 f"Для ввода следующей категории, введите название\n"
                                 f"Для остановки введите /stop")
        else:
            await message.answer(f"Категория .{category} не найдена.")
            logging.info(f"Category {category} don't search")
    else:
        await  message.answer('Вы не зарегестрированы!\n'
                              'Для работы с категориями зарегестрируйтесь.\n'
                              '/register')

@router.message(RegistrationStates.del_category_inc)
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

@router.message(RegistrationStates.waiting_exp)
async def del_cat_inc(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    category = data['category']
    sum_exp = message.text
    await db.database.add_exp(user_id, category, sum_exp, 'expenses')

@router.message(RegistrationStates.waiting_inc)
async def del_cat_inc(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    category = data['category']
    sum_exp = message.text
    await db.database.add_exp(user_id, category, sum_exp, 'income')

def register_callbacks(dp):
    dp.include_router(router)