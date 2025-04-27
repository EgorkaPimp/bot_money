from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


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

def categories_inline():
    inline_kb_list = [
        [InlineKeyboardButton(text="Добавить категорию расходов",
                              callback_data='add_category_exp')],

        [InlineKeyboardButton(text="Удалить категорию расходов",
                              callback_data='del_category_exp')],

        [InlineKeyboardButton(text="Показать категории расходов",
                              callback_data='https://github.com/EgorkaPimp')],

        [InlineKeyboardButton(text="Добавить категорию доходов",
                              callback_data='add_category_inc')],

        [InlineKeyboardButton(text="Удалить категорию доходов",
                              callback_data='del_category_inc')],

        [InlineKeyboardButton(text="Показать категории доходов",
                              callback_data='https://github.com/EgorkaPimp')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
