from data_operations.delete_data import deleting_vacancy_user_location
from data_operations.get_data import get_count_vacancies_user_location
from data_operations.get_msk_spb_data import get_count_vacancies_msk_spb
from data_operations.save_data import saving_vacancies_big_data
from loading_vacancies.endpoints import ParameterRequestTrudvsem
from loading_vacancies.trudvsem.data_processing_trudvsem import (
    parce_vacancies_msk_spb_trudvsem,
    parce_vacancies_user_location_trudvsem,
    parce_vacancy_trudvsem
)
from loading_vacancies.trudvsem.request_api_trudvsem import (
    get_one_vacancy_trudvsem,
    get_vacancies_api_trudvsem_user_location,
    get_vacancies_trudvsem_msk_spb,
)
from database.models import Vacancy, VacancyMSK, VacancySPB


async def load_one_vacancy_trudvsem(
    vacancy_id: str, company_code: str
) -> dict:
    """
    Управление загрузкой и обработкой данных об одной вакансии с api hh.ru.
    """
    api_result = get_one_vacancy_trudvsem(
        company_code=company_code, vacancy_id=vacancy_id
    )
    if not api_result.get('status') and 'vacancy_status' in api_result:
        return {'status': False, 'vacancy_status': 'does_not_exist'}

    if not api_result.get('status'):
        return {'status': False}

    preparing_result = parce_vacancy_trudvsem(
        vacancy=api_result.get('vacancy')
    )
    if not preparing_result.get('status'):
        return {'status': False}
    return {'status': True, 'vacancy': preparing_result.get('vacancy')}


def load_vacancy_from_trudvsem_msk():
    """
    Управление загрузкой и обработкой данных о вакансиях
    в Москве с api trudvsem.ru.
    """
    data_vacancies_from_api = get_vacancies_trudvsem_msk_spb(
        reg_code_trudvsem=ParameterRequestTrudvsem.REG_CODE_TRUDVSEM_MSK
    )
    # Проверка результата запроса к api
    if not data_vacancies_from_api.get('status'):
        return {'status': False}

    # Подготовка данных для записи в БД
    processing_result = parce_vacancies_msk_spb_trudvsem(
        list_vacancies=data_vacancies_from_api.get('vacancy_lst'),
        location='Москва',
    )
    if not processing_result.get('status'):
        return {'status': False}

    # Сохранение данных о вакансиях в Москве в БД
    query_result = saving_vacancies_big_data(
        data_vacancies=processing_result.get('vacancies_lst'),
        model=VacancyMSK
    )
    if not query_result.get('status'):
        return {'status': False}

    # Получение информации о количестве загруженных
    # вакансиях в Москве с сайта trudvsem.ru
    query_count_result = get_count_vacancies_msk_spb(
        vacancy_source='Работа России', model=VacancyMSK
    )
    if not query_count_result.get('status'):
        return {'status': False}

    return {
        'status': True,
        'count_vacancy_msk': query_count_result.get('count_vacancies'),
    }


def load_vacancy_from_trudvsem_spb():
    """
    Управление загрузкой и обработкой данных о вакансиях
    в Санкт-Петербурге с api trudvsem.ru.
    """
    data_vacancies_from_api = get_vacancies_trudvsem_msk_spb(
        reg_code_trudvsem=ParameterRequestTrudvsem.REG_CODE_TRUDVSEM_SPB
    )

    # Проверка результата запроса к api
    if not data_vacancies_from_api.get('status'):
        return {'status': False}

    # Подготовка данных для записи в БД
    processing_result = parce_vacancies_msk_spb_trudvsem(
        list_vacancies=data_vacancies_from_api.get('vacancy_lst'),
        location='Санкт-Петербург',
    )
    if not processing_result.get('status'):
        return {'status': False}

    # Сохранение данных о вакансиях в Москве в БД
    query_result = saving_vacancies_big_data(
        data_vacancies=processing_result.get('vacancies_lst'),
        model=VacancySPB
    )
    if not query_result.get('status'):
        return {'status': False}

    # Получение информации о количестве загруженных
    # вакансиях в Санкт-Петербурге с сайта trudvsem.ru
    query_count_result = get_count_vacancies_msk_spb(
        vacancy_source='Работа России', model=VacancySPB
    )
    if not query_count_result.get('status'):
        return {'status': False}

    return {
        'status': True,
        'count_vacancy_spb': query_count_result.get('count_vacancies'),
    }


async def load_vacancy_trudvsem_user_location(
    reg_code_trudvsem: str, user_location: str, user_tg_id: str
) -> dict:
    """
    Управление загрузкой и обработкой данных о вакансиях в пользовательской
    локации с api trudvsem.ru.
    """

    # Получение от API trudvsem.ru вакансий в пользовательской локации
    data_vacancies_from_api = get_vacancies_api_trudvsem_user_location(
        reg_code_trudvsem=reg_code_trudvsem
    )

    # Проверка результата запроса к api
    if not data_vacancies_from_api.get('status'):
        return {'status': False}

    # Подготовка данных для записи в БД
    processing_result = await parce_vacancies_user_location_trudvsem(
        list_vacancies=data_vacancies_from_api.get('vacancy_lst'),
        location=user_location,
        applicant_tg_id=user_tg_id,
    )

    # Проверка результата обработки данных о вакансиях перед их записью в БД
    if not processing_result.get('status'):
        return {'status': False}

    # удаление вакансий пользователя, ранее добавленных в БД
    query_result_deleting = deleting_vacancy_user_location(
        user_tg_id=user_tg_id, vacancy_source='Работа России'
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
        vacancy_source='Работа России',
    )
    if not query_count_result.get('status'):
        return {'status': False}
    return {
        'status': True,
        'count_vacancy': query_count_result.get('count_vacancies'),
    }
