PHRASES_FOR_MESSAGE = {
    'start_command': (
        ', привет!\n\n</b>Я помогаю найти работу людям с инвалидностью.\n'
        'Ты готов начать поиск вакансий?\n\n'
        'Если да, то жми кнопку <b>"Готов начать"</b>\n\n'
        'Если нужна справка, ты всегда можешь воспользоваться командой /help\n'
        'или нажать кнопку <b>"Справка по боту"</b>\n\n'
        'Ты также можешь перейти в избранное, '
        'нажав кнопку <b>"Перейти в избранное"</b>'
    ),
    'help_command': (
        ', вот, что я могу!\n\n'
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
    ),
    'choice_federal_districts': (
        ', пора сделать первый шаг!\n\nВыбери из списка федеральный округ, в '
        'котором ты хотел(а) бы посмотреть вакансии.\n'
        'Если ты вдруг ошибешься, на следующем шаге '
        'можно будет вернуться назад.'
    ),
    'choice_region_name': (
        ', отлично!\n\nТеперь нужно выбрать из списка название, '
        'интереcующего тебя региона.\n'
        'Если был выбран не тот '
        'федеральный округ, жми кнопку <b>"Вернуться к выбору ФО"</b>'
    ),
    'input_name_locality': (
        ', на этом шаге нужно ввести название населенного пункта, '
        'в котором тебе хотелось бы посмотреть вакансии.\n\n'
        '<b>Обрати внимание!</b>\nНазвание населенного пункта необходимо '
        'вводить кириллицей с большой буквы. '
        'Не используй в названии цифры и буквы латинского алфавита, а также '
        'не пиши тип населенного пункта (город, село, поселок и т.п.)'
    ),
    'process_of_searching': (
        ', я начинаю поиск вакансий. Для получения данных и их обработки '
        'мне понадобится какое-то время.\n\n'
        'В списке найденных вакансий ты можешь посмотреть '
        'подробную информацию о каждой вакансии, '
        'а также добавить вакансию в избранное\n\n'
        'Надеюсь, поиск завершится удачно!'
    ),
    'show_vacancies': (
        ' - вот столько вакансий в указанном населенном пункте '
        'удалось найти\n\nДля того чтобы посмотреть вакансии, '
        'жми кнопку <b>"Показать вакансии"</b>.\n'
        'В списке показывается по 10 вакансий. Используй кнопки '
        '<b>"Назад"</b> и <b>"Вперед"</b>'
        'для перемещения между списками с вакансиями.'
    ),
    'vacancies_not_found': (
        'по вашему запросу ничего не удалось найти. '
        'Попробуй ввести данные еще раз и проверь правильность '
        'названия населенного пункта, который ты ввёл.\n\n'
        'Ранее ты ввёл: '
    ),
    'show_completed': (
        ', доступные вакансии закончились.\n\n'
        'Ты можешь посмотреть вакансии, добавленные в избранное, '
        'нажав на кнопку <b>"Перейти в избранное"</b>\n'
        'Ты также можешь начать поиск заново, нажав на кнопку '
        '<b>"Ввести данные заново"</b>.'
    ),
    'no_vacancies_in_favorites': (
        ', пока ты не добавил(а) ни одной вакансии в избранное!\n\n'
        'Уверен, что это легко исправить. '
        'Готов помочь тебе в поиске доступных вакансий.\n'
        'Для того чтобы начать поиск вакансий, жми кнопку '
        '<b>"Готов начать"</b>\n'
        'Если нужна справка по работе с ботом, '
        'жми кнопку <b>"Справка по боту"</b>'
    ),
    'message_in_favorites': (
        ', находясь в избранном ты можешь просматривать '
        'краткую и подробную информацию о добавленных вакансиях.\n\n'
        'Если нужно перейти к поиску вакансий, '
        'жми кнопку: <b>"Начать ввод данных"</b>\n'
        'Если нужна справка по работе с ботом, жми кнопку '
        '<b>"Справка по боту"</b>'
    ),
    'cancel': (
        ', работа со мной завершена успешно!\n\n'
        'Если хочешь начать все заново, жми <b>"Начать ввод данных"</b>\n'
        'Если нужна справка по боту, жми <b>"Справка по боту"</b>\n\n'
        '<b>И это еще не все!</b>\n'
        'Не забывай, что все сохраненные тобой вакансии находятся в '
        'избранном\n'
        'Перейти в избранное можно с помощью команды /favorites '
        'или нажав кнопку <b>"Перейти в избранное"</b>'
    ),
    'federal_district_wrong': (
        ', на данном этапе тебе необходимо выбрать федеральный округ '
        'из списка федеральных округов, который я только что тебе отправил.\n'
        'Ничего страшного, давай попробуем еще раз! Всё получится!'
    ),
    'region_name_wrong': (
        ', на данном этапе тебе необходимо выбрать регион '
        'из списка регионов, который я только что тебе отправил.\n'
        'Ничего страшного, давай попробуем еще раз! Всё получится!'
    ),
    'name_locality_wrong': (
        ', к сожалению, введенные тобой символы не могут сложиться '
        'в наименование населенного пункта в России. Попробуй еще раз!\n\n'
        'Вот, что ты ввел в качестве наименования населенного пункта:\n- '
    ),
    'data_checking_wrong': (
        ', на этом шаге ничего вводить не требуется!\n\n'
        'Сейчас давай проверим введенные данные. Если всё верно, '
        'жми кнопку <b>"Начать поиск вакансий"</b>\n\n'
        'Если вдруг что-то не так, можно вернуться к первому шагу. '
        'Для этого жми кнопку <b>"Ввести данные заново"</b>'
    ),
    'other_answer': (
        ', прошу прощения, но я получил сообщение, которое не могу '
        'обработать!\n\nНе забывай, ты всегда можешь получить справку '
        'по работе с ботом, отправив команду /help или нажав кнопку '
        '<b>"Справка по боту"</b>'
    ),
    'feedback': (
        ', привет!</b>\n\nЯ очень рад, что ты воспользовался ботом и '
        'заглянул сюда. Это здорово, благодарю тебя!\n\n'
        'Если у тебя есть замечания по работе бота, не '
        'стесняйся, пиши мне в '
        '<a href="tg://user?id=482235727">Telegram</a>\n\n'
        'Ты можешь поддержать бот, рассказав о нем своим друзьям в '
        'социальных сетях или лично при встрече.\n\n'
        'Поддержать проект можно и финансово: аренда хостинга '
        'стоит денег и требует оплаты ежемесячно.\n\n'
        'Ты можешь сделать перевод по СБП по номеру: +79124646606 '
        '(банк Сбер или Тинькофф).\nПолучатель: '
        'Барабанщиков Кирилл Сергеевич. (то есть я)\n\n'
        'Дело это исключительно добровольное! '
        'Любая денежка, даже самая маленькая, будет в помощь!\n\n'
        'Желаю тебе удачи в поиске работы! У тебя всё получится!'
    ),
}
