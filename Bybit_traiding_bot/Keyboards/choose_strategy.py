from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def user_choose_strategy():
    keyboard = [
        [
            InlineKeyboardButton(text="Gold Standard", callback_data='Gold Standard'),
            InlineKeyboardButton(text="High Risk", callback_data='High Risk'),
            InlineKeyboardButton(text="Passive Portfolio", callback_data='Passive Portfolio')

    ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)