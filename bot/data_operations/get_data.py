import logging
from datetime import datetime

from database.models import (
    Applicant,
    Favorites,
    Region,
    Vacancy,
    db_work_for_everyone
)
from peewee import PeeweeException

logger_data_operations = logging.getLogger(__name__)


def get_data_lst_regions(
    federal_district_code: str,
) -> dict:
    """
    Получение списка регионов заданного пользователем федерального округа.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        data = (
            Region.select(Region.region_name, Region.region_code)
            .where(Region.federal_district_code == federal_district_code)
            .order_by(Region.region_name)
            .tuples()
        )
        if data:
            return {
                'status': True,
                'data_regions': [region_data for region_data in data]
            }
        return {'status': False}
    except PeeweeException as error:
        logger_data_operations.exception(
            f'При отправке запроса к таблице region произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_count_vacancies_user_location(
    user_tg_id: str, vacancy_source: str
) -> dict:
    """Подсчет количества найденных в пользовательской локации вакансий."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        count_vacancies = (
            Vacancy.select()
            .where(
                (Vacancy.applicant_tg_id == user_tg_id)
                & (Vacancy.vacancy_source == vacancy_source)
            )
            .count()
        )
        return {'status': True, 'count_vacancies': count_vacancies}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При отправке запроса к таблице с информацией о вакансиях '
            'в пользовательской локации  произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_count_all_vacancies_user_location(user_tg_id: int) -> dict:
    """Получение вакансий пользователя в заданной локации."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        count_vacancies = (
            Vacancy.select()
            .where(Vacancy.applicant_tg_id == user_tg_id)
            .count()
        )
        return {'status': True, 'count_vacancies': count_vacancies}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При отправке запроса на получение количества вакансий '
            'к таблице с информацией о вакансиях в пользовательской '
            'локации  произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_all_vacancies_user_location(user_tg_id: int) -> dict:
    """
    Получение вакансий пользователя в заданной локации, если их меньше десяти.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        vacancies = Vacancy.select().where(
            Vacancy.applicant_tg_id == user_tg_id
        ).order_by(Vacancy.vacancy_source.desc())
        return {'status': True, 'vacancies': vacancies}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При отправке запроса на получение вакансий '
            'к таблице с информацией о вакансиях в пользовательской '
            'локации  произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_ten_vacancies(user_tg_id: int, page_number: int) -> dict:
    """Получение по десять вакансий для показа пользователю."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        vacancies = (
            Vacancy.select()
            .where(Vacancy.applicant_tg_id == user_tg_id)
            .order_by(Vacancy.vacancy_source.desc())
            .paginate(page_number, 10)
        )
        return {'status': True, 'ten_vacancies': vacancies}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При отправке запроса на получение десяти вакансий '
            'к таблице с информацией о вакансиях в пользовательской '
            'локации  произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_vacancies_from_favorites(user_tg_id: str) -> dict:
    """Получение вакансий добавленных в избранное."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        vacancies = Favorites.select().where(
            Favorites.applicant_tg_id == user_tg_id
        ).order_by(Favorites.vacancy_source.desc())
        return {'status': True, 'vacancies': vacancies}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При отправке запроса на получение вакансий, добавленных '
            'пользователем в избранное произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_one_vacancy_from_favorites(user_tg_id: str, vacancy_id: str) -> dict:
    """Получение одной вакансии добавленной в избранное."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        vacancy = Favorites.get_or_none(
            Favorites.vacancy_id == vacancy_id,
            Favorites.applicant_tg_id == user_tg_id,
        )
        return {'status': True, 'vacancy': vacancy}
    except PeeweeException as error:
        logger_data_operations.exception(
            'При отправке запроса на получение вакансий, добавленных '
            'пользователем в избранное произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_count_vacancies_by_keyword(user_tg_id: int, keyword: str) -> dict:
    """
    Подсчет количества найденных в пользовательской локации
    вакансий по ключевому слову.
    """
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        count_vacancies = (
            Vacancy.select()
            .where(
                (Vacancy.applicant_tg_id == user_tg_id)
                & (Vacancy.vacancy_name.contains(keyword))
            )
            .count()
        )
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


def get_vacancies_by_keyword(user_tg_id: int, keyword: str) -> dict:
    """Получение вакансий пользователя по ключевому слову."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        vacancies = Vacancy.select().where(
            (Vacancy.applicant_tg_id == user_tg_id)
            & (Vacancy.vacancy_name.contains(keyword))
        ).order_by(Vacancy.vacancy_source.desc())
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


def get_ten_vacancies_by_keyword(
    user_tg_id: int, page_number: int, keyword: str
) -> dict:
    """Получение по десять вакансий для показа пользователю."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        vacancies_by_keyword = (
            Vacancy.select()
            .where(
                (Vacancy.applicant_tg_id == user_tg_id)
                & (Vacancy.vacancy_name.contains(keyword))
            ).order_by(Vacancy.vacancy_source.desc())
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


def get_one_vacancy(vacancy_id: str, user_tg_id: int) -> dict:
    """Проверка наличия вакансии."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        vacancy = Vacancy.get_or_none(
            Vacancy.vacancy_id == vacancy_id,
            Vacancy.applicant_tg_id == user_tg_id,
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


def get_count_applicants() -> dict:
    """Подсчет количества пользователей."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        count_applicants = Applicant.select().count()
        unique_applicants = (
            Applicant.select(Applicant.user_tg_id).distinct().count()
        )
        time_select = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        text = (
            f'По состоянию на {time_select} общее количество пользователей, '
            f'которые воспользовались ботом, составило: {count_applicants}.\n'
            f'Количество уникальных пользователей: {unique_applicants}'
        )
        logger_data_operations.info(text)
        return {'status': True, 'text': text}
    except PeeweeException as error:
        text_error = (
            'При отправке запроса к таблице с информацией '
            'о пользователях, произошла ошибка.'
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        logger_data_operations.exception(text_error)
        return {'status': False, 'error': text_error}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()


def get_count_favorites() -> dict:
    """Подсчет количества пользователей и вакансий, добавленных в избранное."""
    try:
        if not db_work_for_everyone.is_connection_usable():
            db_work_for_everyone.connect()
        count_vacancies = Favorites.select().count()
        count_applicants = (
            Favorites.select(Favorites.applicant_tg_id).distinct().count()
        )
        time_select = datetime.now().strftime('%d.%m.%y %H:%M:%S')
        text = (
            f'По состоянию на {time_select} общее количество вакансий, '
            f'добавленных в избранное, составило: {count_vacancies}\n'
            'Количество пользователей, которые воспользовались '
            f'разделом избранное, составило: {count_applicants}'
        )
        logger_data_operations.info(text)
        return {'status': True, 'text': text}
    except PeeweeException as error:
        text_error = (
            'При отправке запроса к таблице с информацией о вакансиях, '
            'добавленных в избранное, произошла ошибка.'
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        logger_data_operations.exception(text_error)
        return {'status': False, 'error': text_error}
    finally:
        if not db_work_for_everyone.is_closed():
            db_work_for_everyone.close()
