import logging
from peewee import PeeweeException

from database.models import (
    Favorites,
    Vacancy,
    VacancyMSK,
    VacancySPB,
    db_work_for_everyone,
)


logger_data_operations = logging.getLogger(__name__)


# оставляем ошибки
def delete_vacancies_msk_spb() -> dict:
    """
    Полное удаление данных о вакансиях в Москве и Санкт-Петербурге,
    перед загрузкой свежих вакансий.
    Удаление происходит по рассписанию, один раз в сутки.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        count_deleted_records_msk = VacancyMSK.delete().execute()
        count_deleted_records_spb = VacancySPB.delete().execute()
        return {
            'status': True,
            'count_msk': count_deleted_records_msk,
            'count_spb': count_deleted_records_spb,
        }
    except PeeweeException as error:
        text_error = (
            'При попытке удалить данные о ранее загруженных вакансиях '
            'в Москве и Санкт-Петербурге произошла ошибка'
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        logger_data_operations.exception(text_error)
        return {'status': False, 'error': text_error}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def deleting_vacancy_user_location(
    user_tg_id: str, vacancy_source: str
) -> dict:
    """
    Удаление данных о вакансиях, оставшихся после
    предыдущего запроса пользователя.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()

        Vacancy.delete().where(
            (Vacancy.applicant_tg_id == user_tg_id)
            & (Vacancy.vacancy_source == vacancy_source)
        ).execute()

        return {'status': True}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке удалить данные о ранее загруженных вакансиях '
            'в пользовательской локации произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def delete_vacancy_from_favorites(
    vacancy_id: str, user_tg_id: str, vacancy_source: str
) -> dict:
    """Удаление вакансии из избранного."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()

        Favorites.delete().where(
            Favorites.vacancy_id == vacancy_id,
            Favorites.applicant_tg_id == user_tg_id,
            Favorites.vacancy_source == vacancy_source,
        ).execute()

        return {'status': True}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке удалить данные о ранее загруженных вакансиях '
            'в пользовательской локации произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()
