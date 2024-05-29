from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram.filters.state import StateFilter


from Lexicon.commands_eng import commands_eng
from Keyboards.choose_strategy import user_choose_strategy
from DataBase.database import check_id_in_passive, check_id_in_gold, check_id_in_high, add_user_in_gold, \
    add_user_in_high, add_user_in_passive, session, GoldStandard, HighRisk, PassivePortfolio
from Function.read_message import calculate_position_size, process_message



class StrategyInfo(StatesGroup):
    strategy = State()
    depo = State()
    signal = State()


strategy_dict = {}

signal_router_eng: Router = Router()


@signal_router_eng.callback_query(StateFilter(default_state), F.data == 'sig')
async def choose_signal(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if not check_id_in_high(user_id) or not check_id_in_gold(user_id) or not check_id_in_passive(user_id):
        await callback.message.answer(
            text=commands_eng['signal_1'], reply_markup=user_choose_strategy()
        )
        await state.set_state(StrategyInfo.strategy)
    else:
        await callback.message.answer(
            text='Use the /cancel command and choose the strategy that suits you'
        )


@signal_router_eng.callback_query(StateFilter(StrategyInfo.strategy),
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
    await state.set_state(StrategyInfo.depo)


@signal_router_eng.message(StateFilter(StrategyInfo.depo))
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
            await state.set_state(StrategyInfo.signal)
            await state.clear()
    except ValueError:
        await message.answer(
            text='❌ The entered value is not an integer\n\n'
                 'Try again\n\n'
                 '🚫 If you have changed your mind, then enter /cancel'
        )


@signal_router_eng.message(lambda message: 'Position type' in message.text)
async def handle_position_info(message: Message):

    process_message(message.text)
    user_id = message.from_user.id
    deposit = 10000  # Общий депозит

    # Проверяем, в какой из таблиц пользователь есть
    if session.query(GoldStandard).filter_by(user_id=user_id).first():
        deposit = session.query(GoldStandard).filter_by(user_id=user_id).first().deposit
    elif session.query(HighRisk).filter_by(user_id=user_id).first():
        deposit = session.query(HighRisk).filter_by(user_id=user_id).first().deposit
    elif session.query(PassivePortfolio).filter_by(user_id=user_id).first():
        deposit = session.query(PassivePortfolio).filter_by(user_id=user_id).first().deposit

    # Чтение содержимого файлов
    with open('position_type.txt', 'r') as file:
        position_type = file.read().strip().lower()
    with open('entry.txt', 'r') as file:
        entry_prices = [float(line.strip()) for line in file if line.strip()]
    with open('stop_loss.txt', 'r') as file:
        stop_loss_price_str = file.readline().strip()
        if stop_loss_price_str:  # Проверяем, что строка не пустая
            stop_loss_price = float(stop_loss_price_str)
        else:
            stop_loss_price = 0  # Устанавливаем значение по умолчанию, если строка пустая

    with open('risk_percent.txt', 'r') as file:
        risk_percent = float(file.readline().strip())

    # Расчет размеров позиций только для четных индексов
    position_sizes = []
    for i in range(0, len(entry_prices), 2):
        entry_price = entry_prices[i]
        deposit_percent = entry_prices[i + 1]   # Получаем процент депозита для текущей сделки
        entry_amount = deposit * (deposit_percent/100)  # Вычисляем размер депозита для текущей сделки
        position_size = calculate_position_size(position_type=position_type, D=entry_amount, PE=entry_price, PL=stop_loss_price, R=risk_percent)
        position_sizes.append(position_size)
        # print(f"Trade {i//2 + 1}: {position_type}, Deposit: {entry_amount}, Entry Price: {entry_price}, Stop Loss Price: {stop_loss_price}, Risk Percent: {risk_percent}")

    if position_sizes:
        position_sizes_rounded = [round(size, 8) for size in position_sizes]
        sizes_str = '\n'.join([f"Position {i + 1}: {size}" for i, size in enumerate(position_sizes_rounded)])
        await message.answer(f'💰Position sizes:\n\n{message.text}\n\n<b>{sizes_str}</b>\n', parse_mode="HTML")

    else:
        await message.answer("Error occurred during position size calculation.")










