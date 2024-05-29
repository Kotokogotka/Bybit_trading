from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def user_calc_sig():
    keyboard = [
        [
            InlineKeyboardButton(text="calculator", callback_data='calc'),
            InlineKeyboardButton(text="signals", callback_data='sig'),
            InlineKeyboardButton(text="New Strategy", callback_data='new')
    ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)