import logging
from peewee import PeeweeException

from database.models import (
    Applicant,
    Favorites,
    Region,
    Vacancy,
    VacancyMSK,
    VacancySPB,
    db_work_for_everyone,
)


logger_database = logging.getLogger(__name__)


def create_tables_if_not_exists() -> dict:
    """
    Функция создания таблиц в базе данных. Таблицы будут созданы,
    после проверки их отсутствия в БД.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        tables = db_work_for_everyone.get_tables()
        if not tables:
            db_work_for_everyone.create_tables(
                [Region, Applicant, Vacancy, VacancyMSK, VacancySPB, Favorites]
            )
            text_msg = (
                'Таблицы для моделей Region, Applicant, Vacancy, VacancyMSK, '
                'VacancySPB, Favorites успешно созданы в БД'
            )
            logger_database.info(text_msg)
            return {'status': True, 'text_msg': text_msg}
        text_msg = (
            'Таблицы для моделей Region, Applicant, '
            'Vacancy, Favorites ранее уже были созданы в БД'
        )
        logger_database.info(text_msg)
        return {'status': True, 'text_msg': text_msg}
    except PeeweeException as error:
        text_msg = (
            'При создании таблиц в БД произошла ошибка.'
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        logger_database.exception(text_msg)
        return {'status': False, 'error': text_msg}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()
