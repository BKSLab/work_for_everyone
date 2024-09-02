import logging
from typing import Any, Optional

logger_api_trudvsem = logging.getLogger(__name__)


def check_responce_api_trudvsem_one_vacancy(
    response_data: Optional[dict | Any],
) -> dict:
    """
    Проверка ответа на запрос к api trudvsem.ru для
    получения данных одной вакансии.
    """
    # Проверка типа полученных данных. Ожидается словарь
    if not isinstance(response_data, dict):
        logger_api_trudvsem.critical(
            'При запросе данных об одной вакансии от api trudvsem.ru '
            'получен не соответствующий тип данных. На вход ожидался словарь, '
            f'а получен тип: {type(response_data)}.'
        )
        return {'status': False}

    keys_responce_from_api_trudvsem = ['status', 'request', 'meta', 'results']
    if not set(keys_responce_from_api_trudvsem).issubset(
        set(response_data.keys())
    ):
        logger_api_trudvsem.critical(
            'При запросе к api trudvsem.ru на получение данных об одной '
            'вакансии, ключи в полученном ответе не соответствуют '
            'документации. Получе словарь содержит ключи: '
            f'{str(response_data.keys())}'
        )
        return {'status': False}
    return {'status': True}


def check_received_data_trudvsem(response_data: Any) -> dict[str, bool]:
    """
    Проверка данных, полученных от api trudvsem.ru, перед их обработкой
    для показа пользователю
    """
    if not isinstance(response_data, dict):
        logger_api_trudvsem.critical(
            'При подготовки данных для показа пользователю вакансий, полученных '
            'от api trudvsem.ru, ожидался словарь с данными вакансии. '
            f'Однако был получен иной тип данных: {type(response_data)}.'
        )
        return {'status': False}

    keys_responce_from_api_trudvsem = ['status', 'request', 'meta', 'results']
    if not set(keys_responce_from_api_trudvsem).issubset(
        set(response_data.keys())
    ):
        logger_api_trudvsem.critical(
            'От api trudvsem.ru пришел ответ с данными о вакансии, в котором '
            'ключи не соответствуют документации.'
            f'Получе словарь содержит ключи: {str(response_data.keys())}'
        )
        return {'status': False}
    return {'status': True}


def check_received_data_one_vacancy_trudvsem(
    vacancy_data: Any,
) -> dict[str, bool]:
    """
    Проверка данных об одной вакансии, полученных от api trudvsem.ru,
    перед их обработкой для показа пользователю
    """
    if not isinstance(vacancy_data, dict):
        logger_api_trudvsem.critical(
            'При подготовки данных для показа пользователю одной вакансии, '
            'полученной от api trudvsem.ru, ожидался словарь с данными '
            f'вакансии. Однако был получен : {type(vacancy_data)}.'
        )
        return {'status': False}
    keys_vacancy_data = [
        'id',
        'duty',
        'job-name',
        'social_protected',
        'salary',
        'company',
        'addresses',
    ]
    if not set(keys_vacancy_data).issubset(set(vacancy_data.keys())):
        logger_api_trudvsem.critical(
            'От api trudvsem.ru пришел ответ с данными об одной вакансии'
            ', в котором ключи не соответствуют документации.'
            f'Получе словарь содержит ключи: {str(vacancy_data.keys())}'
        )
        return {'status': False}
    return {'status': True}
