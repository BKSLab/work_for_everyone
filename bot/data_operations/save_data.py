import logging
from typing import Union

from database.models import (
    Applicant,
    Favorites,
    Region,
    Vacancy,
    VacancyMSK,
    VacancySPB,
    db_work_for_everyone
)
from peewee import PeeweeException


logger_data_operations = logging.getLogger(__name__)


def saving_region_data(data_region: list[dict[str, str]]) -> dict:
    """Функция сохранения данных о регионах в таблице region."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()

        result = Region.insert_many(data_region).execute()
        return {'status': True, 'count_rows': len(result)}
    except PeeweeException as error:
        text_error = (
            'При попытке сохранить данные о регионах в таблице region '
            f'произошла ошибка. Текст ошибки: {error}. '
            f'Тип ошибки: {type(error).__name__}.'
        )
        logger_data_operations.exception(text_error)
        return {'status': False, 'error': text_error}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def saving_vacancies_big_data(
    data_vacancies: list[dict], model: VacancyMSK | VacancySPB | Vacancy
) -> dict:
    """Сохранение данных о вакансиях в пользовательской локации."""

    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        model.insert_many(data_vacancies).execute()
        return {'status': True}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке сохранить данных о вакансиях в таблицу для '
            f'модели {model} произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def saving_applicant_data(
    data: dict[str, str | int]
) -> dict[str, bool | Applicant]:
    """Сохранение данных пользователя (соискателя)."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        instance, _ = Applicant.get_or_create(
            name_applicant=data.get('name_applicant'),
            user_tg_id=str(data.get('user_tg_id')),
            region=Region.get(Region.region_code == data.get('region_code')),
            location=data.get('location'),
        )
        return {'status': True, 'instance': instance}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке сохранить данные о пользователе произошла ошибка'
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def saving_vacancy_favorites(
    vacancy_instance: Union[Vacancy, VacancyMSK, VacancySPB], user_tg_id: str
) -> dict:
    """Сохранение вакансии в избранном."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        instance, _ = Favorites.get_or_create(
            vacancy_name=vacancy_instance.vacancy_name,
            applicant_tg_id=str(user_tg_id),
            salary=vacancy_instance.salary,
            vacancy_source=vacancy_instance.vacancy_source,
            vacancy_url=vacancy_instance.vacancy_url,
            employer_name=vacancy_instance.employer_name,
            employer_location=vacancy_instance.employer_location,
            employer_phone_number=vacancy_instance.employer_phone_number,
            company_code=vacancy_instance.company_code,
            vacancy_id=vacancy_instance.vacancy_id,
        )
        return {'status': True, 'instance': instance}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке сохранить данные в избранном произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()
