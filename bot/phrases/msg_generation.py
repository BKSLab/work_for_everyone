def msg_verification(data: dict[str, str | int]) -> str:
    """
    Формирование проверочного сообщения для пользователя,
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
        f'<b>Наименование населённого пункта:</b> {data.get("location")},\n'
    )


def msg_info_vacancy(vacancy: dict[str, str | int]) -> str:
    """
    Формирование сообщения с краткой информацией о вакансии,
    для показа пользователю в списке вакансий.
    """
    return (
        f'<b>Должность:</b> {vacancy.get("vacancy_name")};\n\n'
        f'<b>Заработная плата:</b> {vacancy.get("salary")};\n'
        f'<b>Работодатель:</b> {vacancy.get("employer_name")};\n'
        f'<b>Адресс работодателя:</b> {vacancy.get("employer_location")}\n'
        f'<b>Номер телефона работодателя:</b> '
        f'{vacancy.get("employer_phone_number")}\n'
        f'<b>Электронная почта:</b> {vacancy.get("employer_email")}\n'
    )


def msg_details_info_vacancy(vacancy: dict[str, str | int]) -> str:
    """Формирование сообщения с подробной информацией о вакансии."""
    return (
        'Подробные свдения о вакансии:\n\n'
        f'Должность: {vacancy.get("vacancy_name")};\n\n'
        f'Дата публикации вакансии: {vacancy.get("creation_date")};\n'
        f'Вакансия из категории: {vacancy.get("social_protected")}.\n\n'
        'Данные о заработной плате:\n'
        f'Минимальная заработная плата: {vacancy.get("salary_min")};\n'
        f'Максимальный размер заработной платы: '
        f'{vacancy.get("salary_max")};\n\n'
        f'Должностные обязанности:\n{vacancy.get("duty")}.\n\n'
        'Информация о работодателе:\n'
        f'Наименование работодателя: {vacancy.get("employer_name")};\n'
        f'Контактное лицо: {vacancy.get("contact_person")};\n'
        f'Номер телефона работодателя: '
        f'{vacancy.get("employer_phone_number")};\n'
        f'Электронная почта: {vacancy.get("employer_email")};\n'
        f'Адресс работодателя: {vacancy.get("employer_location")}.\n'
    )
