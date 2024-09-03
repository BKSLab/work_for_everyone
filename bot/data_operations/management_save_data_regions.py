import csv
import logging
import os

from data_operations.save_data import saving_region_data
from data_operations.check_data import region_data_exists
from config_data.config import load_config


logger_data_operations = logging.getLogger(__name__)
config = load_config()


def read_csv_file_with_data_regions() -> dict[dict[str, str]]:
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


def management_saving_data_regions() -> dict:
    """
    Функция управления процессом чтения и загрузки данных
    о регионах в таблицу region
    """
    # Проверка наличии данных о регионах в таблице region в БД
    result_check = region_data_exists()

    # Если при проверки наличия таблиц в БД произошла ошибка,
    # работа функции завершается, администратору направляется
    # соответствующее сообщение.
    if not result_check.get('status'):
        return {'status': False, 'error': result_check.get('error')}
    # Если при обращении к БД не возникнит ошибок, но при этом
    # будет обнаружено, что таблицы уже существуют в БД, то
    # функция завершает свою работу, а администратору будет
    # направлено соответствующее сообщение
    if result_check.get('status') and result_check.get('data_exists'):
        return {'status': True, 'text_msg': result_check.get('text_msg')}
    # Если при обращении к БД не возникнит ошибок и необходимых таблиц
    # не будет обнаружен, управление будет передано в функцию
    # read_csv_file_with_data_regions(), которая прочитает
    # csv файл с данными о регионах и поместит эти данные в список
    if result_check.get('status') and not result_check.get('data_exists'):
        result_load = read_csv_file_with_data_regions()
        # В случае, если в ходе чтения файла возникнут ошибки, работа
        # функции будет завершена, а администратору будет направлено сообщение
        if not result_load.get('status'):
            return {'status': False, 'error': result_load.get('error')}
        # Если никаких ошибок при чтении csv файла не возникло,
        # то сгенирированный список словарей с данными о регионах
        # передается в функцию saving_region_data()
        # для сохранения этих данных в таблице region
        data_regions = result_load.get('data_regions')
        query_result = saving_region_data(data_regions)
        # В случае, если в ходе сохранение данных в БД возникнут ошибки, работа
        # функции будет завершена, а администратору будет направлено сообщение
        if not query_result.get('status'):
            return {'status': False, 'error': query_result.get('error')}
        # В случае удачного завершения операции по сохранении данных
        # о регионах в БД функция вернет результат со статусом True
        # и сообщением об удачном завершении
        text_msg = (
            'Результат работы функции read_csv_file_with_data_regions(): '
            f'{result_load.get("text_msg")}\nРезультат работы функции '
            'saving_region_data(): Данные о регионах были'
            'успешно сохранены в таблице region. Всего добавлено '
            f'{query_result.get("count_rows")} записей'
        )
        logger_data_operations.info(text_msg)
        return {'status': True, 'text_msg': text_msg}
