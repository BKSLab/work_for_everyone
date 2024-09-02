import logging
import re

from loading_vacancies.hh.check_api_hh_responce import check_received_data_hh


logger_api_hh = logging.getLogger(__name__)


def parce_vacancies_msk_spb_hh(
    vacancies: list[dict], employer_location: str
) -> dict:
    """
    Обработка данных о вакансиях, полученных от api hh.ru.
    Данные обрабатываются перед сохранением данных в БД
    и показом пользователю краткой информации о найденных вакансиях.
    """
    vacancies_lst = []

    # Проход по полученному списку вакансий. на каждой итерации
    # обрабатывается словарь с данными о вакансии
    for vacancy in vacancies:
        # проверка полученных данных для их определения возможности
        # их последующей обработки и добавления в итоговый список
        check_result = check_received_data_hh(response_data=vacancy)
        if not check_result.get('status'):
            return {'status': False, 'error': check_result.get('error')}
        if vacancy.get('salary') is None:
            salary = 'Работодатель не указал заработную плату'
        if vacancy.get('salary') and vacancy.get('salary').get('from'):
            salary = f'от {vacancy.get("salary").get("from")}'
        if vacancy.get('salary') and vacancy.get('salary').get('to'):
            salary = f'до {vacancy.get("salary").get("to")}'
        if (
            vacancy.get('salary')
            and vacancy.get('salary').get('from')
            and vacancy.get('salary').get('to')
        ):
            salary = (
                f'от {vacancy.get("salary").get("from")} '
                f'до {vacancy.get("salary").get("to")}'
            )
        employer_name = (
            vacancy.get('employer')
            .get('name')
            .replace('Job development', '')
            .replace('(', '')
            .replace(')', '')
        )
        if vacancy.get('contacts') is None:
            employer_phone_number = 'Работодатель не указал номер телефон'
        elif not vacancy.get('contacts').get('phones'):
            employer_phone_number = 'Работодатель не указал номер телефон'
        elif not vacancy.get('contacts').get('phones')[0].get('formatted'):
            employer_phone_number = 'Работодатель не указал номер телефон'
        else:
            phones = vacancy.get('contacts').get('phones')[0]
            employer_phone_number = phones.get('formatted')
        if not vacancy.get('employer').get('id'):
            company_code = 'Код работодателя не указан'
        else:
            company_code = vacancy.get('employer').get('id')
        vacancies_lst.append(
            {
                'vacancy_name': vacancy.get('name'),
                'salary': salary,
                'employer_name': employer_name,
                'company_code': company_code,
                'employer_phone_number': employer_phone_number,
                'vacancy_source': 'hh.ru',
                'employer_location': employer_location,
                'vacancy_url': vacancy.get('alternate_url'),
                'vacancy_id': vacancy.get('id'),
            }
        )

    return {'status': True, 'vacancies_lst': vacancies_lst}


def parce_vacancy_hh(vacancy: dict) -> dict:
    """
    Обработка данных о вакансии, полученных от api hh.ru.
    Данные обрабатываются для показа пользователю подробной
    информации о конкретной вакансии (кнопка подробнее).
    """
    data = {}
    if vacancy.get('salary') is None:
        salary = 'Работодатель не указал заработную плату'
    if vacancy.get('salary') and vacancy.get('salary').get('from'):
        salary = f'от {vacancy.get("salary").get("from")}'
    if vacancy.get('salary') and vacancy.get('salary').get('to'):
        salary = f'до {vacancy.get("salary").get("to")}'
    if (
        vacancy.get('salary')
        and vacancy.get('salary').get('from')
        and vacancy.get('salary').get('to')
    ):
        salary = (
            f'от {vacancy.get("salary").get("from")} до '
            f'{vacancy.get("salary").get("to")}'
        )
    description_row = re.sub(
        r'<[^>]+>', '', vacancy.get('description'), flags=re.S
    )
    if len(description_row) > 500:
        description = (
            description_row[:500]
            + '...(Полный текст описания смотри на сайте)'
        )
    else:
        description = description_row
    employer_name = vacancy.get('employer').get('name')

    if vacancy.get('address') is None:
        employer_location = 'Работодатель не указал адрес'
    if vacancy.get('address') and not vacancy.get('address').get('raw'):
        employer_location = 'Работодатель не указал адрес'
    if vacancy.get('address') and vacancy.get('address').get('raw'):
        employer_location = vacancy.get('address').get('raw')

    if vacancy.get('contacts') is None:
        employer_email = 'Работодатель не указал email'
        employer_phone_number = 'Работодатель не указал номер телефона'
    else:
        employer_email = (
            'Работодатель не указал email'
            if vacancy.get('contacts').get('email') is None
            else vacancy.get('contacts').get('email')
        )
        employer_phone_number = (
            'Работодатель не указал номер телефона'
            if not vacancy.get('contacts').get('phones')
            else vacancy.get('contacts').get('phones')[0]
        )

    data['vacancy_name'] = vacancy.get('name')
    data['social_protected'] = 'Инвалиды'
    data['vacancy_source'] = 'hh.ru'
    data['salary'] = salary
    data['description'] = description
    data['employer_name'] = employer_name
    data['employer_phone_number'] = employer_phone_number
    data['employer_email'] = employer_email
    data['employer_location'] = employer_location
    data['vacancy_id'] = vacancy.get('id')
    data['vacancy_url'] = vacancy.get('alternate_url')

    return data


async def parce_vacancies_user_location_hh(
    list_vacancies: list[dict], location: str, applicant_tg_id: str
) -> dict:
    """
    Обработка данных о вакансиях, полученных от API hh.ru.
    Данные обрабатываются перед сохранением данных в БД
    и показом пользователю краткой информации о найденных вакансиях.
    """

    # Список для добавления информации об обработанных вакансиях
    vacancies_lst = []

    # Проход по полученному списку вакансий. на каждой итерации
    # обрабатывается словарь с данными о вакансии
    for vacancy in list_vacancies:
        # проверка полученных данных для их определения возможности
        # их последующей обработки и добавления в итоговый список
        check_result = check_received_data_hh(response_data=vacancy)
        if not check_result.get('status'):
            return {'status': False, 'error': check_result.get('error')}
        if vacancy.get('salary') is None:
            salary = 'Работодатель не указал заработную плату'
        if vacancy.get('salary') and vacancy.get('salary').get('from'):
            salary = f'от {vacancy.get("salary").get("from")}'
        if vacancy.get('salary') and vacancy.get('salary').get('to'):
            salary = f'до {vacancy.get("salary").get("to")}'
        if (
            vacancy.get('salary')
            and vacancy.get('salary').get('from')
            and vacancy.get('salary').get('to')
        ):
            salary = (
                f'от {vacancy.get("salary").get("from")} '
                f'до {vacancy.get("salary").get("to")}'
            )
        employer_name = (
            vacancy.get('employer')
            .get('name')
            .replace('Job development', '')
            .replace('(', '')
            .replace(')', '')
        )
        if vacancy.get('contacts') is None:
            employer_phone_number = 'Работодатель не указал номер телефон'
        elif not vacancy.get('contacts').get('phones'):
            employer_phone_number = 'Работодатель не указал номер телефон'
        elif not vacancy.get('contacts').get('phones')[0].get('formatted'):
            employer_phone_number = 'Работодатель не указал номер телефон'
        else:
            phones = vacancy.get('contacts').get('phones')[0]
            employer_phone_number = phones.get('formatted')
        if not vacancy.get('employer').get('id'):
            company_code = 'Код работодателя не указан'
        else:
            company_code = vacancy.get('employer').get('id')
        vacancies_lst.append(
            {
                'applicant_tg_id': applicant_tg_id,
                'vacancy_name': vacancy.get('name'),
                'salary': salary,
                'employer_name': employer_name,
                'company_code': company_code,
                'employer_phone_number': employer_phone_number,
                'vacancy_source': 'hh.ru',
                'employer_location': location,
                'vacancy_url': vacancy.get('alternate_url'),
                'vacancy_id': vacancy.get('id'),
            }
        )

    return {'status': True, 'vacancies_lst': vacancies_lst}
