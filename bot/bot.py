import asyncio
import logging
from pathlib import Path

from administration.administration import main_administration
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config_data.config import load_config
from data_operations.management_save_data_regions import (
    management_saving_data_regions,
)
from database.create_db import create_db
from database.create_tables import create_tables_if_not_exists
from handlers import (
    commands_handlers,
    favorites_handlers,
    main_handlers,
    msk_spb_handlers,
    other_handlers,
    search_by_keyword_handlers,
    search_by_keyword_msk_spb_handlers
)
from keyboards.menu import set_main_menu
from loading_vacancies.load_manage_vacancies import (
    loading_management_vacancies_msk_spb,
    loading_management_vacancies_msk_spb_on_start_bot
)


config = load_config()


def init_bot_and_dispatcher() -> tuple[Bot, Dispatcher]:
    """Функция инициализации объектов бота и диспетчера."""
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=config.tg_bot.storage)
    return bot, dp


async def initialize_database(bot: Bot) -> None:
    """Функция создания БД и таблиц, если они не созданы."""
    result_creation = create_db()
    if not result_creation.get('status'):
        text_msg = result_creation.get('error')
        await bot.send_message(chat_id=config.app.admin_user_id, text=text_msg)
    else:
        text_msg = result_creation.get('text_msg')
        await bot.send_message(chat_id=config.app.admin_user_id, text=text_msg)

    result_operation = create_tables_if_not_exists()
    if not result_operation.get('status'):
        text_msg = result_operation.get('error')
        await bot.send_message(chat_id=config.app.admin_user_id, text=text_msg)
    else:
        text_msg = result_operation.get('text_msg')
        await bot.send_message(chat_id=config.app.admin_user_id, text=text_msg)


async def add_region_data(bot: Bot) -> None:
    """Функция добавления данных о регионах в БД."""
    result_recording = management_saving_data_regions()
    if not result_recording.get('status'):
        text_msg = result_recording.get('error')
        await bot.send_message(chat_id=config.app.admin_user_id, text=text_msg)
    else:
        text_msg = result_recording.get('text_msg')
        await bot.send_message(chat_id=config.app.admin_user_id, text=text_msg)


def setup_scheduler(bot: Bot) -> None:
    """Функция настройки планировщика задач."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        main_administration,
        CronTrigger(day_of_week='*', hour=0, minute=5),
        args=(bot,),
    )
    scheduler.add_job(
        loading_management_vacancies_msk_spb,
        CronTrigger(day_of_week='*', hour=0),
        args=(bot,),
    )
    scheduler.start()


async def setup_dispatcher_and_start_bot(dp: Dispatcher, bot: Bot) -> None:
    """Функция настройки обработчиков команд и запуска пуллинга бота."""
    dp.include_routers(
        commands_handlers.router,
        main_handlers.router,
        msk_spb_handlers.router,
        search_by_keyword_handlers.router,
        search_by_keyword_msk_spb_handlers.router,
        other_handlers.router,
        favorites_handlers.router,
    )
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main() -> None:
    """Основная функция запуска процессов."""
    bot, dp = init_bot_and_dispatcher()

    await initialize_database(bot=bot)
    await add_region_data(bot=bot)
    await loading_management_vacancies_msk_spb_on_start_bot(bot=bot)

    setup_scheduler(bot=bot)

    await setup_dispatcher_and_start_bot(dp=dp, bot=bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'),
        handlers=[
            logging.FileHandler(Path(__file__).with_name('main.log')),
            logging.StreamHandler(),
        ],
        encoding='utf-8',
    )
    try:
        asyncio.run(main())
        logging.info('Функция начала работу.')
    except Exception as error:
        logging.critical(
            f'Failed to run the main function: {error}', exc_info=True
        )
