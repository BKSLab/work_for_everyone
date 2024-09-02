from dataclasses import dataclass


@dataclass(frozen=True)
class EndpointHH:
    """URL адреса, используемые для обращения к API hh.ru."""

    VACANCY_URL: str = 'https://api.hh.ru/vacancies/'


@dataclass(frozen=True)
class ParameterRequestHH:
    """Параметры запроса, используемые для обращения к API hh.ru."""

    SOCIAL_PROTECTED_HH: str = 'accept_handicapped'
    VACANCIES_PER_ONE_PAGE_HH: int = 100

    # Параметры для обращения к api hh.ru для загрузки вакансий в МСК
    REG_CODE_HH_MSK: int = 1
    PARAMETR_NAME_HH_MSK: str = 'metro'
    METRO_LINES_MSK: tuple[int] = (
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        95,
        96,
        97,
        98,
        131,
        132,
        133,
        135,
        136,
    )

    # Параметры для обращения к api hh.ru для загрузки вакансий в СПБ
    REG_CODE_HH_SPB: int = 2
    PARAMETR_NAME_HH_SPB: str = 'experience'
    EXPERIENS_SPB: tuple[str] = (
        'noExperience',
        'between1And3',
        'between3And6',
        'moreThan6',
    )


@dataclass(frozen=True)
class EndpointTrudvsem:
    """URL адреса, используемые для обращения к API."""

    ENDPOINT_REGION: str = (
        'http://opendata.trudvsem.ru/api/v1/vacancies/region/'
    )
    ONE_VACANCY_ENDPOINT: str = (
        'http://opendata.trudvsem.ru/api/v1/vacancies/vacancy'
    )


@dataclass(frozen=True)
class ParameterRequestTrudvsem:
    """Параметры запроса, используемые для обращения к API."""

    SOCIAL_PROTECTED: str = 'Инвалиды'
    VACANCIES_PER_ONE_PAGE: int = 100
    FIRST_ELEMENT_LIST: int = 0

    # Параметры для обращения к api hh.ru для загрузки вакансий в МСК
    REG_CODE_TRUDVSEM_MSK: int = 77
    REG_CODE_TRUDVSEM_SPB: int = 78
