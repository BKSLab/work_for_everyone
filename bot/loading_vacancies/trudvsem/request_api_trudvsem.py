import logging
from math import ceil

import requests
from loading_vacancies.endpoints import EndpointTrudvsem, ParameterRequestTrudvsem
from loading_vacancies.trudvsem.check_api_trudvsem_responce import (
    check_responce_api_trudvsem_one_vacancy,
)

logger_api_trudvsem = logging.getLogger(__name__)


def request_to_api_trudvsem_one_vacancy(company_code: str, vacancy_id: str) -> dict:
    """Запрос к api trudvsem.ru на получение данных об одной вакансии."""
    try:
        api_response = requests.get(
            '/'.join(
                [
                    EndpointTrudvsem.ONE_VACANCY_ENDPOINT,
                    company_code,
                    vacancy_id,
                ]
            )
        )
    except requests.exceptions as error:
        logger_api_trudvsem.exception(
            'При запросе к api сайта trudvsem.ru для получения данных об '
            f'одной вакансии (id вакансии: {vacancy_id}, company_code'
            f': {company_code}), произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    if api_response.status_code != requests.codes.ok:
        logger_api_trudvsem.critical(
            f'При запросе на получение данных от api trudvsem.ru '
            f'(vacancy_id: {vacancy_id}, company_code: {company_code}, '
            f'был получен код {api_response.status_code}'
        )
        return {'status': False}

    try:
        api_response_dict = api_response.json()
    except requests.exceptions.JSONDecodeError as error:
        logger_api_trudvsem.exception(
            'При преобразовании полученного ответа от api trudvsem.ru '
            f'при запросе данных о вакансии с id {vacancy_id} и '
            f'company_code: {company_code} в объект dict произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    return {
        'status': True,
        'data': api_response_dict,
    }


def request_to_api_trudvsem_msk_spb(
    params_trudvsem: dict, reg_code_trudvsem: int
) -> dict:
    """
    Запрос к api trudvsem.ru на получение данных о вакансиях в
    Москве и Санкт-Петербурге.
    """
    try:
        api_response = requests.get(
            f'{EndpointTrudvsem.ENDPOINT_REGION}{reg_code_trudvsem}',
            params=params_trudvsem,
        )
    except requests.exceptions as error:
        logger_api_trudvsem.exception(
            'При запросе к api сайта trudvsem.ru для получения данных о вакансиях '
            f'в Москве и Санкт-Петербурге, произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}

    if api_response.status_code != requests.codes.ok:
        logger_api_trudvsem.critical(
            'При запросе к api сайта trudvsem.ru для получения данных о '
            'вакансиях в Москве и Санкт-Петербурге, получен код '
            f'не равный 200. Полученный код: {api_response.status_code}'
        )
        return {'status': False}
    return {
        'status': True,
        'data': api_response,
    }


def request_to_api_trudvsem_user_location(
    params_trudvsem: dict, reg_code_trudvsem: int
) -> dict:
    """
    Запрос к api trudvsem.ru на получение данных о вакансиях
    в пользовательской локации.
    """
    try:
        api_response = requests.get(
            f'{EndpointTrudvsem.ENDPOINT_REGION}{reg_code_trudvsem}',
            params=params_trudvsem,
        )
    except requests.exceptions as error:
        logger_api_trudvsem.exception(
            'При запросе к api сайта trudvsem.ru для получения данных о '
            f'вакансиях в регионе ({str(reg_code_trudvsem)}), '
            'произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}

    if api_response.status_code != requests.codes.ok:
        logger_api_trudvsem.critical(
            'При запросе к api сайта trudvsem.ru для получения данных о '
            f'вакансиях в в регионе ({str(reg_code_trudvsem)}), получен код '
            f'не равный 200. Полученный код: {str(api_response.status_code)}'
        )
        return {'status': False}
    return {
        'status': True,
        'data': api_response,
    }


def get_one_vacancy_trudvsem(company_code: str, vacancy_id: str) -> dict:
    """
    Получение данных об одной вакансии от api trudvsem.ru.
    Для показа пользователю подробной информации о вакансии.
    """
    api_responce = request_to_api_trudvsem_one_vacancy(
        company_code=company_code,
        vacancy_id=vacancy_id,
    )
    if not api_responce.get('status'):
        return {'status': False}

    check_result = check_responce_api_trudvsem_one_vacancy(
        response_data=api_responce.get('data')
    )
    if not check_result.get('status'):
        return {'status': False}
    results = api_responce.get('data').get('results')
    if not results:
        return {'status': False, 'vacancy_status': 'does_not_exist'}
    return {'status': True, 'vacancy': api_responce.get('data')}


def get_vacancies_trudvsem_msk_spb(
    reg_code_trudvsem: int,
) -> dict:
    """
    Получение данных о вакансиях в Москве и Санкт-Петербурге
    от api trudvsem.ru.
    """
    params = {'social_protected': ParameterRequestTrudvsem.SOCIAL_PROTECTED}
    api_responce = request_to_api_trudvsem_msk_spb(
        params_trudvsem=params,
        reg_code_trudvsem=reg_code_trudvsem,
    )
    if not api_responce.get('status'):
        return {'status': False}
    # вычисление кличества страниц, которые необходимо запросить
    count_pages = ceil(
        int(api_responce.get('data').headers.get('TotalResultCount'))
        / ParameterRequestTrudvsem.VACANCIES_PER_ONE_PAGE
    )
    try:
        vacancy_lst = [
            request_to_api_trudvsem_msk_spb(
                {
                    'social_protected': ParameterRequestTrudvsem.SOCIAL_PROTECTED,
                    'limit': ParameterRequestTrudvsem.VACANCIES_PER_ONE_PAGE,
                    'offset': page,
                },
                reg_code_trudvsem,
            )
            .get('data')
            .json()
            for page in range(count_pages)
        ]
    except Exception as error:
        logger_api_trudvsem.exception(
            'При обработки данных в процессе их получения от api '
            'сайта trudvsem.ru произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    return {'status': True, 'vacancy_lst': vacancy_lst}


def get_vacancies_api_trudvsem_user_location(reg_code_trudvsem: str) -> dict:
    """
    Получение и обработка данных в пользовательской локации от api trudvsem.ru.
    """
    params = {'social_protected': ParameterRequestTrudvsem.SOCIAL_PROTECTED}
    api_responce = request_to_api_trudvsem_user_location(
        params_trudvsem=params,
        reg_code_trudvsem=reg_code_trudvsem,
    )
    if not api_responce.get('status'):
        return {'status': False}
    # вычисление кличества страниц, которые необходимо запросить
    count_pages = ceil(
        int(api_responce.get('data').headers.get('TotalResultCount'))
        / ParameterRequestTrudvsem.VACANCIES_PER_ONE_PAGE
    )
    try:
        vacancy_lst = [
            request_to_api_trudvsem_user_location(
                {
                    'social_protected': ParameterRequestTrudvsem.SOCIAL_PROTECTED,
                    'limit': ParameterRequestTrudvsem.VACANCIES_PER_ONE_PAGE,
                    'offset': page,
                },
                reg_code_trudvsem,
            )
            .get('data')
            .json()
            for page in range(count_pages)
        ]
    except Exception as error:
        logger_api_trudvsem.exception(
            'При обработки данных вакансий в регионе с кодом '
            f'{str(reg_code_trudvsem)} в процессе их получения от api '
            'сайта trudvsem.ru произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    return {'status': True, 'vacancy_lst': vacancy_lst}
