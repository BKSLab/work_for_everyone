import json
import re
from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
from database.models import Region
from database.redis import redis
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


class CommanDdataEntryFilter(BaseFilter):
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


class RegionNameFilter(BaseFilter):
    """
    Фильтр для перехвата номеров регионов
    в выбранном федеральном округе.
    """

    async def __call__(self, callback: CallbackQuery) -> bool:
        data_redis = await redis.get(
            f'fsm:{str(callback.from_user.id)}:'
            f'{str(callback.from_user.id)}:data'
        )
        fd_code = json.loads(data_redis).get('fd_code')
        regions = [
            (region.region_code, region.region_name)
            for region in Region.select().where(
                Region.federal_district_code == fd_code
            )
        ]
        for region in regions:
            if int(callback.data) in region:
                return {'region_name': region[1]}
        return False


class NameLocalityFilter(BaseFilter):
    """
    Фильтр для обработки названия ннаселенного пункта,
    введенного пользователем.
    """

    async def __call__(self, message: Message) -> bool | dict[str, List[str]]:
        if message.text.lower() in ['москва', 'санкт-Петербург']:
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
