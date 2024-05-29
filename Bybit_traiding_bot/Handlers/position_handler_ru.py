from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StatesGroup, State, StateFilter

from Function.calculate_position import calculate_position_size
from Keyboards.currency_pair import type_position


calc_router_ru: Router = Router()

user_dict = {}


class InputClientInfo(StatesGroup):
    type_position = State()  # Выбор позиции
    entry_price = State()  # Цена входа в позицию. Это цена, по которой трейдер планирует войти в позицию.
    stop_loss_price = State()  # Цена выхода из позиции при убытке
    deposit = State()  # Размера депозита
    risk_percentage = State()  # Процент риска


@calc_router_ru.callback_query(StateFilter(default_state), F.data == 'futures')
async def process_input_currency(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Выберете позицию в которую будете входить', reply_markup=type_position()
    )
    await state.set_state(InputClientInfo.type_position)


@calc_router_ru.callback_query(StateFilter(InputClientInfo.type_position),
                               F.data.in_(['short', 'long']))
async def process_typy_position(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type_position=callback.data)
    await callback.message.delete()
    await callback.message.answer(
        text='📝 Пожалуйста, введите число для цены входа в позицию 💹\n\n'
    )
    await state.set_state(InputClientInfo.entry_price)


@calc_router_ru.message(StateFilter(InputClientInfo.entry_price), lambda message: message.text.replace('.', '', 1).isdigit())
async def process_entry_price(message: Message, state: FSMContext):

    if '.' in message.text:
        entry_price = float(message.text)
    else:
        entry_price = int(message.text)

    await state.update_data(entry_price=entry_price)
    await message.answer(
        text=f'💰 Цена входа вы указали {entry_price}\n\n'
    )
    await message.answer(
        text='📝 Пожалуйста, введите число для цены выхода из позиции 💹\n\n'
             '❓ Цена выхода из позиции (стоп-лосс) определяет ваш потенциальный убыток, '
             'если сделка завершится неудачно. При анализе цены выхода учтите уровни сопротивления/поддержки, '
             'а также свою стратегию управления рисками.'
    )
    await state.set_state(InputClientInfo.stop_loss_price)


@calc_router_ru.message(StateFilter(InputClientInfo.entry_price))
async def process_bad_entry(message: Message):
    await message.answer(
        text='❌ Введенное значение не является целым числом или с плавающей точкой(дробным)\n\n'
             'Пример:✅ 1000, 2.3\n'
             'Пример: ❌ сто, 66,66\n\n'
             '🚫 Если передумали, то введите /cancel'
    )


@calc_router_ru.message(StateFilter(InputClientInfo.stop_loss_price), lambda message: message.text.replace('.', '', 1).isdigit())
async def process_good_stop_loss(message: Message, state: FSMContext):
    if '.' in message.text:
        stop_loss = float(message.text)
    else:
        stop_loss = int(message.text)

    await state.update_data(stop_loss_price=stop_loss)
    await message.answer(
        text=f'💰 Цену выхода вы указали {message.text}\n\n'
    )
    await message.answer(
        text='💰 Пожалуйста, введите сумму депозита в виде целого числа 💰\n\n'
             '❓ Сумма депозита влияет на вашу торговую стратегию и уровень риска. '
             'Это важный параметр, который следует тщательно рассматривать при принятии решений о торговле. '
             'Убедитесь, что ваш риск соответствует вашим финансовым возможностям и торговой стратегии.'
    )
    await state.set_state(InputClientInfo.deposit)


@calc_router_ru.message(StateFilter(InputClientInfo.stop_loss_price))
async def process_bad_stop_loss(message: Message):
    await message.answer(
        text='❌ Введенное значение не является целым числом или с плавающей точкой(дробным)\n\n'
             'Пример:✅ 1000, 2.3\n'
             'Пример: ❌ сто, 66,66\n\n'
             '🚫 Если передумали, то введите /cancel'
    )


@calc_router_ru.message(StateFilter(InputClientInfo.deposit), lambda x: int(x.text))
async def process_good_deposit(message: Message, state: FSMContext):
    await state.update_data(deposit=int(message.text))
    await message.answer(
        text=f'💰 Сумма депозита: {message.text} 💰'
    )
    await message.answer(
        text='📈 Пожалуйста, введите % риска от 1 до 100 📈\n\n'
             '❓ Процент риска определяет, сколько процентов от вашего депозита вы готовы потерять в одной сделке. '
             'Это ключевой параметр для управления вашими инвестициями и контроля за потерями. '
             'Выберите процент риска, который соответствует вашему уровню комфорта и вашей торговой стратегии.'
    )
    await state.set_state(InputClientInfo.risk_percentage)


@calc_router_ru.message(StateFilter(InputClientInfo.deposit))
async def process_bad_deposit(message: Message):
    await message.answer(
        text='❌ Введенное значение не является числом\n\n'
             '🚫 Если передумали, то введите /cancel'
    )


@calc_router_ru.message(StateFilter(InputClientInfo.risk_percentage), lambda x: int(x.text) and 1 <= int(x.text) <= 100)
async def process_good_risk(message: Message, state: FSMContext):
    await state.update_data(risk_percentage=int(message.text))
    await message.answer(
        text=f'📈 Процент риска: {message.text} % 📈'
    )

    await message.answer(
        text='🎉 Все данные введены!'
    )
    user_dict = await state.get_data()
    await message.answer(f'Тип позиции: {user_dict["type_position"]}\n'
                         f'💰 Цена входа: {user_dict["entry_price"]}\n'
                         f'💰 Цена выхода: {user_dict["stop_loss_price"]}\n'
                         f'💰 Депозит: {user_dict["deposit"]}\n'
                         f'📈 Процент риска: {user_dict["risk_percentage"]} %\n'
                         )
    position_volume = calculate_position_size(position_type=user_dict["type_position"],
                                              D=user_dict["deposit"],
                                              PE=user_dict["entry_price"],
                                              PL=user_dict["stop_loss_price"],
                                              R=user_dict["risk_percentage"])
    await message.answer(
        text=f"Объем позиции: {position_volume}\n\n"
             f"Для нового расчета воспользуйтесь командой /cancel")
