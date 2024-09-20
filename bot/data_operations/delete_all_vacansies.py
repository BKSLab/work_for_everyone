import logging

from database.models import Vacancy, db_work_for_everyone
from peewee import PeeweeException


logger_data_operations = logging.getLogger(__name__)


def delete_all_vacansies_from_vacancy_table() -> dict:
    """
    Полное удаление данных о вакансиях.
    Удаление происходит по рассписанию, один раз в сутки.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        if Vacancy.get_or_none() is None:
            text = (
                'Таблица vacancy на момент удаления была пуста.'
            )
            logger_data_operations.info(text)
        else:
            count_deleted_records = Vacancy.delete().execute()
            text = (
                f'Данные удалены. Удалено {count_deleted_records} записей.'
            )
            logger_data_operations.info(text)
        return {'status': True, 'text': text}
    except PeeweeException as error:
        text_error = (
            'При удалении данных из таблицы vacancy произошла ошибка.'
            f'произошла ошибка. Текст ошибки: {error}. '
            f'Тип ошибки: {type(error).__name__}.'
        )
        logger_data_operations.exception(text_error)
        return {'status': False, 'error': text_error}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()
