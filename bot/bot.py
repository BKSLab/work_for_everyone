import asyncio
import logging
from pathlib import Path

from administration.administration import main_administration
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config_data.config import ADMIN_USER_ID, load_config
from data_operations.management_save_data_regions import (
    management_saving_data_regions,
)
from database.create_db import create_db
from database.create_tables import create_tables_if_not_exists
from handlers import (commands_handlers, favorites_handlers, main_handlers,
                      msk_spb_handlers, other_handlers,
                      search_by_keyword_handlers,
                      search_by_keyword_msk_spb_handlers)
from keyboards.menu import set_main_menu
from loading_vacancies.load_manage_vacancies import \
    loading_management_vacancies_msk_spb


async def main() -> None:
    config = load_config()
    create_db()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=config.tg_bot.storage)

    # Функция создания таблиц в БД, необходимых для работы
    result_operation = create_tables_if_not_exists()
    if not result_operation.get('status'):
        text_msg = result_operation.get('error')
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text_msg)
    else:
        text_msg = result_operation.get('text_msg')
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text_msg)
    # Добавление данных о регионах в таблицу Region в ДБ
    result_recording = management_saving_data_regions()
    if not result_recording.get('status'):
        text_msg = result_recording.get('error')
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text_msg)
    else:
        text_msg = result_recording.get('text_msg')
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text_msg)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        main_administration,
        CronTrigger(day_of_week='*', minute=30),
        # CronTrigger(day_of_week='*', hour=23),
        args=(bot,),
    )
    scheduler.add_job(
        loading_management_vacancies_msk_spb,
        CronTrigger(day_of_week='*', minute=32),
        # CronTrigger(day_of_week='*', hour=4, minute=11),
        args=(bot,),
    )
    scheduler.start()

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


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        # filename=(Path(__file__) / 'main.log').name,
        format=('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'),
        handlers=[
            logging.FileHandler(Path(__file__).with_name('main.log')),
            logging.StreamHandler(),
        ],
        # filemode='w',
        encoding='utf-8',
    )
    # logging.basicConfig(
    #     level=logging.INFO,
    #     filename=(Path(__file__) / 'main.log').name,
    #     format=('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'),
    #     filemode='w',
    #     encoding='utf-8',
    # )
    try:
        asyncio.run(main())
        logging.info('Функция начала работу.')
    except Exception as error:
        logging.critical(
            f'Failed to run the main function: {error}', exc_info=True
        )
