from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def user_futures_spot():
    keyboard = [
        [
            InlineKeyboardButton(text="Futures", callback_data='futures'),
            InlineKeyboardButton(text="Spot", callback_data='spot')
    ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)