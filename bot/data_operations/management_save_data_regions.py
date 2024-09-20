import csv
import logging
import os

from data_operations.save_data import saving_region_data
from data_operations.check_data import region_data_exists
from config_data.config import load_config


logger_data_operations = logging.getLogger(__name__)
config = load_config()


def read_csv_file_with_data_regions() -> dict:
    """Чтение данных о регионах из csv файла и их добавление в список"""
    try:
        with open(
            os.path.join(
                config.app.base_dir,
                'database',
                'information_about_regions.csv'
            )
        ) as information_about_regions_csv:
            reader = csv.reader(
                information_about_regions_csv,
                delimiter=';',
                skipinitialspace=True,
            )
            try:
                rows = [
                    {
                        key: value
                        for key, value in zip(
                            [
                                'region_code',
                                'region_name',
                                'federal_district_code',
                                'region_code_hh',
                            ],
                            one_record,
                        )
                    }
                    for one_record in reader
                ]
            except csv.Error as error:
                text_error = (
                    'Во время чтения файла information_about_regions.csv '
                    f'произошла ошибка ({str(reader.line_num)}). '
                    f'Текст ошибки: {error}. '
                    f'Тип ошибки: {type(error).__name__}.'
                )
                logger_data_operations.exception(text_error)
                return {'status': False, 'error': text_error}

        text_msg = (
            'Данные о регионах из information_about_regions.csv '
            'успешно прочитаны и добавлены в список для их '
            f'последующей записи в БД. Всего обработано {len(rows)} записей'
        )
        logger_data_operations.info(text_msg)
        return {'status': True, 'text_msg': text_msg, 'data_regions': rows}

    except FileNotFoundError as error:
        text_error = (
            'При попытки открыть information_about_regions.csv для чтения,'
            'файл не был обнаружен в соответствующей директории. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        logger_data_operations.exception(text_error)
        return {'status': False, 'error': text_error}

    except Exception as error:
        text_error = (
            'В работе read_csv_file_with_data_regions() произошла ошибка.'
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        logger_data_operations.exception(text_error)
        return {'status': False, 'error': text_error}


def management_saving_data_regions() -> dict:
    """
    Функция управления процессом чтения и загрузки данных
    о регионах в таблицу region
    """
    result_check = region_data_exists()
    if not result_check.get('status'):
        return {'status': False, 'error': result_check.get('error')}
    if result_check.get('status') and result_check.get('data_exists'):
        return {'status': True, 'text_msg': result_check.get('text_msg')}
    if result_check.get('status') and not result_check.get('data_exists'):
        result_load = read_csv_file_with_data_regions()
        if not result_load.get('status'):
            return {'status': False, 'error': result_load.get('error')}
        data_regions = result_load.get('data_regions')
        query_result = saving_region_data(data_regions)
        if not query_result.get('status'):
            return {'status': False, 'error': query_result.get('error')}
        text_msg = (
            'Результат работы функции read_csv_file_with_data_regions(): '
            f'{result_load.get("text_msg")}\nРезультат работы функции '
            'saving_region_data(): Данные о регионах были'
            'успешно сохранены в таблице region. Всего добавлено '
            f'{query_result.get("count_rows")} записей'
        )
        logger_data_operations.info(text_msg)
        return {'status': True, 'text_msg': text_msg}
