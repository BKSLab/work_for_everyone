def msg_verification(data: dict[str, str | int]) -> str:
    """
    Формирование проверочного сообщения для пользователя
    перед началом поиска вакансий.
    """
    return (
        f'{data.get("name_applicant")}, давай проверим введённые данные.\n\n'
        'Если данные не верны, то жми кнопку <b>"Ввести данные заново"</b>.\n'
        'Если всё верно, жми кнопку <b>"Начать поиск вакансий"</b>\n\n'
        '<b>Проверяем данные:\n</b>'
        f'<b>Федеральный округ:</b> {data.get("fd_code")}\n'
        f'<b>Название выбранного региона:</b> {data.get("region_name")}\n'
        f'<b>Номер выбранного региона:</b> {data.get("region_code")}\n'
        f'<b>Наименование населённого пункта:</b> {data.get("location")}'
    )


def msg_info_vacancy(vacancy: dict[str, str | int]) -> str:
    """
    Формирование сообщения с краткой информацией о вакансии
    для показа пользователю в списке вакансий.
    """
    return (
        f'<b>Должность:</b> {vacancy.get("vacancy_name")}\n\n'
        f'<b>Источник вакансии:</b> {vacancy.get("vacancy_source")}\n\n'
        f'<b>Заработная плата:</b> {vacancy.get("salary")}\n'
        f'<b>Работодатель:</b> {vacancy.get("employer_name")}\n'
        f'<b>Контактный телефон:</b> '
        f'{vacancy.get("employer_phone_number")}\n'
    )


def msg_info_vacancy_favorites(
    vacancy: dict[str, str | int],
    status_information: str
) -> str:
    """
    Формирование сообщения с краткой информацией о вакансии
    для показа пользователю в списке вакансий в избранном.
    """
    return (
        f'<b>Статус</b>: {status_information}\n\n'
        f'<b>Должность:</b> {vacancy.get("vacancy_name")}\n\n'
        f'<b>Источник вакансии:</b> {vacancy.get("vacancy_source")}\n\n'
        f'<b>Заработная плата:</b> {vacancy.get("salary")}\n'
        f'<b>Работодатель:</b> {vacancy.get("employer_name")}\n'
        f'<b>Контактный телефон:</b> '
        f'{vacancy.get("employer_phone_number")}\n'
    )


def msg_details_info_vacancy(vacancy: dict[str, str | int]) -> str:
    """Формирование сообщения с подробной информацией о вакансии."""
    return (
        '<b>Подробные сведения о вакансии:</b>\n\n'
        f'<b>Должность:</b> {vacancy.get("vacancy_name")}\n'
        f'<b>Вакансия для людей с инвалидностью</b>\n\n'
        f'<b>Источник вакансии:</b> {vacancy.get("vacancy_source")}\n\n'
        f'<b>Размер заработной платы:</b> {vacancy.get("salary")}\n\n'
        f'<b>Должностные обязанности:</b>\n{vacancy.get("description")}.\n\n'
        '<b>Информация о работодателе:</b>\n'
        f'<b>Наименование работодателя:</b> {vacancy.get("employer_name")}\n'
        f'<b>Номер телефона работодателя:</b> '
        f'{vacancy.get("employer_phone_number")}\n'
        f'<b>Электронная почта:</b> {vacancy.get("employer_email")}\n'
        f'<b>Адрес работодателя:</b> {vacancy.get("employer_location")}\n'
    )
