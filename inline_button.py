from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

import db

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

def categories_exp():
    inline_kb_list = [
        [InlineKeyboardButton(text="Показать категории расходов",
                              callback_data='view_category_exp')],

        [InlineKeyboardButton(text="Добавить категорию расходов",
                              callback_data='add_category_exp')],

        [InlineKeyboardButton(text="Удалить категорию расходов",
                              callback_data='del_category_exp')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def categories_inc():
    inline_kb_list = [
        [InlineKeyboardButton(text="Показать категории доходов",
                              callback_data='view_category_inc')],

        [InlineKeyboardButton(text="Добавить категорию доходов",
                              callback_data='add_category_inc')],

        [InlineKeyboardButton(text="Удалить категорию доходов",
                              callback_data='del_category_inc')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def add_exp(user_id):
    categories = db.serch_match.view_categories(user_id, 'expenses')
    inline_kb_list = []
    for cat in categories:
        format_key = []
        format_key.append(InlineKeyboardButton(text=f"{cat[0].title()}",
                              callback_data=f'add_exp_{cat[0].title()}'))
        inline_kb_list.append(format_key)
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def add_inc(user_id):
    categories = db.serch_match.view_categories(user_id, 'income')
    inline_kb_list = []
    for cat in categories:
        format_key = []
        format_key.append(InlineKeyboardButton(text=f"{cat[0].title()}",
                              callback_data=f'add_inc_{cat[0].title()}'))
        inline_kb_list.append(format_key)
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

def finances_exp():
    inline_kb_list = [
        [InlineKeyboardButton(text="Показать расходы за текущий день",
                              callback_data='fin_day_exp')],

        [InlineKeyboardButton(text="Показать расходы за определенный день",
                              callback_data='fin_pick_day_exp')],

        [InlineKeyboardButton(text="Показать расходы за текущий месяц",
                              callback_data='fin_month_exp')],

        [InlineKeyboardButton(text="Показать расходы за определенный месяц",
                              callback_data='fin_pick_month_exp')],

        [InlineKeyboardButton(text="Показать расходы за год",
                              callback_data='view_fin_ear')],

        [InlineKeyboardButton(text="Показать расходы по конкретной категории",
                              callback_data='view_fin_cat')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


