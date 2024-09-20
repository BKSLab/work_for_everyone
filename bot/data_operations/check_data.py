import logging

from database.models import (
    Favorites,
    Region,
    VacancyMSK,
    VacancySPB,
    db_work_for_everyone
)
from peewee import PeeweeException


logger_data_operations = logging.getLogger(__name__)


def region_data_exists() -> dict:
    """Функция проверки наличия данных о регионах в таблице region."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()

        query_result = Region.get_or_none()
        if query_result:
            text_msg = 'Таблице region содержит данные о регионах.'
            logger_data_operations.info(text_msg)
            return {'status': True, 'data_exists': True, 'text_msg': text_msg}
        logger_data_operations.info(
            'В таблице region отсутствуют данные о регионах.'
        )
        return {'status': True, 'data_exists': False}
    except PeeweeException as error:
        text_error = (
            'При обращении к таблице region произошла ошибка.'
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        logger_data_operations.exception(text_error)
        return {'status': False, 'error': text_error}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def check_vacancy_favorites_exists(
    vacancy_id: str, user_tg_id: int
) -> dict:
    """Проверка наличия вакансии в избранном."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        result = (
            Favorites.select()
            .where(
                Favorites.vacancy_id == vacancy_id,
                Favorites.applicant_tg_id == user_tg_id,
            )
            .exists()
        )
        return {'status': True, 'check_status': result}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При обращении к таблицы с вакансиями, добавленными в избранное '
            f'произошла ошибка. Текст ошибки: {error}. '
            f'Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def check_vacancy_msk_spb_exists() -> dict:
    """
    Функция проверки наличия данных о загруженных вакансиях
    в Москве и Санкт-Петербурге на момент старта бота в БД.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()

        query_result_msk = VacancyMSK.get_or_none()
        query_result_spb = VacancySPB.get_or_none()

        if query_result_msk and query_result_spb:
            text_msg = (
                'Вакансии в Москве и Санкт-Петербурге при старте бота '
                'уже загружены в БД.'
            )
            logger_data_operations.info(text_msg)
            return {'status': True, 'data_exists': True, 'text_msg': text_msg}
        text_msg = (
            'Вакансии в Москве и Санкт-Петербурге при старте бота '
            'отсутствуют. Требуется их загрузка для нормальной работы бота.'
        )
        logger_data_operations.info(text_msg)
        return {'status': True, 'data_exists': False, 'text_msg': text_msg}
    except PeeweeException as error:
        text_error = (
            'При обращении к таблице с вакансиям в Москве и Санкт-Петербурге '
            f'произошла ошибка. Текст ошибки: {error}. '
            f'Тип ошибки: {type(error).__name__}.'
        )
        logger_data_operations.exception(text_error)
        return {'status': False, 'error': text_error}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()
