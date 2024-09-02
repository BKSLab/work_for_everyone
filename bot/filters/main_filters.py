import json
import re
from math import ceil
from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from data_operations.get_data import get_data_lst_regions
from database.redis import redis
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
        # Получение списка кодов федеральных округов
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
        # Получение данных из хранилища Redis о номере федерального округа,
        # который пользователь выбрал на предыдущем этапе
        data_redis = await redis.get(
            f'fsm:{str(callback.from_user.id)}:'
            f'{str(callback.from_user.id)}:data'
        )
        fd_code = json.loads(data_redis).get('fd_code')

        # Подумать над тем, как переместить поиск регионов в хендлер
        # Получение списка регионов в выбранном пользователе ФО.
        result = get_data_lst_regions(fd_code)
        if not result.get('status'):
            return False
        regions = result.get('data_regions')
        for region in regions:
            if (
                callback.data == region[1]
                and callback.data != '77'
                and callback.data != '78'
            ):
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

    async def __call__(self, callback: CallbackQuery) -> bool:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if data[1] == 'details':
            return True


class CollapseDetailedFilter(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Свернуть'.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if data[1] == 'collapse':
            return True


class DeleteVacancyFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Удалить из избранного'.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if data[1] == 'delete':
            return True


class ShowManyVacanciesFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопок пагинации.
    """
    async def __call__(
        self, callback: CallbackQuery
    ) -> Union[bool, dict[str, int]]:
        if '_' not in callback.data:
            return False
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
