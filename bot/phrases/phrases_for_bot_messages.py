from dataclasses import dataclass


@dataclass
class BotCommandPhrases:
    """
    Тексты, используемые для показа пользователю при активации команд бота.
    """

    start_command: str = (
        '<b>{user_name}, привет!\n\n</b>Я помогаю найти работу людям с '
        'инвалидностью.\nТы готов начать поиск вакансий?\n\n'
        'Если да, то жми кнопку <b>"Готов начать"</b>\n\n'
        'Если нужна справка, ты всегда можешь воспользоваться командой /help\n'
        'или нажать кнопку <b>"Справка по боту"</b>\n\nТы также можешь '
        'перейти в избранное, нажав кнопку <b>"Перейти в избранное"</b>'
    )
    help_command: str = (
        '<b>{user_name}</b>, вот, что я могу!\n\n'
        '<b>Telegram bot Работа для всех позволяет:</b>\n'
        '- искать вакансии в указанном пользователем населенном пункте;\n'
        '- просматривать список вакансий;\n'
        '- получать подробную информацию о конкретной вакансии;\n'
        '- добавлять вакансии в избранное.\n\n'
        '<b>Как получить список интересующих вакансий:</b>\n'
        '1. Выбери из списка федеральный округ.\n'
        '2. Выбери из списка регион.\n'
        '3. Введи название населенного пункта (город, село, поселок и т.п.), '
        'в котором ты хотел бы посмотреть вакансии.\n'
        '4. Проверь введенные данные. Если всё верно, жми кнопку '
        '<b>"Начать поиск вакансий"</b>.\n'
        '5. Если в данных ошибка, жми <b>"Ввести данные заново"</b>.\n\n'
        'Вакансии будут показываться списком, по 10 вакансий за один раз.'
        'Ты можешь листать список вакансий как вперёд, так и назад.\n'
        'Под каждой вакансией будут две кнопки: '
        '<b>"Добавить в избранное"</b> и <b>"Подробнее"</b>\n\n'
        'После просмотра подробной информации о вакансии ты можешь вернуться '
        'обратно к списку вакансий.\n\n'
        'После того как будет закончена работа с ботом, все найденные '
        'вакансии будут удалены, кроме тех вакансий, которые добавлены '
        'в <b>избранное</b>. Они будут доступны, '
        'пока ты сам их не удалишь.\n\n'
        '<b>Доступные команды в боте:</b>\n'
        '- /start - начало работы с ботом;\n'
        '- /help - получить справку по работе с ботом;\n'
        '- /cancel - завершение работы с ботом;\n'
        '- /favorites - посмотреть вакансии, добавленные в избранное\n'
        '- /feedback - обратная связь по работе с ботом.\n\n'
        '<b>Вперёд!!!</b>'
    )
    feedback_command: str = (
        '<b>{user_name}, привет!</b>\n\nЯ очень рад, что ты воспользовался '
        'ботом и заглянул сюда. Это здорово, благодарю тебя!\n\n'
        'Если у тебя есть замечания по работе бота, не '
        'стесняйся, пиши мне в '
        '<a href="tg://user?id=482235727">Telegram</a>\n\n'
        'Ты можешь поддержать бот, рассказав о нем своим друзьям в '
        'социальных сетях или лично при встрече.\n\n'
        'Поддержать проект можно и финансово: аренда хостинга '
        'стоит денег и требует оплаты ежемесячно.\n\n'
        'Ты можешь сделать перевод по СБП по номеру: +79124646606 '
        '(банк Сбер или Т-Банк).\nПолучатель: '
        'Барабанщиков Кирилл Сергеевич. (то есть я)\n\n'
        'Дело это исключительно добровольное! '
        'Любая денежка, даже самая маленькая, будет в помощь!\n\n'
        'Желаю тебе удачи в поиске работы! У тебя всё получится!'
    )
    cancel_command: str = (
        '<b>{user_name}</b>, работа со мной завершена успешно!\n\n'
        'Если хочешь начать все заново, жми <b>"Начать ввод данных"</b>\n'
        'Если нужна справка по боту, жми <b>"Справка по боту"</b>\n\n'
        '<b>И это еще не все!</b>\nНе забывай, что все сохраненные '
        'тобой вакансии находятся в избранном\n'
        'Перейти в избранное можно с помощью команды /favorites '
        'или нажав кнопку <b>"Перейти в избранное"</b>'
    )


@dataclass
class BotErrorMessages:
    """
    Тексты, используемые для показа пользователю сообщений об ошибках.
    """

    favorites_error: str = (
        '{user_name}, к сожалению, но в ходе работы с вакансиями, '
        'добавленными в избранное, произошла ошибка.\nПожалуйста, свяжитесь '
        'с <a href="tg://user?id=482235727">автором бота</a> "Работа для всех"'
    )
    data_error: str = (
        '{user_name}, к сожалению, но в ходе работы с данными, '
        'произошла ошибка.\nПожалуйста, свяжитесь '
        'с <a href="tg://user?id=482235727">автором бота</a> "Работа для всех"'
    )
    trudvsem_request_error: str = (
        '{user_name}, к сожалению, но при обращении к сайту "Работа России" '
        'произошла оошибка.\nПожалуйста, свяжитесь '
        'с <a href="tg://user?id=482235727">автором бота</a> "Работа для всех"'
    )
    hh_request_error: str = (
        "{user_name}, к сожалению, но при обращении к сайту hh.ru "
        'произошла оошибка.\nПожалуйста, свяжитесь '
        'с <a href="tg://user?id=482235727">автором бота</a> "Работа для всех"'
    )
    main_request_error: str = (
        '{user_name}, к сожалению, но при поиске вакансий в указанном '
        'тобой населенном пункте, произошла ошибка gпри загрузки '
        'вакансий.\nПожалуйста, свяжитесь '
        'с <a href="tg://user?id=482235727">автором бота</a> "Работа для всех"'
    )
    reply_unprocessed_msg: str = (
        '{user_name}, прошу прощения, но я получил сообщение, которое не могу '
        'обработать!\n\nНе забывай, ты всегда можешь получить справку '
        'по работе с ботом, отправив команду /help или нажав кнопку '
        '<b>"Справка по боту"</b>'
    )
    federal_district_wrong: str = (
        '{user_name}, на данном этапе тебе необходимо выбрать федеральный '
        'округ из списка федеральных округов, который я только что тебе '
        'отправил.\nНичего страшного, давай попробуем еще раз!'
    )
    region_name_wrong: str = (
        '{user_name}, на данном этапе тебе необходимо выбрать регион '
        'из списка регионов, который я только что тебе отправил.\n'
        'Ничего страшного, давай попробуем еще раз!'
    )
    name_locality_wrong: str = (
        '{user_name}, к сожалению, введенные тобой символы не могут сложиться '
        'в наименование населенного пункта в России. Попробуй еще раз!\n\n'
        'Ранее ты ввел: {user_location}'
    )
    data_checking_wrong: str = (
        '{user_name}, на этом шаге ничего вводить не требуется!\n\n'
        'Сейчас давай проверим введенные данные. Если всё верно, '
        'жми кнопку <b>"Начать поиск вакансий"</b>\n\n'
        'Если вдруг что-то не так, можно вернуться к первому шагу. '
        'Для этого жми кнопку <b>"Ввести данные заново"</b>'
    )


@dataclass
class BotHandlerMessages:
    """
    Тексты, используемые для показа пользователю сообщений.
    """

    no_vacancies_in_favorites: str = (
        '{user_name}, пока ты не добавил(а) ни одной вакансии в избранное!\n\n'
        'Уверен, что это легко исправить.Готов помочь тебе в поиске доступных '
        'вакансий.\nДля того чтобы начать поиск вакансий, жми кнопку '
        '<b>"Готов начать"</b>\nЕсли нужна справка по работе с ботом, '
        'жми кнопку <b>"Справка по боту"</b>'
    )
    message_in_favorites: str = (
        '{user_name}, ты добавил(а) {vacancies_count} вакансий в избранное.'
        '\n\nНаходясь в избранном ты можешь просматривать информацию о '
        'вакансиях, а при необходимости перейти на страницу '
        'с вакансией для отклика.\n\nДля перехода к поиску вакансий '
        'жми кнопку: <b>"Начать ввод данных"</b>\n'
        'Если нужна справка по работе с ботом, жми кнопку '
        '<b>"Справка по боту"</b>'
    )
    vacancy_deleted: str = 'Вакансия {vacancy_name} удалена из избранного'
    choice_federal_districts: str = (
        '{user_name}, пора сделать первый шаг!\n\nВыбери из списка '
        'федеральный округ, в котором ты хотел(а) бы посмотреть вакансии.\n'
        'Если ты вдруг ошибешься, на следующем шаге '
        'можно будет вернуться назад.'
    )
    choice_region_name: str = (
        '{user_name}, отлично!\n\nТеперь нужно выбрать из списка название, '
        'интереcующего тебя региона.\nЕсли был выбран не тот '
        'федеральный округ, жми кнопку <b>"Вернуться к выбору ФО"</b>'
    )
    input_name_locality: str = (
        '{user_name}, на этом шаге нужно ввести название населенного пункта, '
        'в котором тебе хотелось бы посмотреть вакансии.\n\n'
        '<b>Обрати внимание!</b>\nНазвание населенного пункта необходимо '
        'вводить кириллицей с большой буквы. '
        'Не используй в названии цифры и буквы латинского алфавита, а также '
        'не пиши тип населенного пункта (город, село, поселок и т.п.)'
    )
    search_vacancies: str = (
        '{user_name}, я начинаю поиск вакансий. Для получения данных и их '
        'обработки мне понадобится время.\n\nВ списке найденных вакансий '
        'ты можешь посмотреть подробную информацию о каждой вакансии, '
        'а также добавить вакансию в избранное\n\n'
        'Надеюсь, поиск завершится удачно!'
    )
    vacancies_not_found: str = (
        '{user_name}, по твоему запросу ничего не удалось найти. '
        'Попробуй ввести данные еще раз и проверь правильность '
        'названия населенного пункта, который ты ввёл.\n\n'
        'Ранее ты ввёл: {user_location}'
    )
    show_vacancies: str = (
        '{user_name}, {total_vacancies} - вот столько вакансий в '
        '{user_location} удалось найти.\n\n{count_vacancy_trudvsem} - на '
        'сайте Работа России\n{count_vacancy_hh} - на сайте hh.ru\n\n'
        'Для того чтобы посмотреть вакансии, жми кнопку '
        '<b>"Показать все вакансии"</b>.\nВ списке показывается по 10 '
        'вакансий. Используй кнопки <b>"Назад"</b> и <b>"Вперед"</b> '
        'для перемещения между списками с вакансиями.\n\n'
        'Кроме того, ты можешь уточнить поиск по ключевому слову, '
        'для этого жми кнопку <b>"Поиск по ключевому слову"</b>'
    )
    show_completed: str = (
        '{user_name}, доступные вакансии закончились.\n\nТы можешь посмотреть '
        'вакансии, добавленные в избранное, нажав на кнопку '
        '<b>"Перейти в избранное"</b>\nТы также можешь начать поиск заново, '
        'нажав на кнопку <b>"Ввести данные заново"</b>.'
    )
    show_information: str = (
        '{user_name}, показано {vacancies_shown} из {count_vacancies} '
        'найденных вакансий\n\nИспользуй для навигации кнопки '
        '<b>"Вперед"</b> и <b>"Назад"</b>.\nПодходящие вакансии можешь '
        "добавлять в избранное."
    )
    show_vacancies_msk_spb: str = (
        '{user_name}, мне удалось найти {total} вакансий в городе {city}:\n'
        '- {count_hh} - на сайте hh.ru\n'
        '- {count_trud} - на сайте "Работа России"\n\n'
        'Конечно, ты можешь посмотреть все вакансии, нажав на кнопку '
        '<b>"Показать все вакансии"</b>, но у меня есть другой план.\n'
        'Я предлагаю искать подходящие для тебя вакансии по ключевому слову, '
        'для этого жми кнопку <b>"Поиск по ключевому слову"</b>. ВПЕРЁД!'
    )
    keyword_search_info: str = (
        '{user_name}, в режиме поиска вакансий по ключевому слову ты можешь '
        'найти именно те вакансии, которые тебя интересуют.\n\n'
        'В качестве ключевого слова ты можешь ввести '
        'название профессии (экономист, повар, монтажник и т.п.).\n\n'
        'Не стоит вводить символы на английском языке '
        'и использовать специальные символы.\n\n'
        'Если вакансий по твоему запросу не будет найдено, ты можешь '
        'посмотреть полный список вакансий, нажав на '
        'кнопку <b>"Показать все вакансии"</b>, '
        'либо снова ввести другое ключевое слово для повторного поиска.'
    )
    vacancies_not_found_by_keyword: str = (
        '{user_name}, мне не удалось найти вакансии по ключевому слову: '
        '<b>{keyword}</b>\n\nТы можешь ввести другое ключевое слово для '
        'поиска, нажав кнопку <b>"Поиск по ключевому слову"</b>, или '
        'перейти к просмотру всех вакансий, найденных в указанной тобой '
        'местности. Для этого жми кнопку <b>"Показать все вакансии"</b>'
    )
    show_vacancies_by_keyword: str = (
        '{user_name}, {total_vacancies} - вот столько вакансий по ключевому '
        'слову <b>{keyword}</b> удалось найти\n\nДля того чтобы посмотреть '
        'вакансии, жми кнопку <b>"Показать вакансии"</b>.\n'
    )
    show_completed_by_keyword: str = (
        '{user_name}, доступные вакансии закончились.\n\nТы можешь ввести '
        'другое ключевое слово для поиска, нажав кнопку '
        '<b>"Поиск по ключевому слову"</b>, либо посмотреть полный список '
        'найденных вакансий, нажав кнопку <b>"Показать все вакансии"</b>.\n'
        'Ты можешь перейти в избранное, чтобы посмотреть свои вакансии.'
    )
    show_information_by_keyword: str = (
        '{user_name}, показано {vacancies_shown} из {count_vacancies} '
        'найденных по ключевому слову {keyword} вакансий\n\nИспользуй '
        'для навигации кнопки <b>"Вперед"</b> и <b>"Назад"</b>.\n'
        'Подходящие вакансии можешь добавлять в избранное.'
    )
