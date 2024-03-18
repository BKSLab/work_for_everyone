# Telegram bot "Работа для всех"

**Ссылка на бот:** https://t.me/work_for_all_people_bot  

**Презентация проекта на сайте touch-it.ru доступна по ссылке:** https://touch-it.ru/telegram-bot-work-for-everyone-release/  
**Презентация проекта на канале в Дзен доступна по ссылке:** https://dzen.ru/a/ZfgAwUd_kxpphX41  
**Публикации о ходе разработки проекта на сайте touch-it.ru:** https://touch-it.ru/category/telegram-bot/  

## Примечание!
Telegram bot находится на стадии тестирования.

## Описание
**Работа для всех** – Telegram bot предоставляет интерфейс для поиска, просмотра и добавления понравившихся вакансий в избранное.  
Все вакансии являются вакансиями для людей с инвалидностью, опубликованными на портале [«Работа России»](https://trudvsem.ru/) и представленные через открытый [API](https://trudvsem.ru/opendata/api).


**Telegram bot Работа для всех позволяет:**
- искать вакансии в указанном пользователем населенном пункте,
- просматривать информацию о найденных вакансиях,
- получать подробную информацию о конкретной вакансии,
- добавлять вакансии в избранное.


## Описание команд, доступных при работе с ботом:
- **/start** (Начать работу) - старт работы с ботом.
- **/help** (Справка по работе с ботом) - пользователь получает подробную справку по алгоритму работы с ботом.
- **/favorites** (Перейти в избранное) - команда используется для перехода к сохраненным пользователем вакансиям.
- **/cancel** (Завершение работы) - завершает работу с ботом.
- **/feedback** (Обратная связь) - переход в раздел с описанием способов, как и где можно оставить отзыв на работу бота.

Описанные команды доступны как из меню бота, так и путем ввода команд в текстовое поле ввода Telegram клиента.


## Алгоритм работы Telegram бота:
1. Работа с ботом начинается активацией команды **/start**. В ответ на эту команду бот поприветствует пользователя по имени и даст краткую инструкцию по работе с ботом.
Кроме инструкции бот подскажет, что подробную информацию о работе с ботом и поддерживаемых коммандах пользователь может узнать по команде **/help** или нажав кнопку **"Справка по боту"**.  
Кроме непосредственно справки о работе с ботом, по команде **/help** пользователь получает кнопку **"Начать ввод данных"**, которая, как и кнопка **"Готов начать"** запускает основную логику бота.

2. После активации команды **/start** кроме информационного сообщения бот покажет пользователю три кнопки:
- **"Готов начать"**
- **"Справка по боту"**
- **"Перейти в избранное"**

3. Активация кнопки **"Справка по боту"** реагирует аналогично команде **/help**.

4. Нажатие кнопки **"Готов начать"** запускает основную логику работы бота.

5. Пользователь поэтапно выбирает из списка:
    - название федерального округа. Это нужно, чтобы на следующем этапе бот предоставил пользователю список субъектов РФ, которые входят в указанный федеральный округ;
    - название субъекта РФ. На этом этапе бот предоставляет возможность вернуться на предыдущий шаг, если пользователь неправильно укажет название федерального округа.

6. После выбора федерального округа и региона пользователь должен ввести название населенного пункта, в котором он хочет найти вакансию. 
Название населенного пункта вводится без указания его типа (город, село, деревня и т.п.). Об этом пользователь предупреждается в соответствующем информационном сообщении.

7. После того как пользователь ввел наименование населенного пункта бот осуществляет валидацию введенных данных. 
В частности, проверяет, что в названии населенного пункта используется только кириллица, а также не используются цифры и другие специальные символы кроме дефиса. 
Дефис часто используется в названии населенных пунктов в России. Проверке также подлежит количество введенных слов, так как в России нет населенных пунктов, в названии которых 
присутствовало бы больше двух слов и одного предлога. В том случае, если название населенного пункта введено пользователем со строчной буквы, то бот преобразует первые буквы названия в заглавные. 

8. При успешной валидации бот выдает пользователю сообщение с введенными данными для повторной проверки пользователем их корректности. Также пользователь видит две кнопки:
    - **"Начать поиск вакансий"**
    - **"Ввести данные заново"** (на случай ошибочно введенных данных)

9. Если при валидации названия населенного пункта будут выявлены ошибки, бот указывает пользователю на это и повторно предлагает указать название населенного пункта со справкой по правилам ввода.

10. Активация кнопки **"Начать поиск вакансий"** запускает модуль бота, отвечающий за формирование и отправку запроса к [API](https://trudvsem.ru/opendata/api).
В том случае, если GET запрос был выполнен успешно, в таблицу с данными о вакансиях записываются найденные для данного пользователя вакансии.

11. При нажатии кнопки **"Начать поиск вакансий"** пользователь получает также сообщение, что начался поиск вакансий и что это может занять какое-то время. 
На этом же этапе пользователь получает краткую справку по работе со списком вакансий.

12. В случае неудачного запроса или проблем, связанных с работой API, пользователь получит сообщение об этом.

13. По результатам поиска пользователю сообщается о количестве найденных вакансий, а также показываются первые 10 найденных вакансий при нажатии кнопки **"Показать вакансии"**
Далее пользователь может листать списки найденных вакансий как вперед, так и назад. Эта функция реализована через пагинацию.

14. Каждая вакансия представляет собой отдельное сообщение. Под каждой вакансией есть две кнопки:
    - **"Добавить в избранное"**
    - **"Подробнее"**

15. Пример описания вакансии в списке вакансий:
    - **Должность:** Начальник отдела учета расходов
    - **Заработная плата:** от 50000
    - **Работодатель:** АО "УДМУРТАВТОДОРСТРОЙ"
    - **Адрес работодателя:** Удмуртская республика, г Ижевск, Олега Кошевого улица, 18
    - **Номер телефона работодателя:** +7(341) 290-88-10
    - **Электронная почта:** info@autodor.org

16. Пример подробного описания вакансии:
    - Подробные сведения о вакансии:
    - **Должность:** Начальник отдела учета расходов
    - **Вакансия из категории:** Инвалиды
    - Данные о заработной плате:
        - **Минимальная заработная плата:** 19 242
        - **Максимальный размер заработной платы:** 20 000
    - **Должностные обязанности:** В соответствии с должностной инструкцией и трудовым договором.
    - Информация о работодателе:
        - **Наименование работодателя:** АО "УДМУРТАВТОДОРСТРОЙ"
        - **Контактное лицо:** Иванов Иван Иванович
        - **Номер телефона работодателя:** +7(341) 290-88-10
        - **Электронная почта:** info@autodor.org
        - **Адрес работодателя:** Удмуртская республика, г Ижевск, Олега Кошевого улица, 18

17. Нажатие кнопки **"Добавить в избранное"** добавляет вакансию в избранное. Вакансии, добавленные в избранное, хранятся после окончания сессии, и пользователь может всегда вернуться к ним.

18. После того как пользователь просмотрел подробную информацию о вакансии, он может вернуться обратно к списку вакансий для дальнейшего их просмотра.

19. По окончании работы с ботом все данные о найденных вакансиях, которые записывались в БД, кроме вакансий, добавленных в избранное, удаляются. 


## Стэк технологии
- Python: 3.11
- Peewee: 3.16.3
- Aiogram: 3.1.1
- Docker и Docker Compose

Подробнее с используемыми зависимостями вы можете ознакомиться в файле [requirements.txt](https://github.com/BKSLab/work_for_everyone/blob/main/bot/requirements.txt)

## Deploy проекта на сервере
- установить Docker и Docker compose
- создать директорию для проекта, перейти в нее
- скопировать (создать) файлы: docker-compose.yml и .env (пример файла .env см. в файле [.env.example](https://github.com/BKSLab/work_for_everyone/blob/main/.env.example))
- поднять docker контейнеры командой docker compose up -d

## Об авторе проекта
Меня зовут Барабанщиков Кирилл, я python backend разработчик.

## Мои контакты
- Telegram: https://t.me/Kirill_Barabanshchikov
- почта: bks2408@mail.ru
