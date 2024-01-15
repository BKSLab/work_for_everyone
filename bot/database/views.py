import csv
import logging
import os
from typing import List

from config_data.config import BASE_DIR
from database.models import Region, db_work_for_everyone
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
    if not db_work_for_everyone.table_exists(table_name='region'):
        Region.create_table()
    if Region.get_or_none() is None:
        load_information_about_regions()
    _database_close()


def get_data_regions(federal_district_code: int) -> List[tuple[str, int]]:
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
