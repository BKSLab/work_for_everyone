import csv
import logging
import os
from typing import List, Union

from config_data.config import BASE_DIR
from database.models import (
    Applicant,
    Favorites,
    Region,
    Vacancy,
    db_work_for_everyone,
)
from peewee import ModelSelect


def _database_connection() -> None:
    """Открытие сооединения с БД."""
    if not db_work_for_everyone.is_connection_usable():
        db_work_for_everyone.connect()
        logging.info('the connection to the database was open')


def _database_close() -> None:
    """Закрытие соединения с БД."""
    if not db_work_for_everyone.is_closed():
        db_work_for_everyone.close()
        logging.info('the connection to the database was closed')


def load_information_about_regions() -> None:
    """Загрузка данных о регионах в БД."""
    with open(
        os.path.join(BASE_DIR, 'database', 'information_about_regions.csv')
    ) as information_about_regions_csv:
        reader = csv.reader(
            information_about_regions_csv,
            delimiter=';',
            skipinitialspace=True,
        )
        rows = [
            {
                key: value
                for key, value in zip(
                    ['region_code', 'region_name', 'federal_district_code'],
                    one_record,
                )
            }
            for one_record in reader
        ]
    Region.insert_many(rows).execute()
    logging.info('data has been successfully loaded into the region table')


def check_table_region_and_data_exists() -> None:
    """
    Проверка наличия таблицы region в БД и данных в ней.
    При отсутствии таблицы, таблица будет создана. В том случае,
    если в таблице данные отсутствуют, они будут загружены.
    """
    _database_connection()
    if not db_work_for_everyone.table_exists(
        table_name=['region', 'applicant', 'vacancy', 'favorites']
    ):
        db_work_for_everyone.create_tables(
            [Region, Applicant, Vacancy, Favorites]
        )
    if Region.get_or_none() is None:
        load_information_about_regions()
    _database_close()


def get_data_regions(
    federal_district_code: int,
) -> Union[bool, List[tuple[str, int]]]:
    """
    Получение списка регионов заданного пользователем федерального округа.
    """
    _database_connection()
    data: ModelSelect = (
        Region.select(Region.region_name, Region.region_code)
        .where(Region.federal_district_code == federal_district_code)
        .tuples()
    )
    _database_close()
    if data:
        return [region_data for region_data in data]
    return False


def saving_applicant_data(data: dict[str, str | int]) -> Applicant:
    """Сохранение данных пользователя (соискателя)."""
    _database_connection()
    instance, _ = Applicant.get_or_create(
        name_applicant=data.get('name_applicant'),
        user_tg_id=data.get('user_tg_id'),
        region=Region.get(Region.region_code == data.get('region_code')),
        location=data.get('location'),
    )
    _database_close()
    return instance


def saving_vacancies_data(data: List[dict]) -> None:
    """Сохранение данных о вакансиях в пользовательской локации."""
    _database_connection()
    Vacancy.insert_many(data).execute()
    logging.info('data has been successfully loaded into the vacancy table')
    _database_close()


def deleting_vacancy_data(user_tg_id: int) -> None:
    """
    Удаление данных о вакансиях, оставшихся после
    предыдущего запроса пользователя.
    """
    _database_connection()
    Vacancy.delete().where(Vacancy.applicant_tg_id == user_tg_id).execute()
    _database_close()


def get_count_vacancies(user_tg_id: int) -> int:
    """Подсчет количества найденных в пользовательской локации вакансий."""
    _database_connection()
    count_vacancies = (
        Vacancy.select().where(Vacancy.applicant_tg_id == user_tg_id).count()
    )
    _database_close()
    return count_vacancies


def get_vacancies(user_tg_id: int) -> ModelSelect:
    """Получение вакансий пользователя."""
    _database_connection()
    vacancies = Vacancy.select().where(Vacancy.applicant_tg_id == user_tg_id)
    _database_close()
    return vacancies


def check_vacancy_exists(
    # company_code: str,
    vacancy_id: str,
    user_tg_id: int,
) -> bool:
    """Проверка наличия вакансии."""
    _database_connection()
    query_result = (
        Vacancy.select()
        .where(
            # Vacancy.company_code == company_code,
            Vacancy.vacancy_id == vacancy_id,
            Vacancy.applicant_tg_id == user_tg_id,
        )
        .exists()
    )
    _database_close()
    return query_result


def get_vacancy(
    # company_code: str,
    vacancy_id: str,
    user_tg_id: int,
) -> Vacancy:
    """Проверка наличия вакансии."""
    _database_connection()
    vacancy = Vacancy.get_or_none(
        # Vacancy.company_code == company_code,
        Vacancy.vacancy_id == vacancy_id,
        Vacancy.applicant_tg_id == user_tg_id,
    )
    _database_close()
    return vacancy


def saving_vacancy_favorites(data: dict[str, str | int]) -> None:
    """Сохранение вакансии в избранном."""
    _database_connection()
    Favorites.get_or_create(
        applicant_tg_id=data.get('applicant_tg_id'),
        vacancy_name=data.get('vacancy_name'),
        salary=data.get('salary'),
        employer_name=data.get('employer_name'),
        employer_location=data.get('employer_location'),
        employer_email=data.get('employer_email'),
        employer_phone_number=data.get('employer_phone_number'),
        company_code=data.get('company_code'),
        vacancy_id=data.get('vacancy_id'),
    )
    _database_close()


def check_vacancy_favorites_exists(
    company_code: str, vacancy_id: str, user_tg_id: int
) -> bool:
    """Проверка наличия вакансии в избранном."""
    _database_connection()
    query_result = (
        Favorites.select()
        .where(
            Favorites.company_code == company_code,
            Favorites.vacancy_id == vacancy_id,
            Favorites.applicant_tg_id == user_tg_id,
        )
        .exists()
    )
    _database_close()
    return query_result


def delete_vacancy_from_favorites(
    company_code: str, vacancy_id: str, user_tg_id: int
):
    """Удаление вакансии из избранного."""
    _database_connection()
    Favorites.delete().where(
        Favorites.company_code == company_code,
        Favorites.vacancy_id == vacancy_id,
        Favorites.applicant_tg_id == user_tg_id,
    ).execute()
    _database_close()


def get_ten_vacancies(user_tg_id: int, page_number: int) -> Vacancy:
    """Получение по десять вакансий для показа пользователю."""
    # кажды раз при запросе функция должна возвращать список из десяти вакансий
    # найденных в локации пользователя
    _database_connection()
    vacancies = (
        Vacancy.select()
        .where(Vacancy.applicant_tg_id == user_tg_id)
        .paginate(page_number, 10)
    )
    _database_close()
    return vacancies


def get_vacancies_from_favorites(user_tg_id: int) -> ModelSelect:
    """Получение вакансий добавленных в избранное."""
    _database_connection()
    vacancies = Favorites.select().where(
        Favorites.applicant_tg_id == user_tg_id
    )
    _database_close()
    return vacancies


def get_vacancy_from_favorites(vacancy_id: str, user_tg_id: int) -> Vacancy:
    """Проверка наличия вакансии в избранном."""
    _database_connection()
    vacancy = Favorites.get_or_none(
        # Vacancy.company_code == company_code,
        Favorites.vacancy_id == vacancy_id,
        Favorites.applicant_tg_id == user_tg_id,
    )
    _database_close()
    return vacancy
