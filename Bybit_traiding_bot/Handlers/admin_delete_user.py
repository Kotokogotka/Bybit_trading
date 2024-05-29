from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StatesGroup, State, StateFilter

from DataBase.database import delete_user_in_users, check_id_in_db



class DeleteUser(StatesGroup):
    telegram_id = State()  # Ожидание ввода id нового


delete_user = Router()


user_id = {}


@delete_user.callback_query(StateFilter(default_state), F.data == 'delete')
async def add_new_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='To delete user, enter their telegram id')
    await state.set_state(DeleteUser.telegram_id)


@delete_user.message(StateFilter(DeleteUser.telegram_id))
async def good_id(message: Message, state: FSMContext):
    try:
        tg_id = int(message.text)
        if check_id_in_db(tg_id=tg_id):
            await state.update_data(tg_id=tg_id)
            delete_user_in_users(tg_id=tg_id)
            await state.clear()
            await message.answer("User delete successfully!")
        else:
            await message.answer("This user was not found in the database\n\n"
                                 "Use the /cancel command")
    except ValueError:
        await bad_telegram_id(message)


@delete_user.message(StateFilter(DeleteUser.telegram_id))
async def bad_telegram_id(message: Message):
    await message.answer(
        text=f'User ID should be entered as digits.\n'
       f'Send any message from the selected user to @getmyid_bot and copy the ID.\n\n'
       f'If you changed your mind, use the /cancel command.')


