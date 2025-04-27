import logging
from aiogram.fsm.context import FSMContext
from aiogram import Router, types
from aiogram.filters import Filter
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State

import db.database, db.serch_match

router = Router()

class CallbackDataFilter(Filter):
    def __init__(self, data: str) -> None:
        self.data = data

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == self.data

class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()

@router.callback_query(CallbackDataFilter("reg"))
async def registration_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Регистрация: \n"
                                     "Придумайте себе никнейм:")
    await state.set_state(RegistrationStates.waiting_for_name)

@router.callback_query(CallbackDataFilter("view"))
async def registration_callback(callback: types.CallbackQuery):
    await callback.message.answer("***********")

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
    logging.error(result)
    if result:
        logging.info(result)
        await message.answer('Вы успешно зарегистрировались 👏👏👏\n')
    else:
        nick = db.serch_match.user_nick(user_id)
        await message.answer(f'Вы уже были зарегестрированы!🫣 \nВаш ник: {nick}\n')




def register_callbacks(dp):
    dp.include_router(router)