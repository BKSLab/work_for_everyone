import asyncio

from aiogram import Bot, Dispatcher

from config_data.config import load_config


async def main() -> None:
    # загрузка конфигурации бота
    config = load_config()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    dp = Dispatcher(storage=config.tg_bot.storage)
    # регистрация роутеров в диспетчере
    # dp.include_router(user_handlers.router)
    # dp.include_router(other_handlers.router)

    # пропускаем накопивщиеся апдейты и запускаем пуллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
