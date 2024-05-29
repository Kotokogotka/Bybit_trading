from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_add_delete():
    keyboard = [
        [
            InlineKeyboardButton(text="🤝📥 add_user", callback_data='add'),
            InlineKeyboardButton(text="❌👤 delete_user", callback_data='delete')
    ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)