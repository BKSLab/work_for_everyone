import re


def clean_html_from_dict(data: dict[str, str | int]) -> dict[str, str | int]:
    """Очистка HTML-тегов из всех строковых значений в словаре."""
    cleaned_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Удаляем все HTML-теги
            cleaned_value = re.sub(r'<[^>]+>', '', value, flags=re.S)
            cleaned_data[key] = cleaned_value
        else:
            cleaned_data[key] = value
    return cleaned_data


def msg_verification(data: dict[str, str]) -> str:
    """
    Формирование проверочного сообщения для пользователя
    перед началом поиска вакансий.
    """
    return (
        f'{data.get("name_applicant")}, давай проверим введённые данные.\n\n'
        'Если данные не верны, то жми кнопку <b>"Ввести данные заново"</b>.\n'
        'Если всё верно, жми кнопку <b>"Начать поиск вакансий"</b>\n\n'
        '<b>Проверяем данные:\n</b>'
        f'<b>Регион:</b> {data.get("region_name")}\n'
        f'<b>Населенный пункт:</b> {data.get("location")}'
    )


def msg_info_vacancy(vacancy: dict[str, str | int]) -> str:
    """
    Формирование сообщения с краткой информацией о вакансии
    для показа пользователю в списке вакансий.
    """
    vacancy_cl = clean_html_from_dict(data=vacancy)
    return (
        f'<b>Должность:</b> {vacancy_cl.get("vacancy_name")}\n\n'
        f'<b>Источник вакансии:</b> {vacancy_cl.get("vacancy_source")}\n\n'
        f'<b>Заработная плата:</b> {vacancy_cl.get("salary")}\n'
        f'<b>Работодатель:</b> {vacancy_cl.get("employer_name")}\n'
        f'<b>Контактный телефон:</b> '
        f'{vacancy_cl.get("employer_phone_number")}\n'
    )


def msg_info_vacancy_favorites(
    vacancy: dict[str, str | int],
    status_information: str
) -> str:
    """
    Формирование сообщения с краткой информацией о вакансии
    для показа пользователю в списке вакансий в избранном.
    """
    vacancy_cl = clean_html_from_dict(data=vacancy)
    return (
        f'<b>Статус</b>: {status_information}\n\n'
        f'<b>Должность:</b> {vacancy_cl.get("vacancy_name")}\n\n'
        f'<b>Источник вакансии:</b> {vacancy_cl.get("vacancy_source")}\n\n'
        f'<b>Заработная плата:</b> {vacancy_cl.get("salary")}\n'
        f'<b>Работодатель:</b> {vacancy_cl.get("employer_name")}\n'
        f'<b>Контактный телефон:</b> '
        f'{vacancy_cl.get("employer_phone_number")}\n'
    )


def msg_details_info_vacancy(vacancy: dict[str, str | int]) -> str:
    """Формирование сообщения с подробной информацией о вакансии."""
    # Очищаем словарь от HTML-тегов
    vacancy_cl = clean_html_from_dict(data=vacancy)
    return (
        '<b>Подробные сведения о вакансии:</b>\n\n'
        f'<b>Должность:</b> {vacancy_cl.get("vacancy_name")}\n'
        f'<b>Вакансия для людей с инвалидностью</b>\n\n'
        f'<b>Источник вакансии:</b> {vacancy_cl.get("vacancy_source")}\n\n'
        f'<b>Размер заработной платы:</b> {vacancy_cl.get("salary")}\n\n'
        f'<b>Должностные обязанности:</b>\n{vacancy_cl.get("description")}.'
        '\n\n<b>Информация о работодателе:</b>\n'
        f'<b>Наименование работодателя:</b> {vacancy_cl.get("employer_name")}'
        f'\n<b>Номер телефона работодателя:</b> '
        f'{vacancy_cl.get("employer_phone_number")}\n'
        f'<b>Электронная почта:</b> {vacancy_cl.get("employer_email")}\n'
        f'<b>Адрес работодателя:</b> {vacancy_cl.get("employer_location")}\n'
    )
