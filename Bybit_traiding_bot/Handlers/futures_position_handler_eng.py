from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StatesGroup, State, StateFilter

from Function.calculate_position import calculate_position_size
from Keyboards.currency_pair import type_position


calc_router_eng: Router = Router()

user_dict_eng = {}


class InputClientInfo_eng(StatesGroup):
    type_position_eng = State()  # Выбор позиции
    entry_price_eng = State()  # Цена входа в позицию. Это цена, по которой трейдер планирует войти в позицию.
    stop_loss_price_eng = State()  # Цена выхода из позиции при убытке
    deposit_eng = State()  # Размера депозита
    risk_percentage_eng = State()  # Процент риска


@calc_router_eng.callback_query(StateFilter(default_state), F.data == 'futures')
async def process_input_currency_eng(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Select the position you will enter', reply_markup=type_position()
    )
    await state.set_state(InputClientInfo_eng.type_position_eng)
    await callback.message.delete()


@calc_router_eng.callback_query(StateFilter(InputClientInfo_eng.type_position_eng),
                               F.data.in_(['short', 'long']))
async def process_typy_position_eng(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type_position=callback.data)
    await callback.message.delete()
    await callback.message.answer(
        text=f'📝 Please enter a number for the entry price 💹\n\n'
            f'❓ The entry price sets your starting point for a {callback.data} position. '
            'It should be set above the current market price to profit from price drops. '
            'When analyzing the entry price, consider your strategy and expectations, as well as the current level of '
             'risk. '
    )
    await state.set_state(InputClientInfo_eng.entry_price_eng)


@calc_router_eng.message(StateFilter(InputClientInfo_eng.entry_price_eng), lambda message: message.text.replace('.', '', 1).isdigit())
async def process_entry_price_eng(message: Message, state: FSMContext):
    if '.' in message.text:
        entry = float(message.text)
    else:
        entry = int(message.text)

    await state.update_data(entry_price=entry)
    await message.answer(
        text=f'💰 You have specified the entry price {message.text}\n\n'
    )
    await message.answer(
        text='📝 Please enter a number for the exit price 💹\n\n'
'❓ The entry price sets the level at which your trade will be closed in a loss.'
    )
    await state.set_state(InputClientInfo_eng.stop_loss_price_eng)


@calc_router_eng.message(StateFilter(InputClientInfo_eng.entry_price_eng))
async def process_bad_entry_eng(message: Message):
    await message.answer(
        text='❌ The entered value is not an integer or a floating point number (decimal)\n\n'
            'Example: ✅ 1000, 2.3\n'
            'Example: ❌ 100, 66.66\n\n'
            '🚫 If you change your mind, enter /cancel'
    )


@calc_router_eng.message(StateFilter(InputClientInfo_eng.stop_loss_price_eng), lambda message: message.text.replace('.', '', 1).isdigit())
async def process_good_stop_loss_eng(message: Message, state: FSMContext):
    if '.' in message.text:
        stop_loss = float(message.text)
    else:
        stop_loss = int(message.text)
    await state.update_data(stop_loss_price=stop_loss)
    await message.answer(
        text=f'💰 You have indicated the exit price {message.text}\n\n'
    )
    await message.answer(
        text='💰 Please enter the deposit amount as a whole number 💰\n\n'
            '❓ The deposit amount affects your trading strategy and risk level. '
            'This is an important parameter to consider thoroughly when making trading decisions. '
            'Ensure that your risk aligns with your financial capabilities and trading strategy.'
    )
    await state.set_state(InputClientInfo_eng.deposit_eng)


@calc_router_eng.message(StateFilter(InputClientInfo_eng.stop_loss_price_eng))
async def process_bad_stop_loss_eng(message: Message):
    await message.answer(
        text='❌ The entered value is not an integer or a floating point number (decimal)\n\n'
             'Example: ✅ 1000, 2.3\n'
             'Example: ❌ 100, 66.66\n\n'
             '🚫 If you change your mind, enter /cancel'
    )


@calc_router_eng.message(StateFilter(InputClientInfo_eng.deposit_eng), lambda x: int(x.text))
async def process_good_deposit_eng(message: Message, state: FSMContext):
    await state.update_data(deposit=int(message.text))
    await message.answer(
        text=f'💰 The amount of the deposit: {message.text} 💰'
    )
    await message.answer(
        text='📈 Please enter the risk percentage from 1 to 100 📈\n\n'
            '❓ The risk percentage determines how much of your deposit you are willing to lose in a single trade. '
            'This is a critical parameter for managing your investments and controlling losses. '
            'Choose a risk percentage that aligns with your comfort level and your trading strategy.'
    )
    await state.set_state(InputClientInfo_eng.risk_percentage_eng)


@calc_router_eng.message(StateFilter(InputClientInfo_eng.deposit_eng))
async def process_bad_deposit_eng(message: Message):
    await message.answer(
        text='❌ The entered value is not an integer\n\n'
             '🚫 If you have changed your mind, then enter /cancel'
    )


@calc_router_eng.message(StateFilter(InputClientInfo_eng.risk_percentage_eng), lambda x: int(x.text) and 1 <= int(x.text) <= 100)
async def process_good_risk_eng(message: Message, state: FSMContext):
    await state.update_data(risk_percentage=int(message.text))
    await message.answer(
        text=f'📈 Percentage of risk: {message.text} % 📈'
    )

    await message.answer(
        text='🎉 All data is entered!'
    )
    user_dict = await state.get_data()
    await message.answer(f'Position type: {user_dict["type_position"]}\n'
                         f'💰 Entry price: {user_dict["entry_price"]}\n'
                         f'💰 Exit price: {user_dict["stop_loss_price"]}\n'
                         f'💰 Deposit: {user_dict["deposit"]}\n'
                         f'📈 Percentage of risk: {user_dict["risk_percentage"]} %\n'
                         )
    position_volume = calculate_position_size(position_type=user_dict["type_position"],
                                              D=user_dict["deposit"],
                                              PE=user_dict["entry_price"],
                                              PL=user_dict["stop_loss_price"],
                                              R=user_dict["risk_percentage"])
    await message.answer(
        text=f"Position Volume: {position_volume}\n\n"
                f"To perform a new calculation, use the command /cancel")




