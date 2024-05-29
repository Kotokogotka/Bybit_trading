from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def type_position():
    keyboard = [
        [
            InlineKeyboardButton(text="Long", callback_data='long'),
            InlineKeyboardButton(text="Short", callback_data='short')
    ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)