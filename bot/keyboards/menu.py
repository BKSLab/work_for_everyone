from aiogram import Bot
from aiogram.types import BotCommand
from phrases.texts_for_bot_buttons import ButtonData


async def set_main_menu(bot: Bot):
    """ "Функция для создания основного меню бота."""
    main_menu_commands = [
        BotCommand(command=data[0], description=data[1])
        for data in ButtonData.commands_data
    ]
    await bot.set_my_commands(main_menu_commands)
