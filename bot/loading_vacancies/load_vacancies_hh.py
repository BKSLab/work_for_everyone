import aiohttp
from data_operations.delete_data import deleting_vacancy_user_location
from data_operations.get_data import get_count_vacancies_user_location
from data_operations.get_msk_spb_data import get_count_vacancies_msk_spb
from data_operations.save_data import saving_vacancies_big_data
from database.models import Vacancy, VacancyMSK, VacancySPB
from loading_vacancies.endpoints import ParameterRequestHH
from loading_vacancies.hh.data_processing_hh import (
    parce_vacancies_msk_spb_hh,
    parce_vacancies_user_location_hh,
    parce_vacancy_hh,
)
from loading_vacancies.hh.request_api_hh import (
    get_one_vacancy_hh,
    get_vacancies_api_hh_user_location,
    get_vacancies_hh_msk_spb,
)


async def load_vacancy_user_location_hh(
    reg_code_hh: str, user_location: str, user_tg_id: str
) -> dict:
    """
    Управление загрузкой и обработкой данных о вакансиях в пользовательской
    локации с api hh.ru.
    """
    async with aiohttp.ClientSession() as session:
        data_vacancies_from_api = await get_vacancies_api_hh_user_location(
            session=session,
            reg_code_hh=reg_code_hh,
            user_location=user_location
        )

    # Проверка результата запроса к api
    if not data_vacancies_from_api.get('status'):
        return {'status': False}

    # Подготовка данных для записи в БД
    processing_result = await parce_vacancies_user_location_hh(
        list_vacancies=data_vacancies_from_api.get('vacancy_lst'),
        location=user_location,
        applicant_tg_id=user_tg_id,
    )

    # Проверка результата обработки данных о вакансиях перед их записью в БД
    if not processing_result.get('status'):
        return {'status': False}

    # удаление вакансий пользователя, ранее добавленных в БД
    query_result_deleting = deleting_vacancy_user_location(
        user_tg_id=user_tg_id, vacancy_source='hh.ru'
    )
    if not query_result_deleting.get('status'):
        return {'status': False}

    # Сохранение данных о вакансиях в пользовательской локации в БД
    query_result = saving_vacancies_big_data(
        data_vacancies=processing_result.get('vacancies_lst'), model=Vacancy
    )
    if not query_result.get('status'):
        return {'status': False}

    # Получение информации о количестве загруженных
    # вакансиях в пользовательской локации
    query_count_result = get_count_vacancies_user_location(
        user_tg_id=user_tg_id,
        vacancy_source='hh.ru',
    )
    if not query_count_result.get('status'):
        return {'status': False}
    return {
        'status': True,
        'count_vacancy': query_count_result.get('count_vacancies'),
    }


async def load_one_vacancy_hh(vacancy_id: str) -> dict:
    """
    Управление загрузкой и обработкой данных об одной вакансии с api hh.ru.
    """
    # запрос к api сайта hh.ru для получения полной информации о вакансии
    api_result = get_one_vacancy_hh(vacancy_id=vacancy_id)
    if not api_result.get('status'):
        return {'status': False}

    if api_result.get('status') and 'vacancy_status' in api_result:
        vacancy_status = api_result.get('vacancy_status')
        if vacancy_status == 'archival':
            vacancy = parce_vacancy_hh(vacancy=api_result.get('vacancy'))
            return {
                'status': True,
                'vacancy_status': 'archival',
                'vacancy': vacancy,
            }
        if vacancy_status == 'actual':
            vacancy = parce_vacancy_hh(vacancy=api_result.get('vacancy'))
            return {
                'status': True,
                'vacancy_status': 'actual',
                'vacancy': vacancy,
            }
        if vacancy_status == 'does_not_exist':
            return {'status': True, 'vacancy_status': 'does_not_exist'}


def load_vacancy_from_hh_msk() -> dict:
    """
    Управление загрузкой и обработкой данных о вакансиях в Москве с api hh.ru.
    """
    # Загрузка вакансий в Москве по линиям метро
    for line_id in ParameterRequestHH.METRO_LINES_MSK:
        # Получение вакансий в Москве по каждой линии метро
        data_vacancies_from_api = get_vacancies_hh_msk_spb(
            reg_code_hh=ParameterRequestHH.REG_CODE_HH_MSK,
            parametr_name=ParameterRequestHH.PARAMETR_NAME_HH_MSK,
            parametr_id=line_id,
        )
        # Проверка результата запроса к api
        if not data_vacancies_from_api.get('status'):
            return {'status': False}

        # Подготовка данных для записи в БД
        processing_result = parce_vacancies_msk_spb_hh(
            vacancies=data_vacancies_from_api.get('vacancy_lst'),
            employer_location='Москва',
        )

        if not processing_result.get('status'):
            return {'status': False}

        # Сохранение данных о вакансиях в Москве в БД
        query_result = saving_vacancies_big_data(
            data_vacancies=processing_result.get('vacancies_lst'),
            model=VacancyMSK,
        )
        if not query_result.get('status'):
            return {'status': False}

    # Получение информации о количестве загруженных
    # вакансиях в Москве с сайта hh.ru
    query_count_result = get_count_vacancies_msk_spb(
        vacancy_source='hh.ru', model=VacancyMSK
    )
    if not query_count_result.get('status'):
        return {'status': False}

    return {
        'status': True,
        'count_vacancy_msk': query_count_result.get('count_vacancies'),
    }


def load_vacancy_from_hh_spb():
    """
    Управление загрузкой и обработкой данных о вакансиях
    в Санкт-Петербурге с api hh.ru.
    """

    # Загрузка вакансий в Москве по линиям метро
    for experience_id in ParameterRequestHH.EXPERIENS_SPB:
        # Получение вакансий в Москве по каждой линии метро
        data_vacancies_from_api = get_vacancies_hh_msk_spb(
            reg_code_hh=ParameterRequestHH.REG_CODE_HH_SPB,
            parametr_name=ParameterRequestHH.PARAMETR_NAME_HH_SPB,
            parametr_id=experience_id,
            # location=location,
        )
        # Проверка результата запроса к api
        if not data_vacancies_from_api.get('status'):
            return {'status': False}

        # Подготовка данных для записи в БД
        processing_result = parce_vacancies_msk_spb_hh(
            vacancies=data_vacancies_from_api.get('vacancy_lst'),
            employer_location='Санкт-Петербург',
        )
        if not processing_result.get('status'):
            return {'status': False}
        # Сохранение данных о вакансиях в Санкт-Петербурге в БД
        query_result = saving_vacancies_big_data(
            data_vacancies=processing_result.get('vacancies_lst'),
            model=VacancySPB,
        )
        if not query_result.get('status'):
            return {'status': False}

    # Получение информации о количестве загруженных
    # вакансиях в Санкт-Петербургес сайта hh.ru
    query_count_result = get_count_vacancies_msk_spb(
        vacancy_source='hh.ru', model=VacancySPB
    )
    if not query_count_result.get('status'):
        return {'status': False}
    return {
        'status': True,
        'count_vacancy_spb': query_count_result.get('count_vacancies'),
    }
