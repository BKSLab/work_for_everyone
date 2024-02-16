from math import ceil

import requests
from api_trudvsem.endpoints import Endpoint, ParameterRequest


def _send_request_to_api(params, region_code):
    """Запрос к api работа в России."""

    api_response = requests.get(
        f'{Endpoint.ENDPOINT_REGION}{region_code}', params=params
    )
    if api_response.status_code != requests.codes.ok:
        raise requests.HTTPError(
            'при запросе сервер вернул код ' f'{api_response.status_code}',
        )
    return api_response


def get_data_vacancies_from_api(region_code: int) -> dict:
    """Получение данных о вакансиях в регионе пользователя."""
    try:
        api_responce = _send_request_to_api(
            {'social_protected': ParameterRequest.SOCIAL_PROTECTED},
            region_code,
        )
    except requests.HTTPError as error:
        return {'status': False, 'error_text': error}
    count_pages = ceil(
        int(api_responce.headers.get('TotalResultCount'))
        / ParameterRequest.VACANCIES_PER_ONE_PAGE
    )

    try:
        data_vacancies_in_region = [
            _send_request_to_api(
                {
                    'social_protected': ParameterRequest.SOCIAL_PROTECTED,
                    'limit': ParameterRequest.VACANCIES_PER_ONE_PAGE,
                    'offset': page,
                },
                region_code,
            ).json()
            for page in range(count_pages)
        ]
    except requests.HTTPError as error:
        return {'status': False, 'error_text': error}
    return {'status': True, 'data': data_vacancies_in_region}


def get_data_one_vacancy(company_code, vacancy_id) -> dict:
    """Получение данных об одной вакансии."""
    try:
        api_responce = requests.get(
            f'{Endpoint.ONE_VACANCY_ENDPOINT}/{company_code}/{vacancy_id}'
        )
        if api_responce.status_code != requests.codes.ok:
            raise requests.HTTPError(
                'при запросе сервер вернул код ' f'{api_responce.status_code}',
            )
    except requests.HTTPError as error:
        return {'status': False, 'error_text': error}
    return {'status': True, 'data': api_responce.json()}
