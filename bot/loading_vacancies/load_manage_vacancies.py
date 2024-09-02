import asyncio
import logging

from aiogram import Bot
from loading_vacancies.load_vacancies_hh import (
    load_vacancy_from_hh_msk,
    load_vacancy_from_hh_spb,
    load_vacancy_user_location_hh
)
from loading_vacancies.load_vacancies_trudvsem import (
    load_vacancy_from_trudvsem_msk,
    load_vacancy_from_trudvsem_spb,
    load_vacancy_trudvsem_user_location
)
from config_data.config import ADMIN_USER_ID
from data_operations.delete_data import delete_vacancies_msk_spb
from database.models import Applicant


logger_load_msk_spb = logging.getLogger(__name__)


async def loading_management_vacancies_msk_spb(bot: Bot):
    """
    Функция управления загрузкой данных о вакансиях
    в Москве и Санкт-Петербурге. После загрузки данных
    администратору Telegram бота будет направлено сообщение
    о том, что данные успешно загружены и сохранены в БД.
    При возникновении ошибок, администратор получит соответствующее
    сообщение на свой аккаунт в Telegram.
    """

    # Удаление вакансий в БД
    delete_result = delete_vacancies_msk_spb()
    if not delete_result.get('status'):
        text = delete_result.get('error')
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text)
    if delete_result.get('status'):
        text = (
            'Данные о вакансиях из таблиц vacancy_spb и vacancy_msk '
            'удалены успешно. Всего удалено:\n\n'
            f'Удалено вакансий в Москве: {delete_result.get("count_msk")}\n'
            'Удалено вакансий в Санкт-Петербурге: '
            f'{delete_result.get("count_spb")}'
        )
        logger_load_msk_spb.info(text)
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text)

    # загрузка и сохранение данных о вакансиях в Москве с сайта hh.ru
    hh_msk_result = load_vacancy_from_hh_msk()

    # Отправка администратору бота сообщение о сбое в работе
    # при загрузки и сохранении данных о вакансиях в Москве
    if not hh_msk_result.get('status'):
        text = (
            'При загрузке данных о вакансиях с сайта hh.ru в Москве в '
            'таблицу vacancy_msk произошла ошибка.'
        )
        logger_load_msk_spb.info(text)
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text)

    # Отправка сообщения администратору бота и логирование в случае,
    # когда все данные о вакансиях в Москве были загружены и сохранены в БД
    if hh_msk_result.get('status'):
        text = (
            'Данные о вакансиях в Москве успешно загружены с сайта hh.ru '
            'и сохранены в таблице vacancy_msk. Всего сохранено: '
            f'{hh_msk_result.get("count_vacancy_msk")} '
        )
        logger_load_msk_spb.info(text)
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text)

    await asyncio.sleep(delay=5)
    # загрузка и сохранение данных о вакансиях в Санкт_петербурге с сайта hh.ru
    hh_spb_result = load_vacancy_from_hh_spb()

    # Отправка администратору бота сообщение о сбое в работе
    # при загрузки и сохранении данных о вакансиях в Санкт-Петербурге
    if not hh_spb_result.get('status'):
        text = (
            'При загрузке данных о вакансиях с сайта hh.ru в Санкт-Петербурге '
            'в таблицу vacancy_spb произошла ошибка.'
        )
        logger_load_msk_spb.info(text)
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text)

    # Отправка сообщения администратору бота и логирование в случае,
    # когда все данные о вакансиях в Санкт-Петербурге были
    # загружены и сохранены в БД
    if hh_spb_result.get('status'):
        text = (
            'Данные о вакансиях в Санкт-Петербурге успешно загружены '
            'с сайта hh.ru и сохранены в таблице vacancy_spb. '
            f'Всего сохранено: {hh_spb_result.get("count_vacancy_spb")} '
        )
        logger_load_msk_spb.info(text)
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text)

    # загрузка и сохранение данных о вакансиях в Москве с сайта trudvsem.ru
    trudvsem_msk_result = load_vacancy_from_trudvsem_msk()

    # Отправка администратору бота сообщение о сбое в работе
    # при загрузки и сохранении данных о вакансиях в Москве
    if not trudvsem_msk_result.get('status'):
        text = (
            'При загрузке данных о вакансиях с сайта trudvsem.ru в Москве в '
            'таблицу vacancy_msk произошла ошибка.'
        )
        logger_load_msk_spb.info(text)
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text)

    # Отправка сообщения администратору бота и логирование в случае,
    # когда все данные о вакансиях в Москве были загружены и сохранены в БД
    if trudvsem_msk_result.get('status'):
        text = (
            'Данные о вакансиях в Москве успешно загружены '
            'с сайта trudvsem.ru и сохранены в таблице vacancy_msk. '
            f'Всего сохранено: {trudvsem_msk_result.get("count_vacancy_msk")} '
        )
        logger_load_msk_spb.info(text)
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text)

    await asyncio.sleep(delay=5)
    trudvsem_spb_result = load_vacancy_from_trudvsem_spb()

    # Отправка администратору бота сообщение о сбое в работе
    # при загрузки и сохранении данных о вакансиях в Санкт-Петербурге
    if not trudvsem_spb_result.get('status'):
        text = (
            'При загрузке данных о вакансиях в с сайта trudvsem.ru '
            'Санкт-Петербургев таблицу vacancy_spb произошла ошибка.'
        )
        logger_load_msk_spb.info(text)
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text)

    # Отправка сообщения администратору бота и логирование в случае,
    # когда все данные о вакансиях в Санкт-Петербурге
    # были загружены и сохранены в БД
    if trudvsem_spb_result.get('status'):
        text = (
            'Данные о вакансиях в Санкт-Петербурге успешно загружены '
            'с сайта trudvsem.ru и сохранены в таблице vacancy_spb. '
            f'Всего сохранено: {trudvsem_spb_result.get("count_vacancy_spb")} '
        )
        logger_load_msk_spb.info(text)
        await bot.send_message(chat_id=ADMIN_USER_ID, text=text)


async def loading_management_vacancies_user_location(
    aplicant_instance: Applicant,
) -> dict:
    """
    Функция управления загрузкой и сохранением вакансий в пользовательской
    локации с сайта trudvsem.ru и hh.ru
    """
    trudvsem_user_location_result = await load_vacancy_trudvsem_user_location(
        reg_code_trudvsem=aplicant_instance.region.region_code,
        user_location=aplicant_instance.location,
        user_tg_id=aplicant_instance.user_tg_id,
    )
    if not trudvsem_user_location_result.get('status'):
        text = (
            'При загрузке данных о вакансиях с сайта trudvsem.ru в '
            'пользовательской локации произошла ошибка.'
        )
        logger_load_msk_spb.info(text)
        return {'status': False}

    # Информация о количестве вакансий, полученных от сайта trudvsem.ru
    count_vacancy_trudvsem = trudvsem_user_location_result.get('count_vacancy')

    hh_user_location_result = await load_vacancy_user_location_hh(
        reg_code_hh=aplicant_instance.region.region_code_hh,
        user_location=aplicant_instance.location,
        user_tg_id=aplicant_instance.user_tg_id,
    )
    if not hh_user_location_result.get('status'):
        text = (
            'При загрузке данных о вакансиях с сайта hh.ru в '
            'пользовательской локации произошла ошибка.'
        )
        logger_load_msk_spb.info(text)
        return {'status': False}

    # Информация о количестве вакансий, полученных от сайта hh.ru
    count_vacancy_hh = hh_user_location_result.get('count_vacancy')

    # Расчет общего количества найденных вакансий
    total_vacancies = count_vacancy_trudvsem + count_vacancy_hh

    return {
        'status': True,
        'total_vacancies': total_vacancies,
        'count_vacancy_trudvsem': count_vacancy_trudvsem,
        'count_vacancy_hh': count_vacancy_hh,
    }
