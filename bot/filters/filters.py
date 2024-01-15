from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from phrases.texts_for_bot_buttons import TEXT_FOR_BUTTON


class FederalDistrictFilter(BaseFilter):
    """Фильтр для перехвата номера федерального округа."""

    async def __call__(self, callback: CallbackQuery) -> bool:
        codes = [
            code for code in TEXT_FOR_BUTTON.get('federal_districts').values()
        ]
        if int(callback.data) in codes:
            return True
        return False


class RegionNameFilter(BaseFilter):
    """Фильтр для перехвата номера региона."""

    async def __call__(self, callback: CallbackQuery) -> bool:
        print(callback.data)
        return True
