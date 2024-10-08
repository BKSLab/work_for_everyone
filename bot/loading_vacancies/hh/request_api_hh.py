import asyncio
import logging

import aiohttp
import requests

from json import JSONDecodeError
from http import HTTPStatus

from config_data.config import load_config
from loading_vacancies.endpoints import EndpointHH, ParameterRequestHH
from loading_vacancies.hh.check_api_hh_responce import (
    check_responce_api_hh_one_vacancy,
    check_responce_api_hh_vacancies,
)

logger_api_hh = logging.getLogger(__name__)
config = load_config()


async def request_to_api_hh_other_vacancies(
    session: aiohttp.ClientSession,
    reg_code_hh: int,
    location: str,
    page: int = 0,
) -> dict:
    """
    Запрос к api hh.ru на получение данных о вакансиях
    в пользовательской локации.
    """
    headers = {'Authorization': f'Bearer {config.app.access_token_hh}'}
    payload = {
        'page': page,
        'per_page': ParameterRequestHH.VACANCIES_PER_ONE_PAGE_HH,
        'area': reg_code_hh,
        'text': location,
        'label': ParameterRequestHH.SOCIAL_PROTECTED_HH,
    }
    try:
        async with session.get(
            EndpointHH.VACANCY_URL, headers=headers, params=payload
        ) as api_response:
            if api_response.status != HTTPStatus.OK:
                logger_api_hh.critical(
                    'При запросе к api сайта hh.ru для получения данных '
                    'о вакансиях в пользовательской локации, получен код '
                    f'не равный 200. Полученный код: {api_response.status}'
                )
                return {'status': False}
            try:
                api_response_dict = await api_response.json()
                return {
                    'status': True,
                    'data': api_response_dict,
                }
            except JSONDecodeError as error:
                logger_api_hh.critical(
                    'При преобразовании полученного ответа от api hh.ru '
                    f'при запросе данных о вакансиях в пользовательской '
                    'локации в объект dict произошла ошибка. '
                    f'Текст ошибки: {error}. '
                    f'Тип ошибки: {type(error).__name__}.'
                )
                return {'status': False}
    except aiohttp.ClientError as error:
        logger_api_hh.exception(
            'При запросе к api сайта hh.ru для получения данных о вакансиях '
            f'в пользовательской локации ({location}), произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    except asyncio.TimeoutError as error:
        logger_api_hh.exception(
            'Таймаут при запросе к API сайта hh.ru для получения данных '
            f'о вакансиях в пользовательской локации ({location}). '
            f'Текст ошибки: {error}, Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    except Exception as error:
        logger_api_hh.exception(
            'При работе функции request_to_api_hh_other_vacancies произошла '
            'ошибка. Функция получила на вход следующие аргументы: '
            f'Локация: {location}, код региона: {str(reg_code_hh)}. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}


def request_to_api_hh_one_vacancy(vacancy_id: str) -> dict:
    """Запрос к api hh.ru на получение данных об одной вакансии."""
    headers = {'Authorization': f'Bearer {config.app.access_token_hh}'}
    try:
        api_response = requests.get(
            ''.join([EndpointHH.VACANCY_URL, vacancy_id]), headers=headers
        )
    except requests.exceptions as error:
        logger_api_hh.exception(
            'При запросе к api сайта hh.ru для получения данных об '
            f'одной вакансии (id вакансии: {vacancy_id}), произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    # перехват случая, когда вакансия не найдена (удалена)
    if api_response.status_code == requests.codes.not_found:
        logger_api_hh.critical(
            f'Вакансия с id: {vacancy_id} при запросе к api hh.ru не найдена. '
            'При запросе был получен код 404 (not found)'
        )
        return {'status': True, 'vacancy_status': 'does_not_exist'}

    if api_response.status_code != requests.codes.ok:
        logger_api_hh.critical(
            'При запросе к api сайта hh.ru для получения данных об '
            f'одной вакансии (id вакансии: {vacancy_id}), получен код '
            f'не равный 200. Полученный код: {api_response.status_code}'
        )
        return {'status': False}
    # Контроль преобразования полученного ответа в объект ссловаря
    try:
        api_response_dict = api_response.json()
    except requests.exceptions.JSONDecodeError as error:
        logger_api_hh.exception(
            'При преобразовании полученного ответа от api hh.ru '
            f'при запросе данных о вакансии с id {vacancy_id} в объект '
            f'dict произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    return {
        'status': True,
        'data': api_response_dict,
    }


def request_to_api_hh_msk_spb(
    reg_code_hh: int,
    parametr_name: str,
    parametr_id: str | int,
    page: int = 0,
):
    """
    Запрос к api hh.ru на получение данных о вакансиях
    в Москве и Санкт-Петербурге.
    """
    # Токен передается в заголовке запроса
    headers = {'Authorization': f'Bearer {config.app.access_token_hh}'}
    # Словарь с необходимыми параметрами для запроса к api hh.ru
    payload = {
        'page': page,
        'per_page': ParameterRequestHH.VACANCIES_PER_ONE_PAGE_HH,
        'area': reg_code_hh,
        parametr_name: parametr_id,
        'label': ParameterRequestHH.SOCIAL_PROTECTED_HH,
    }
    try:
        api_response = requests.get(
            EndpointHH.VACANCY_URL,
            headers=headers,
            params=payload,
        )
    except requests.exceptions as error:
        logger_api_hh.exception(
            'При запросе к api сайта hh.ru для получения данных о вакансиях '
            f'в Москве и Санкт-Петербурге, произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    if api_response.status_code != requests.codes.ok:
        logger_api_hh.critical(
            'При запросе к api сайта hh.ru для получения данных о вакансиях '
            f'в Москве и Санкт-Петербурге, получен код '
            f'не равный 200. Полученный код: {api_response.status_code}'
        )
        return {'status': False}
    # Контроль преобразования полученного ответа в объект ссловаря
    try:
        api_response_dict = api_response.json()
    except requests.exceptions.JSONDecodeError as error:
        logger_api_hh.exception(
            'При преобразовании полученного ответа от api hh.ru '
            f'при запросе данных о вакансиях в Москве и Санкт-Петербурге '
            f'в объект dict произошла ошибка. '
            f'Текст ошибки: {error}. Тип ошибки: {type(error).__name__}.'
        )
        return {'status': False}
    return {
        'status': True,
        'data': api_response_dict,
    }


def get_one_vacancy_hh(vacancy_id: str) -> dict:
    """
    Получение данных об одной вакансии от api hh.ru.
    Для показа пользователю подробной информации о вакансии.
    """
    api_responce = request_to_api_hh_one_vacancy(vacancy_id=vacancy_id)
    if not api_responce.get('status'):
        return {'status': False}

    if api_responce.get('status') and 'vacancy_status' in api_responce:
        return {'status': True, 'vacancy_status': 'does_not_exist'}
    # Если ошибок при обращении к api сайта hh.ru не возникло,
    # полученные данные направляются на проверку их соответствия
    check_result = check_responce_api_hh_one_vacancy(
        response_data=api_responce.get('data')
    )
    if not check_result.get('status'):
        return {'status': False}

    # обработка случая, когда вакансия перенесена в архив
    vacancy = api_responce.get('data')
    archived = vacancy.get('archived')
    if archived:
        return {
            'status': True,
            'vacancy_status': 'archival',
            'vacancy': vacancy,
        }
    return {'status': True, 'vacancy_status': 'actual', 'vacancy': vacancy}


def get_vacancies_hh_msk_spb(
    reg_code_hh: int, parametr_id: str | int, parametr_name: str
):
    """
    Получение данных о вакансиях в Москве и Санкт-Петербурге от api hh.ru.
    """
    api_responce = request_to_api_hh_msk_spb(
        reg_code_hh=reg_code_hh,
        parametr_name=parametr_name,
        parametr_id=parametr_id,
    )
    if not api_responce.get('status'):
        return {'status': False}

    check_result = check_responce_api_hh_vacancies(
        response_data=api_responce.get('data')
    )
    if not check_result.get('status'):
        return {'status': False}

    # Получение количества страниц с вакансиями
    pages = api_responce.get('data').get('pages')
    # проверка не является ли значение пустым
    if not pages:
        logger_api_hh.critical(
            'При первом запросе к api hh.ru на получение вакансий '
            'в Москве и Санкт-Петербурге в ответе не получено количество '
            'страниц с результатами запроса'
        )
        return {'status': False}

    # Список для добавления информации о вакансиях
    vacancy_lst = []
    # проход по страницам с информацией о вакансиях
    for page in range(pages):
        # Запрос к api сайта hh.ru для получения информации о
        # вакансиях на отдельной страницы.
        api_responce = request_to_api_hh_msk_spb(
            reg_code_hh=reg_code_hh,
            parametr_name=parametr_name,
            parametr_id=parametr_id,
            page=page,
        )
        if not api_responce.get('status'):
            return {'status': False}

        # Если ошибок при обращении к api сайта hh.ru не возникло,
        # полученные данные направляются на проверку их соответствия
        check_result = check_responce_api_hh_vacancies(
            response_data=api_responce.get('data')
        )
        if not check_result.get('status'):
            return {'status': False}

        # Получение списка вакансий на соответствующей страницы
        items = api_responce.get('data').get('items')

        # Добавление вакансий в список
        [vacancy_lst.append(vacancy_data) for vacancy_data in items]
    return {'status': True, 'vacancy_lst': vacancy_lst}


async def get_vacancies_api_hh_user_location(
    session: aiohttp.ClientSession,
    reg_code_hh: str,
    user_location: str
) -> dict:
    """
    Получение и обработка данных в пользовательской локации от api hh.ru.
    """
    api_response = await request_to_api_hh_other_vacancies(
        session=session,
        reg_code_hh=reg_code_hh,
        location=user_location,
    )

    if not api_response.get('status'):
        return {'status': False}

    check_result = check_responce_api_hh_vacancies(
        response_data=api_response.get('data')
    )
    if not check_result.get('status'):
        return {'status': False}

    # Получение количества страниц с вакансиями
    pages = api_response.get('data').get('pages')

    # Проверка на пустое значение
    if not pages:
        logger_api_hh.critical(
            'При первом запросе к api hh.ru на получение вакансий '
            'в пользовательской локации в ответе не получено количество '
            'страниц с результатами запроса'
        )
        return {'status': False}

    # Список для добавления информации о вакансиях
    vacancy_lst = []

    # Создаем семафор для ограничения количества одновременных запросов
    semaphore = asyncio.Semaphore(3)

    # Функция для выполнения запроса с семафором
    async def fetch_page(page):
        async with semaphore:
            await asyncio.sleep(0.1)
            return await request_to_api_hh_other_vacancies(
                session=session,
                reg_code_hh=reg_code_hh,
                location=user_location,
                page=page
            )

    # Асинхронный сбор всех запросов для получения вакансий на всех страницах
    tasks = [fetch_page(page) for page in range(pages)]
    responses = await asyncio.gather(*tasks)

    # Обработка полученных данных
    for api_response in responses:
        if not api_response.get('status'):
            return {'status': False}

        # Проверка корректности данных от API
        check_result = check_responce_api_hh_vacancies(
            response_data=api_response.get('data')
        )
        if not check_result.get('status'):
            return {'status': False}

        # Получение списка вакансий на соответствующей странице
        items = api_response.get('data').get('items')

        # Добавление вакансий в список
        vacancy_lst.extend(items)

    return {'status': True, 'vacancy_lst': vacancy_lst}
