import json
from math import ceil
from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from database.redis import redis


class MSKAndSPBFilter(BaseFilter):
    """Фильтр для перехвата городов Москва и Санкт-Питербург."""

    async def __call__(
        self, callback: CallbackQuery
    ) -> Union[bool, dict[str, str]]:
        if not callback.data.isdigit():
            return False
        if callback.data == '77' or callback.data == '78':
            return True


class ShowManyVacanciesMSKSPBFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопок пагинации при показе вакансий,
    найденных в Москве и Санкт-Петербурге.
    """

    async def __call__(
        self, callback: CallbackQuery
    ) -> Union[bool, dict[str, int]]:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if not list(
            set(data) & set(
                [
                    'show-many-vacancies-msk-spb',
                    'next-msk-spb',
                    'back-msk-spb'
                ]
            )
        ):
            return False
        data_redis = await redis.get(
            f'fsm:{str(callback.from_user.id)}:'
            f'{str(callback.from_user.id)}:data'
        )
        region_code = json.loads(data_redis).get('region_code')
        # логика работы с Москвой
        if region_code == 77:
            count_pages = ceil(
                json.loads(data_redis).get('count_vacancies_msk') / 10
            )
            page_number = int(data[-1])
            if 1 > page_number > count_pages:
                return False
            return {'page_number': page_number}
        # логика работы с Санкт-Петербургом
        if region_code == 78:
            count_pages = ceil(
                json.loads(data_redis).get('count_vacancies_spb') / 10
            )
            page_number = int(data[-1])
            if 1 > page_number > count_pages:
                return False
            return {'page_number': page_number}


class DeleteVacancyMSKSPBFavoritesFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Удалить из избранного'.
    """

    async def __call__(self, callback: CallbackQuery) -> Union[bool, dict]:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if 'mskspb.delete' not in data:
            return False
        vacancy_id = data[0]
        return {'vacancy_id': vacancy_id}


class DetailsMSKSPBFilter(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Подробнее' для вакансий, найденных
    в городе Москва и Санкт-Петербург.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if data[1] == 'mskspb.details':
            return True
        return False


class CollapseDetailedMSKSPBFilter(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Свернуть'
    при показе вакансий в Москве и Санкт-Петербурге..
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if data[1] == 'mskspb.collapse':
            return True
        return False


class AddVacancyMSKSPBFavoritesFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Добавить в избранное'.
    """

    async def __call__(self, callback: CallbackQuery) -> Union[bool, dict]:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if 'mskspb.favorites' not in data:
            return False
        vacancy_id = data[0]
        return {'vacancy_id': vacancy_id}
