import logging
from peewee import PeeweeException
from typing import Union

from database.models import (
    VacancyMSK,
    VacancySPB,
    db_work_for_everyone,
)


logger_data_operations = logging.getLogger(__name__)


def get_count_vacancies_msk_spb(
    vacancy_source: str, model: VacancyMSK | VacancySPB
) -> dict:
    """
    Подсчет количества сохраненных вакансий в Москве и Санкт-Петербурге
    с сайта hh.ru и Работа России.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        count_vacancies = (
            model.select()
            .where(model.vacancy_source == vacancy_source)
            .count()
        )
        return {'status': True, 'count_vacancies': count_vacancies}
    except PeeweeException as error:
        logger_data_operations.exception(
            f'При отправке запроса к таблице модели {model} произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_one_vacancy_msk_spb(
    model: Union[VacancyMSK, VacancySPB], vacancy_id: str
) -> dict:
    """Проверка наличия вакансии в Москве или Санкт-Петербурге."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        vacancy = model.get_or_none(
            model.vacancy_id == vacancy_id,
        )
        return {'status': True, 'vacancy': vacancy}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке отправить запрос на получение одной вакансии, '
            'произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_vacancies_by_keyword_msk_spb(
    model: Union[VacancyMSK, VacancySPB], keyword: str
) -> dict:
    """
    Получение вакансий в Москве или Санкт-Петербурге
    пользователя по ключевому слову.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        vacancies = model.select().where(
            model.vacancy_name.contains(keyword)
        ).order_by(model.vacancy_source.desc())
        return {'status': True, 'vacancies': vacancies}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке отправить запрос на получение вакансий, '
            'найденных по ключевому слову произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_count_vacancies_by_keyword_msk_spb(
    model: Union[VacancyMSK, VacancySPB], keyword: str
) -> dict:
    """
    Подсчет количества найденных в Москве или Санкт-Петербурге
    вакансий по ключевому слову.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        count_vacancies = (
            model.select()
            .where(model.vacancy_name.contains(keyword))
        ).count()

        return {'status': True, 'count_vacancies': count_vacancies}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке отправить запрос на получение количества '
            'вакансий, найденных по ключевому слову произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_ten_vacancies_by_keyword_msk_spb(
    model: Union[VacancyMSK, VacancySPB], page_number: int, keyword: str
) -> dict:
    """
    Получение по десять вакансий найденных в Москве и Санкт-Петербурге
    по ключевому слову для показа пользователю.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        vacancies_by_keyword = (
            model.select()
            .where(
                model.vacancy_name.contains(keyword)
            )
            .order_by(model.vacancy_source.desc())
            .paginate(page_number, 10)
        )
        return {'status': True, 'vacancies_by_keyword': vacancies_by_keyword}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке отправить запрос на получение десяти вакансий, '
            'найденных по ключевому слову произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_count_many_vacancies_msk_spb(
    model: Union[VacancyMSK, VacancySPB]
) -> dict:
    """
    Подсчет количества найденных в Москве или Санкт-Петербурге вакансий.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        count_vacancies = (model.select()).count()
        return {'status': True, 'count_vacancies': count_vacancies}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке отправить запрос на получение количества '
            'вакансий произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_ten_vacancies_msk_spb(
    model: Union[VacancyMSK, VacancySPB], page_number: int
) -> dict:
    """
    Получение по десять вакансий найденных в Москве и Санкт-Петербурге
    по ключевому слову для показа пользователю.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        ten_vacancies = (
            model.select().order_by(
                model.vacancy_source.desc()
            ).paginate(page_number, 10)
        )
        return {'status': True, 'ten_vacancies': ten_vacancies}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При попытке отправить запрос на получение десяти вакансий, '
            'произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()
