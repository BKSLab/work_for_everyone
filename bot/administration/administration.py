import logging
import os

from aiogram import Bot
from aiogram import exceptions
from aiogram.types import FSInputFile
from data_operations.get_data import (
    get_count_applicants,
    get_count_favorites
)
from config_data.config import load_config
from data_operations.delete_all_vacansies import (
    delete_all_vacansies_from_vacancy_table
)


logger_admin = logging.getLogger(__name__)
config = load_config()


async def send_logs_to_admin(bot: Bot):
    """Отправка файла с логами администратору бота."""
    try:
        document = FSInputFile(os.path.join(config.app.base_dir, 'main.log'))
        text_msg = 'Файл с логами для анализа работы бота.'
        await bot.send_document(
            config.app.admin_user_id, document, caption=text_msg
        )
    except exceptions.TelegramAPIError as error:
        error_msg = (
            f'Не удалось отправить файл с логами.\n'
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        logger_admin.error(error_msg)
        await bot.send_message(config.app.admin_user_id, error_msg)
    except Exception as error:
        error_msg = (
            'Произошла неожиданная ошибка при отправке файла с логами\n'
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        logger_admin.error(error_msg)
        await bot.send_message(config.app.admin_user_id, error_msg)


async def main_administration(bot: Bot) -> None:
    """Главная функция для администрирования работы бота."""
    lst_functions: list[dict] = [
        delete_all_vacansies_from_vacancy_table(),
        get_count_applicants(),
        get_count_favorites(),
    ]
    for func in lst_functions:
        query_result = func
        if not query_result.get('status'):
            text_msg = query_result.get('error')
            await bot.send_message(
                chat_id=config.app.admin_user_id, text=text_msg
            )
        else:
            text_msg = query_result.get('text')
            await bot.send_message(
                chat_id=config.app.admin_user_id, text=text_msg
            )
    await send_logs_to_admin(bot=bot)
