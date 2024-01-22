def message_generation(data: dict[str, str | int]) -> str:
    return (
        f'{data.get("name_applicant")}, давай проверим введённые данные.\n\n'
        'Если данные не верны, то жми кнопку "Ввести данные заново".\n'
        'Если всё верно, жми кнопку "Начать поиск вакансий"\n\n'
        '<b>Проверяем данные:\n</b>'
        f'Федеральный округ: {data.get("fd_code")}\n'
        f'Название выбранного региона: {data.get("region_name")}\n'
        f'Номер выбранного региона: {data.get("region_code")}\n'
        f'Наименование населённого пункта: {data.get("location")},\n'
    )
