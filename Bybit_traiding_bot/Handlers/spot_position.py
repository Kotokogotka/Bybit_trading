from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StatesGroup, State, StateFilter

from Function.calculate_position import calculate_position_size
from Keyboards.currency_pair import type_position


spot_position_eng = Router = Router()


@spot_position_eng.callback_query(StateFilter(default_state), F.data == 'spot')
async def start_spot_position(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='This function is currently under development\n\n'
             'We will try to release it as soon as possible\n\n'
             'Use the /cancel command to choose actions!'
    )
    await state.clear()