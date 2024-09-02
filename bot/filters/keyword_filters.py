import json
import re
from math import ceil
from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from database.redis import redis


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


class KeywordMSKSPBFilter(BaseFilter):
    """
    Фильтр для обработки введенного пользователем
    ключевого слова для уточненного поиска
    вакансий в Москве и Санкт-Петербурге.
    """

    async def __call__(self, message: Message) -> bool:
        keyword = message.text
        data_redis = await redis.get(
            f'fsm:{str(message.from_user.id)}:'
            f'{str(message.from_user.id)}:data'
        )
        status_keyword = json.loads(data_redis).get('status_keyword_msk_spb')
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
        if '_' not in callback.data:
            return False
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


class ShowManyVacanciesByKeywordMSKSPBFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопок пагинации при
    показе вакансий, найденных по ключевому слову.
    """

    async def __call__(
        self, callback: CallbackQuery
    ) -> Union[bool, dict[str, int]]:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if not list(
            set(data)
            & set(
                [
                    'show-many-vacancies-by-keyword-msk-spb',
                    'next-keyword-msk-spb',
                    'back-keyword-msk-spb',
                ]
            )
        ):
            return False
        data_redis = await redis.get(
            f'fsm:{str(callback.from_user.id)}:'
            f'{str(callback.from_user.id)}:data'
        )
        count_pages = ceil(
            json.loads(
                data_redis
            ).get('count_vacancies_by_keyword_msk_spb') / 10
        )
        page_number = int(data[-1])
        if 1 > page_number > count_pages:
            return False
        return {'page_number': page_number}
