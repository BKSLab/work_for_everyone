from dataclasses import dataclass


@dataclass
class ButtonData:
    """Данные для создания inline кнопок."""

    show_many_vacancies: tuple[str, str] = (
        'Показать вакансии',
        'show_many_vacancies_1',
    )
    show_few_vacancies: tuple[str, str] = (
        'Показать вакансии',
        'show_few_vacancies',
    )
    ready: tuple[str, str] = ('Готов начать', 'ready')
    ready_favorites: tuple[str, str] = ('Поиск вакансий', 'ready')
    bot_help: tuple[str, str] = ('Справка по боту', 'bot_help')
    data_input: tuple[str, str] = ('Начать ввод данных', 'data_input')
    favorites: tuple[str, str] = ('Перейти в избранное', 'favorites')
    re_enter_data: tuple[str, str] = ('Ввести данные заново', 're_enter_data')
    federal_districts: tuple[tuple[str, int], ...] = (
        ('Центральный федеральный округ', 30),
        ('Северо-Западный федеральный округ', 31),
        ('Приволжский федеральный округ', 33),
        ('Уральский федеральный округ', 34),
        ('Северо-Кавказский федеральный округ', 38),
        ('Южный федеральный округ', 40),
        ('Сибирский федеральный округ', 41),
        ('Дальневосточный федеральный округ', 42),
    )
    back_to_selection_f_d: tuple[str, str] = (
        'Вернуться к выбору ФО',
        'back_to_selection_f_d',
    )
    start_searching: tuple[str, str] = (
        'Начать поиск вакансий',
        'start_searching',
    )
    commands_data: tuple[tuple[str, str], ...] = (
        ('/start', 'Начать работу'),
        ('/help', 'Справка по работе с ботом'),
        ('/favorites', 'Перейти в избранное'),
        ('/cancel', 'Завершить работу'),
        ('/feedback', 'Обратная связь'),
    )
    feedback: tuple[str, str] = ('Обратная связь', 'feedback_from_author')
