from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def user_yes_no():
    keyboard = [
        [
            InlineKeyboardButton(text="Yes", callback_data='yes'),
            InlineKeyboardButton(text="No", callback_data='no')
    ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)