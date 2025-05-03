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


class RegistrationStates(StatesGroup):
    waiting_for_name = State()

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

def register_callbacks(dp):
    dp.include_router(router)