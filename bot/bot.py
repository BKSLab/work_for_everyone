import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from config_data.config import load_config
from handlers import applicant_handlers, other_handlers


async def main() -> None:
    # загрузка конфигурации бота
    config = load_config()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=config.tg_bot.storage)

    # регистрация роутеров в диспетчере
    dp.include_routers(applicant_handlers.router, other_handlers.router)
    # dp.include_router(applicant_handlers.router)
    # dp.include_router(other_handlers.router)

    # пропускаем накопивщиеся апдейты и запускаем пуллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename=(Path(__file__) / 'main.log').name,
        format=('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s'),
        encoding='utf-8',
    )
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
