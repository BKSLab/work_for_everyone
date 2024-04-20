import json
import re
from math import ceil
from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from database.redis import redis
from database.views import (
    get_data_regions,
    get_vacancy,
    get_vacancy_from_favorites,
)
from phrases.texts_for_bot_buttons import ButtonData


class StartDataEntryFilter(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопок,
    отвечающих за запуск основной логики бота.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data in [
            'ready',
            'data_input',
            'back_to_selection_f_d',
            're_enter_data',
        ]:
            return True
        return False


class FederalDistrictFilter(BaseFilter):
    """Фильтр для перехвата номера федерального округа."""

    async def __call__(self, callback: CallbackQuery) -> bool:
        if not callback.data.isdigit():
            return False
        codes = [code[1] for code in ButtonData.federal_districts]
        if int(callback.data) in codes:
            return True
        return False


class RegionFilter(BaseFilter):
    """
    Фильтр для перехвата номеров регионов
    в выбранном федеральном округе.
    """

    async def __call__(
        self, callback: CallbackQuery
    ) -> Union[bool, dict[str, str]]:
        if not callback.data.isdigit():
            return False
        data_redis = await redis.get(
            f'fsm:{str(callback.from_user.id)}:'
            f'{str(callback.from_user.id)}:data'
        )
        fd_code = json.loads(data_redis).get('fd_code')
        regions = get_data_regions(fd_code)
        for region in regions:
            if int(callback.data) in region:
                return {'region_name': region[0]}
        return False


class NameLocalityFilter(BaseFilter):
    """
    Фильтр для обработки названия ннаселенного пункта,
    введенного пользователем.
    """

    async def __call__(self, message: Message) -> Union[bool, dict[str, str]]:
        if message.text.lower() in [
            'москва',
            'санкт-Петербург',
            'Севастополь',
        ]:
            return False
        if '-' in message.text:
            split_message = message.text.split('-')
            hyphen = True
        else:
            split_message = message.text.split()
            hyphen = False
        if (
            len(split_message) <= 3
            and all(
                symbol.isspace() or symbol.isalpha()
                for symbol in (part_name for part_name in split_message)
            )
            and re.search(r'^[А-Яа-яЁё\s\-]+\Z', message.text)
        ):
            if hyphen:
                return {
                    'locality_name': '-'.join(
                        el_str.capitalize() for el_str in split_message
                    ),
                }
            return {
                'locality_name': ' '.join(
                    el_str.capitalize() for el_str in split_message
                ),
            }
        return False


class DetailsFilter(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Подробнее'.
    """

    async def __call__(self, callback: CallbackQuery) -> Union[bool, dict]:
        data = callback.data.split('_')
        if not list(set(data) & set(['details', 'details.fav'])):
            return False
        if data[1] == 'details':
            mode = 'details'
            vacancy_id = data[0]
            vacancy = get_vacancy(vacancy_id, callback.from_user.id)
        elif data[1] == 'details.fav':
            mode = 'details.fav'
            vacancy_id = data[0]
            vacancy = get_vacancy_from_favorites(
                vacancy_id, callback.from_user.id
            )
        if not vacancy:
            return False
        return {'vacancy': vacancy.__dict__.get('__data__'), 'mode': mode}


class CollapseDetailedFilter(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Свернуть'.
    """

    async def __call__(self, callback: CallbackQuery) -> Union[bool, dict]:
        data = callback.data.split('_')
        if not list(set(data) & set(['collapse', 'collapse.fav'])):
            return False
        if data[1] == 'collapse':
            mode = 'collapse'
            vacancy_id = data[0]
            vacancy = get_vacancy(vacancy_id, callback.from_user.id)
        elif data[1] == 'collapse.fav':
            mode = 'collapse.fav'
            vacancy_id = data[0]
            vacancy = get_vacancy_from_favorites(
                vacancy_id, callback.from_user.id
            )
        if not vacancy:
            return False
        return {'vacancy': vacancy.__dict__.get('__data__'), 'mode': mode}


class AddVacancyFavoritesFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Добавить в избранного'.
    """

    async def __call__(self, callback: CallbackQuery) -> Union[bool, dict]:
        data = callback.data.split('_')
        if 'favorites' not in data:
            return False
        vacancy = get_vacancy(data[0], callback.from_user.id)
        if not vacancy:
            return False
        return {
            'vacancy': vacancy.__dict__.get('__data__'),
        }


class DeleteVacancyFavoritesFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Удалить из избранного'.
    """

    async def __call__(self, callback: CallbackQuery) -> Union[bool, dict]:
        data = callback.data.split('_')
        if not list(set(data) & set(['delete', 'delete.fav'])):
            return False

        vacancy = get_vacancy_from_favorites(data[0], callback.from_user.id)
        if not vacancy:
            return False
        return {'vacancy': vacancy.__dict__.get('__data__'), 'mode': data[1]}


class ShowManyVacanciesFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопок пагинации.
    """

    async def __call__(
        self, callback: CallbackQuery
    ) -> Union[bool, dict[str, int]]:
        data = callback.data.split('_')
        if not list(set(data) & set(['many', 'next', 'back'])):
            return False
        data_redis = await redis.get(
            f'fsm:{str(callback.from_user.id)}:'
            f'{str(callback.from_user.id)}:data'
        )
        count_pages = ceil(json.loads(data_redis).get('count_vacancies') / 10)
        page_number = int(data[-1])
        if 1 > page_number > count_pages:
            return False
        return {'page_number': page_number}


class FavoritesFilterr(BaseFilter):
    """
    Фильтр для перехода пользователя в избранное'.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'favorites':
            return True
        return False


class KeywordFilter(BaseFilter):
    """
    Фильтр для обработки введенного пользователем
    ключевого слова для уточненного поиска вакансий.
    """

    async def __call__(self, message: Message) -> bool:
        keyword = message.text
        data_redis = await redis.get(
            f'fsm:{str(message.from_user.id)}:'
            f'{str(message.from_user.id)}:data'
        )
        status_keyword = json.loads(data_redis).get('status_keyword')
        if status_keyword != 1:
            return False
        if all(
            symbol.isspace() or symbol.isalpha() or symbol == '-'
            for symbol in keyword
        ) and re.search(r'^[А-Яа-яЁё\s\-]+\Z', keyword):
            return True
        return False


class ShowManyVacanciesByKeywordFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопок пагинации при
    показе вакансий, найденных по ключевому слову.
    """

    async def __call__(
        self, callback: CallbackQuery
    ) -> Union[bool, dict[str, int]]:
        data = callback.data.split('_')
        if not list(
            set(data)
            & set(
                [
                    'show-many-vacancies-by-keyword',
                    'next-keyword',
                    'back-keyword',
                ]
            )
        ):
            return False
        data_redis = await redis.get(
            f'fsm:{str(callback.from_user.id)}:'
            f'{str(callback.from_user.id)}:data'
        )
        count_pages = ceil(
            json.loads(data_redis).get('count_vacancies_by_keyword') / 10
        )
        page_number = int(data[-1])
        if 1 > page_number > count_pages:
            return False
        return {'page_number': page_number}
