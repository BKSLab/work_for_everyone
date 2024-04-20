import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config_data.config import load_config
from database.create_db import create_db
from database.views import (
    check_table_region_and_data_exists,
    data_administration,
)
from handlers import applicant_handlers, other_handlers
from keyboards.menu import set_main_menu


async def main() -> None:
    config = load_config()
    create_db()
    check_table_region_and_data_exists()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=config.tg_bot.storage)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        data_administration,
        CronTrigger(day_of_week='*', hour=23),
        args=(bot,),
    )
    scheduler.start()

    dp.include_routers(applicant_handlers.router, other_handlers.router)
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename=(Path(__file__) / 'main.log').name,
        format=('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'),
        filemode='w',
        encoding='utf-8',
    )
    asyncio.run(main())
