from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_inline():
    inline_kb_list = [
        [InlineKeyboardButton(text="Регистрация",
                              callback_data='reg')],

        [InlineKeyboardButton(text="Просмотр функций",
                              callback_data='view')],

        [InlineKeyboardButton(text="My_Git😺",
                              url='https://github.com/EgorkaPimp')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

