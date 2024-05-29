import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram import types
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, Message, CallbackQuery

from ConfigData.config import Config, load_config, allowed_admin_ids
from Handlers.change_strategy import new_strategy_router
from Lexicon.commands_ru import commands_ru
from Lexicon.commands_eng import commands_eng
from Handlers.spot_position import spot_position_eng
from Handlers.futures_position_handler_eng import calc_router_eng
from Handlers.admin_add_user import add_user
from Handlers.admin_delete_user import delete_user
from Handlers.signals_eng import signal_router_eng

from Keyboards.choose_admin_add_delete import admin_add_delete
from Keyboards.choose_user_calculator_signal import user_calc_sig
from Keyboards.futures_spot import user_futures_spot

# Инициализация логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция настройки логирования в файл
def setup_logging():
    file_handler = logging.FileHandler(filename='bot_log.txt', mode='w')
    formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# Конфигурация логирования и запуск бота
async def main():
    # Конфигурация логирования
    setup_logging()
    logger.info('Bot started')

    # Загрузка конфигурации в переменную
    config: Config = load_config()

    storage = MemoryStorage()
    # Инициализация бота и диспатчера
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher(storage=storage)

    # Регистрация роутера в диспатчере
    #dp.include_router(calc_router_ru)
    dp.include_router(add_user)
    dp.include_router(calc_router_eng)
    dp.include_router(spot_position_eng)
    dp.include_router(delete_user)
    dp.include_router(signal_router_eng)
    dp.include_router(new_strategy_router)

    # Список с командами бота и их описание
    main_menu_commands = [
        BotCommand(command='/start', description='Start the bot'),
        BotCommand(command='cancel', description='Сancellation of the action'),
        # BotCommand(command='/change_strategy', description='Change the selected strategy'),
        BotCommand(command='/help_eng', description='Information about the work of the bot')

    ]

    await bot.set_my_commands(main_menu_commands)

    @dp.message(CommandStart(), StateFilter(default_state))
    async def process_start_command(message: Message):
        user_id = message.from_user.id
        if user_id in allowed_admin_ids:
            await message.answer(
                text='🔐 You have entered the administrator mode', reply_markup=admin_add_delete()
            )
            await message.delete()
        else:
            await message.answer(text=commands_eng['/start'], reply_markup=user_calc_sig())
            await message.delete()

    @dp.callback_query(StateFilter(default_state), F.data == 'calc')
    async def calc_or_signal(callback: CallbackQuery):
        await callback.message.answer(
           text='Select an action', reply_markup=user_futures_spot()
        )
        await callback.message.delete()

    @dp.message(Command(commands='cancel'), StateFilter(default_state))
    async def process_cancel_command(message: Message):
        await message.answer(
            text=commands_ru['/cancel_none']
        )

    @dp.message(Command(commands='cancel'), ~StateFilter(default_state))
    async def process_cancel_command_state(message: Message, state: FSMContext):
        await message.answer(
            text=commands_ru['/cancel'])
        await state.clear()

    @dp.message(Command(commands='help_ru'))
    async def process_help_ru_command(message: Message):
        await message.answer(text=commands_ru['/help_me_ru'])

    @dp.message(Command(commands='help_eng'))
    async def process_help_eng_command(message: Message):
        await message.answer(text=commands_eng['/help_me_eng'])


    # Пропуск апдейтов и запуск пулинга
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f'An error occurred: {e}')
