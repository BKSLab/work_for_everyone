import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from config_data.config import load_config
from database.views import check_table_region_and_data_exists
from handlers import applicant_handlers, other_handlers


async def main() -> None:
    config = load_config()

    check_table_region_and_data_exists()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=config.tg_bot.storage)

    dp.include_routers(applicant_handlers.router, other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename=(Path(__file__) / 'main.log').name,
        format=('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'),
        encoding='utf-8',
    )
    asyncio.run(main())
