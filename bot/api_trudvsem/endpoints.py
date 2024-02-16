from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoint:
    """URL адреса, используемые для обращения к API."""

    ENDPOINT_REGION: str = (
        'http://opendata.trudvsem.ru/api/v1/vacancies/region/'
    )
    ONE_VACANCY_ENDPOINT: str = (
        'http://opendata.trudvsem.ru/api/v1/vacancies/vacancy'
    )


@dataclass(frozen=True)
class ParameterRequest:
    """Параметры запроса, используемые для обращения к API."""

    SOCIAL_PROTECTED: str = 'Инвалиды'
    VACANCIES_PER_ONE_PAGE: int = 100
    FIRST_ELEMENT_LIST: int = 0
