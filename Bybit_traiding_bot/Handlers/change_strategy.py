from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import StateFilter

from Lexicon.commands_eng import commands_eng
from Keyboards.choose_strategy import user_choose_strategy
from DataBase.database import check_id_in_high, check_id_in_gold, check_id_in_passive, add_user_in_passive, \
    add_user_in_high, add_user_in_gold, delete_user_in_gold, delete_user_in_passive, delete_user_in_high
from Keyboards.yes_no import user_yes_no



class NewStrategyInfo(StatesGroup):
    new_strategy = State()
    new_depo = State()
    old_strategy = State()

new_strategy_dict = {}

new_strategy_router = Router()


@new_strategy_router.callback_query(StateFilter(default_state), F.data == 'new')
async def process_change_strategy(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    old_strategy = None

    if check_id_in_passive(user_id):
        old_strategy = 'Passive Portfolio'
    elif check_id_in_gold(user_id):
        old_strategy = 'Gold Standard'
    elif check_id_in_high(user_id):
        old_strategy = 'High Risk'

    if old_strategy:
        await state.update_data(old_strategy=old_strategy)
        await callback.message.answer(
            text=f'You have chosen the {old_strategy} strategy'
        )

        # Запрос у пользователя подтверждения смены стратегии
        await callback.message.answer(
            text='Do you really want to change your strategy?',
            reply_markup=user_yes_no()
        )
    else:
        await callback.message.answer(
            text='You have not chosen any of the strategies'
        )

    await state.set_state(NewStrategyInfo.new_strategy)


@new_strategy_router.callback_query(F.data == 'yes', StateFilter(NewStrategyInfo.new_strategy))
async def confirm_change_strategy(callback: CallbackQuery, state: FSMContext):
    strategy_data = await state.get_data()
    user_id = callback.from_user.id
    old_strategy = strategy_data.get('old_strategy')

    # Удаляем данные из соответствующей таблицы
    if old_strategy == 'Gold Standard':
        delete_user_in_gold(user_id)
    if old_strategy == 'High Risk':
        delete_user_in_high(user_id)
    if old_strategy == 'Passive Portfolio':
        delete_user_in_passive(user_id)

    await callback.message.answer(
        text='Your old strategy data has been successfully deleted. Choose a new strategy now.',
        reply_markup=user_choose_strategy()
    )
    await state.set_state(NewStrategyInfo.new_strategy)



@new_strategy_router.callback_query(F.data == 'no', StateFilter(NewStrategyInfo.new_strategy))
async def cancel_change_strategy(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='You have cancelled the change of strategy'
    )
    await state.clear()


@new_strategy_router.callback_query(StateFilter(NewStrategyInfo.new_strategy),
                                  F.data.in_(['Gold Standard', 'High Risk', 'Passive Portfolio']))
async def input_depo(callback: CallbackQuery, state: FSMContext):
    await state.update_data(strategy=callback.data)

    if callback.data == 'Gold Standard':
        await callback.message.answer(
            text=commands_eng['gold_choose']
        )
    if callback.data == 'High Risk':
        await callback.message.answer(
            text=commands_eng['high_risk_choose']
        )
    if callback.data == 'Passive Portfolio':
        await callback.message.answer(
            text=commands_eng['passive_choose']
        )
    await callback.message.answer(
        text='💰 Enter the amount of your deposit'
    )
    await state.set_state(NewStrategyInfo.new_depo)


@new_strategy_router.message(StateFilter(NewStrategyInfo.new_depo))
async def input_data(message: Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        if int(message.text):
            await state.update_data(depo=int(message.text))
            strategy_dict = await state.get_data()
            if strategy_dict["strategy"] == 'Gold Standard':
                if not check_id_in_gold(tg_id=user_id):
                    add_user_in_gold(tg_id=user_id, deposit=strategy_dict["depo"])
                    await message.answer(
                        text=f'🚀 The chosen strategy: {strategy_dict["strategy"]} \n'
                             f'💰 Deposit amount: {strategy_dict["depo"]}\n\n'
                    )
                    await message.answer(
                        text=commands_eng['after_input_deposite']
                    )
                else:
                    await message.answer(
                        text='You have already chosen this strategy\n'
                             'Use the command /cancel to get started'
                    )
            if strategy_dict["strategy"] == 'High Risk':
                if not check_id_in_high(tg_id=user_id):
                    add_user_in_high(tg_id=user_id, deposit=strategy_dict["depo"])
                    await message.answer(
                        text=f'🚀 The chosen strategy: {strategy_dict["strategy"]} \n'
                             f'💰 Deposit amount: {strategy_dict["depo"]}\n'
                    )
                    await message.answer(
                        text=commands_eng['after_input_deposite'])
                else:
                    await message.answer(
                        text='You have already chosen this strategy\n'
                             'Use the command /cancel to get started'
                    )
                    await message.answer(
                        text=commands_eng['after_input_deposite'])
            if strategy_dict["strategy"] == 'Passive Portfolio':
                if not check_id_in_passive(tg_id=user_id):
                    add_user_in_passive(tg_id=user_id, deposit=strategy_dict["depo"])
                    await message.answer(
                        text=f'🚀 The chosen strategy: {strategy_dict["strategy"]} \n'
                             f'💰 Deposit amount: {strategy_dict["depo"]}\n'
                    )
                else:
                    await message.answer(
                        text='You have already chosen this strategy\n'
                             'Use the command /cancel to get started'
                    )
            await state.clear()
    except ValueError:
        await message.answer(
            text='❌ The entered value is not an integer\n\n'
                 'Try again\n\n'
                 '🚫 If you have changed your mind, then enter /cancel'
        )