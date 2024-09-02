import logging
import re

from loading_vacancies.endpoints import ParameterRequestTrudvsem
from loading_vacancies.trudvsem.check_api_trudvsem_responce import (
    check_received_data_one_vacancy_trudvsem,
    check_received_data_trudvsem
)


logger_api_trudvsem = logging.getLogger(__name__)


def parce_vacancies_msk_spb_trudvsem(
    list_vacancies: list[dict], location: str
) -> dict:
    """
    Обработка данных о вакансиях, полученных от api trudvsem.ru.
    Данные обрабатываются перед сохранением данных в БД
    и показом пользователю краткой информации о найденных вакансиях.
    """
    for vacancies in list_vacancies:
        check_result = check_received_data_trudvsem(response_data=vacancies)
        if not check_result.get('status'):
            return {'status': False}

    vacancy_data = [
        item
        for sublist in list_vacancies
        for item in sublist.get('results').get('vacancies')
    ]
    pattern = rf'(?i)\b{location}\b'
    vacancies_lst = []
    for vacancy in vacancy_data:
        vacancy_location = (
            vacancy.get('vacancy')
            .get('addresses')
            .get('address')[ParameterRequestTrudvsem.FIRST_ELEMENT_LIST]
            .get('location')
        )
        if re.search(pattern, vacancy_location):
            contact_list = vacancy.get('vacancy').get('contact_list')
            if contact_list:
                contact_phone_number = contact_list[
                    ParameterRequestTrudvsem.FIRST_ELEMENT_LIST
                ].get('contact_value')
            else:
                contact_phone_number = (
                    'Работодатель не указал контактный номер телефона'
                )
            vacancies_lst.append(
                {
                    'vacancy_name': vacancy.get('vacancy').get('job-name'),
                    'salary': 'Работодатель не указал заработную плату.'
                    if vacancy.get('vacancy').get('salary') is None
                    else vacancy.get('vacancy').get('salary'),
                    'vacancy_source': 'Работа России',
                    'vacancy_url': vacancy.get('vacancy').get('vac_url'),
                    'employer_name': vacancy.get('vacancy')
                    .get('company')
                    .get('name'),
                    'employer_location': vacancy.get('vacancy')
                    .get('addresses')
                    .get('address')[
                        ParameterRequestTrudvsem.FIRST_ELEMENT_LIST
                    ]
                    .get('location'),
                    'employer_phone_number': contact_phone_number,
                    'company_code': vacancy.get('vacancy')
                    .get('company')
                    .get('companycode'),
                    'vacancy_id': vacancy.get('vacancy').get('id'),
                }
            )
    return {'status': True, 'vacancies_lst': vacancies_lst}


def parce_vacancy_trudvsem(vacancy: dict) -> dict:
    """
    Обработка данных о вакансии, полученных от api trudvsem.ru.
    Данные обрабатываются для показа пользователю подробной
    информации о конкретной вакансии (кнопка подробнее).
    """

    vacancy_data = (
        vacancy.get('results')
        .get('vacancies')[ParameterRequestTrudvsem.FIRST_ELEMENT_LIST]
        .get('vacancy')
    )
    if not vacancy_data:
        logger_api_trudvsem.critical(
            'Не получилось получить информацию о вакансии, '
            'полученную от сайта trudvsem.ru'
        )
        return {'status': False}
    check_result = check_received_data_one_vacancy_trudvsem(
        vacancy_data=vacancy_data
    )
    if not check_result.get('status'):
        return {'status': False}

    if vacancy_data.get('duty'):
        duty = (
            re.sub(r"<[^>]+>", "", vacancy_data.get('duty'), flags=re.S)
            .replace('&nbsp;', '')
            .replace('&nbsp', '')
        )
    else:
        duty = 'Работодатель не указал должностные обязанности'
    vacancy = {
        'vacancy_name': vacancy_data.get('job-name'),
        'vacancy_id': vacancy_data.get('id'),
        'vacancy_url': vacancy_data.get('vac_url'),
        'social_protected': vacancy_data.get('social_protected'),
        'vacancy_source': 'Работа России',
        'description': duty,
        'employer_location': vacancy_data.get('addresses')
        .get('address')[ParameterRequestTrudvsem.FIRST_ELEMENT_LIST]
        .get('location'),
        'salary': 'Работодатель не указал заработную плату.'
        if vacancy_data.get('salary') is None
        else vacancy_data.get('salary'),
        'employer_name': vacancy_data.get('company').get('name'),
        'company_code': vacancy_data.get('company').get('companycode'),
        'employer_phone_number': ('Работодатель не указал свой номер телефона')
        if vacancy_data.get('company').get('phone') is None
        else vacancy_data.get('company').get('phone'),
        'employer_email': 'Работодатель не указал адрес электронной почты.'
        if vacancy_data.get('company').get('email') is None
        else vacancy_data.get('company').get('email'),
    }
    return {'status': True, 'vacancy': vacancy}


async def parce_vacancies_user_location_trudvsem(
    list_vacancies: list[dict], location: str, applicant_tg_id: str
) -> dict:
    """
    Обработка данных о вакансиях, полученных от API trudvsem.ru.
    Данные обрабатываются перед сохранением данных в БД
    и показом пользователю краткой информации о найденных вакансиях.
    """
    for vacancies in list_vacancies:
        check_result = check_received_data_trudvsem(vacancies)
        if not check_result.get('status'):
            return {'status': False}

    vacancy_data = [
        item
        for sublist in list_vacancies
        for item in sublist.get('results').get('vacancies')
    ]
    pattern = rf'(?i)\b{location}\b'
    vacancies_lst = []
    for vacancy in vacancy_data:
        vacancy_location = (
            vacancy.get('vacancy')
            .get('addresses')
            .get('address')[ParameterRequestTrudvsem.FIRST_ELEMENT_LIST]
            .get('location')
        )
        if re.search(pattern, vacancy_location):
            contact_list = vacancy.get('vacancy').get('contact_list')
            if contact_list:
                contact_phone_number = contact_list[
                    ParameterRequestTrudvsem.FIRST_ELEMENT_LIST
                ].get('contact_value')
            else:
                contact_phone_number = (
                    'Работодатель не указал контактный номер телефона'
                )
            vacancies_lst.append(
                {
                    'applicant_tg_id': applicant_tg_id,
                    'vacancy_name': vacancy.get('vacancy').get('job-name'),
                    'salary': 'Работодатель не указал заработную плату.'
                    if vacancy.get('vacancy').get('salary') is None
                    else vacancy.get('vacancy').get('salary'),
                    'vacancy_source': 'Работа России',
                    'vacancy_url': vacancy.get('vacancy').get('vac_url'),
                    'employer_name': vacancy.get('vacancy')
                    .get('company')
                    .get('name'),
                    'employer_location': vacancy.get('vacancy')
                    .get('addresses')
                    .get('address')[
                        ParameterRequestTrudvsem.FIRST_ELEMENT_LIST
                    ]
                    .get('location'),
                    'employer_phone_number': contact_phone_number,
                    'company_code': vacancy.get('vacancy')
                    .get('company')
                    .get('companycode'),
                    'vacancy_id': vacancy.get('vacancy').get('id'),
                }
            )
    return {'status': True, 'vacancies_lst': vacancies_lst}
