import re
from typing import List

from api_trudvsem.endpoints import ParameterRequest  # type: ignore


def _check_api_responce(response_data: dict) -> bool:
    """Проверка данных, полученных от API."""
    if (
        isinstance(response_data, dict)
        and all(
            key in response_data
            for key in ('status', 'request', 'meta', 'results')
        )
        and isinstance(response_data.get('results').get('vacancies'), list)
    ):
        return True
    return False


def preparing_data_for_vacancy_tb(
    list_vacancies: List[dict], location: str, tg_user_id: int
):
    """Обработка полученных данных от api для записи в БД."""
    for vacancies in list_vacancies:
        if not _check_api_responce(vacancies):
            return {
                'status': False,
                'error_text': (
                    'От API "Работа в России" получен ответ, '
                    'не соответствующий документации.'
                ),
            }
    vacancy_data = [
        item
        for sublist in list_vacancies
        for item in sublist.get('results').get('vacancies')
    ]

    vacancies_lst = []
    for vacancy in vacancy_data:
        vacancy_location = (
            vacancy.get('vacancy')
            .get('addresses')
            .get('address')[ParameterRequest.FIRST_ELEMENT_LIST]
            .get('location')
        )
        if location.lower() in vacancy_location.lower():
            vacancies_lst.append(
                {
                    'applicant_tg_id': tg_user_id,
                    'vacancy_name': vacancy.get('vacancy').get('job-name'),
                    'social_protected': vacancy.get('vacancy').get(
                        'social_protected'
                    ),
                    'salary': 'Работодатель не указал заработную плату.'
                    if vacancy.get('vacancy').get('salary') is None
                    else vacancy.get('vacancy').get('salary'),
                    'employer_name': vacancy.get('vacancy')
                    .get('company')
                    .get('name'),
                    'employer_location': vacancy.get('vacancy')
                    .get('addresses')
                    .get('address')[ParameterRequest.FIRST_ELEMENT_LIST]
                    .get('location'),
                    'employer_email': 'Работодатель не указал email адрес'
                    if vacancy.get('vacancy').get('company').get('email')
                    is None
                    else vacancy.get('vacancy').get('company').get('email'),
                    'employer_phone_number': (
                        'Работодатель не указал номер телефона'
                    )
                    if vacancy.get('vacancy').get('company').get('phone')
                    is None
                    else vacancy.get('vacancy').get('company').get('phone'),
                    'company_code': vacancy.get('vacancy')
                    .get('company')
                    .get('companycode'),
                    'vacancy_id': vacancy.get('vacancy').get('id'),
                }
            )
    return {'status': True, 'vacancies': vacancies_lst}


def preparing_data_one_vacancy(one_vacancy):
    """Обработка данных о запрошенной пользователем вакансии."""
    if not _check_api_responce(one_vacancy):
        return {
            'status': False,
            'error_text': (
                'От API "Работа в России" получен ответ, '
                'не соответствующий документации.'
            ),
        }
    vacancy_data = (
        one_vacancy.get('results')
        .get('vacancies')[ParameterRequest.FIRST_ELEMENT_LIST]
        .get('vacancy')
    )
    contact_list = vacancy_data.get('contact_list')
    if contact_list:
        employer_phone_number = contact_list[
            ParameterRequest.FIRST_ELEMENT_LIST
        ].get('contact_value')
    else:
        employer_phone_number = 'Работодатель не указал номер телефона'
    vacancy = {
        'vacancy_name': vacancy_data.get('job-name'),
        'vacancy_id': vacancy_data.get('id'),
        'social_protected': vacancy_data.get('social_protected'),
        'duty': re.sub(r"<[^>]+>", "", vacancy_data.get('duty'), flags=re.S),
        'location': vacancy_data.get('addresses')
        .get('address')[ParameterRequest.FIRST_ELEMENT_LIST]
        .get('location'),
        'salary': 'Работодатель не указал заработную плату.'
        if vacancy_data.get('salary') is None
        else vacancy_data.get('salary'),
        'salary_min': 'Работодатель не указал минимальную заработную плату.'
        if vacancy_data.get('salary_min') is None
        else vacancy_data.get('salary_min'),
        'salary_max': (
            'Работодатель не указал максимальный размер заработной платы.'
        )
        if vacancy_data.get('salary_max') is None
        else vacancy_data.get('salary_max'),
        'employer_name': vacancy_data.get('company').get('name'),
        'company_code': vacancy_data.get('company').get('companycode'),
        'employer_phone_number': employer_phone_number,
        'employer_email': 'Работодатель не указал адрес электронной почты.'
        if vacancy_data.get('company').get('email') is None
        else vacancy_data.get('company').get('email'),
        'contact_person': 'Работодатель не указал контактное лицо.'
        if vacancy_data.get('contact_person') is None
        else vacancy_data.get('contact_person'),
        'creation_date': vacancy_data.get('creation-date'),
    }
    return {'status': True, 'vacancy': vacancy}
