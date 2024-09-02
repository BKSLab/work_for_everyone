import logging
from typing import Any, Optional

logger_api_hh = logging.getLogger(__name__)


def check_responce_api_hh_one_vacancy(
    response_data: Optional[dict | Any],
) -> dict:
    """
    Проверка ответа на запрос к api hh.ru для получения данных одной вакансии.
    """
    if not isinstance(response_data, dict):
        logger_api_hh.critical(
            'При запросе данных об одной вакансии от api hh.ru '
            'получен не соответствующий тип данных. На вход ожидался словарь, '
            f'а получен тип: {type(response_data)}.'
        )
        return {'status': False}

    keys_responce_from_api_hh = [
        'id',
        'salary',
        'description',
        'employer',
        'name',
        'alternate_url',
    ]

    if not set(keys_responce_from_api_hh).issubset(set(response_data.keys())):
        logger_api_hh.critical(
            'При запросе к api hh.ru на получение данных об одной вакансии, '
            'ключи в полученном ответе не соответствуют документации.'
            f'Получе словарь содержит ключи: {str(response_data.keys())}'
        )
        return {'status': False}
    return {'status': True}


def check_responce_api_hh_vacancies(
    response_data: Optional[dict | Any],
) -> dict:
    """
    Проверка данных, полученных от api hh.ru при запросе данных о вакансиях
    в Москве, Санкт-Петербурге и пользовательской локации.
    """
    # Проверка, является ли преобразованный объект ответа словарем
    if not isinstance(response_data, dict):
        logger_api_hh.critical(
            'При запросе данных о вакансиях в Москве, Санкт-Петербурге '
            'и в пользовательской локации от api hh.ru получен не '
            'соответствующий тип данных. На вход '
            f'ожидался словарь, а получен тип: {type(response_data)}.'
        )
        return {'status': False}
    keys_responce_from_api_hh = [
        'items',
        'found',
        'pages',
        'page',
        'per_page',
        'clusters',
        'arguments',
        'fixes',
        'suggests',
        'alternate_url',
    ]
    # Проверка ключей полученного словаря со списком ожидаемых
    # ключей в соответствии с документацией к api сайта hh.ru
    if not set(keys_responce_from_api_hh) == set(response_data.keys()):
        logger_api_hh.critical(
            'При запросе к api hh.ru на получение данных о вакансиях в '
            'в Москве, Санкт-Петербурге и в пользовательской локации, '
            'ключи в полученном ответе не соответствуют документации. '
            f'Получе словарь содержит ключи: {str(response_data.keys())}'
        )
        return {'status': False}
    return {'status': True}


def check_received_data_hh(response_data: Optional[dict | Any]) -> dict:
    """
    Проверка данных, полученных от api hh.ru, перед их обработкой
    для показа пользователю
    """
    if not isinstance(response_data, dict):
        logger_api_hh.critical(
            'При подготовки данных для показа пользователю вакансий, '
            'полученных от api hh.ru, ожидался словарь с данными вакансии. '
            f'Однако был получен иной тип данных: {type(response_data)}.'
        )
        return {'status': False}

    keys_responce_from_api_hh = [
        'salary',
        'employer',
        'address',
        'contacts',
        'alternate_url',
    ]

    if not set(keys_responce_from_api_hh).issubset(set(response_data.keys())):
        logger_api_hh.critical(
            'От api hh.ru пришел ответ с данными о вакансии, в котором '
            'ключи не соответствуют документации.'
            f'Получе словарь содержит ключи: {str(response_data.keys())}'
        )
        return {'status': False}
    return {'status': True}
