import logging
from aiogram.fsm.context import FSMContext
from aiogram import Router, types
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
    await callback.message.answer("Добавление категорий: \n"
                                  "Введите название:")
    await state.set_state(RegistrationStates.add_categories_ex)

@router.callback_query(CallbackDataFilter("add_category_inc"))
async def categories_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Добавление категорий: \n"
                                  "Введите название:")
    await state.set_state(RegistrationStates.add_categories_inc)

@router.message(RegistrationStates.add_categories_ex)
async def add_cat_exp(message: types.Message, ):
    user_id = message.from_user.id
    category = message.text
    if db.serch_match.user_exists(user_id):
        nick = db.serch_match.user_nick(user_id)
        if db.serch_match.user_categories(user_id, category.lower(), 'expenses'):
            logging.info(f'category user was created')
            await message.answer(f"Категория {category} уже существует")
        else:
            await db.database.add_category(category.lower(), user_id, nick, 'expenses')
            await message.answer(f"Категория {category} добавлена. \n"
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
    nick = db.serch_match.user_nick(user_id)
    if db.serch_match.user_categories(user_id, category.lower(), 'income'):
        logging.info(f'category user was created')
        await message.answer(f"Категория {category} уже существует")
    else:
        await db.database.add_category(category.lower(), user_id, nick, 'income')
        await message.answer(f"Категория {category} добавлена. \n"
                             f"Для ввода следующей категории, введите название\n"
                             f"Для остановки введите /stop")



def register_callbacks(dp):
    dp.include_router(router)