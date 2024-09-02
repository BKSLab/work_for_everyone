from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class FavoritesFilterr(BaseFilter):
    """
    Фильтр для перехода пользователя в избранное'.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data == 'favorites':
            return True
        return False


class AddVacancyFavoritesFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Добавить в избранное'.
    """

    async def __call__(self, callback: CallbackQuery) -> Union[bool, dict]:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if 'favorites' not in data:
            return False
        vacancy_id = data[0]
        return {'vacancy_id': vacancy_id}


class DetailsFavoritesFilter(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Подробнее'.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if data[1] == 'favorites.details':
            return True


class CollapseDetailedFavoritesFilter(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Свернуть' в избранном.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if data[1] == 'favorites.collapse':
            return True


class DeleteVacancyFavoritesFilterr(BaseFilter):
    """
    Фильтр для перехвата нажатия кнопки 'Удалить из избранного' в избранном.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        if '_' not in callback.data:
            return False
        data = callback.data.split('_')
        if data[1] == 'favorites.delete':
            return True
