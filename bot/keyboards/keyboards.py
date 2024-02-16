from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder


def generating_pagination_kb(
    page_number: int, count_pages: int
) -> KeyboardBuilder[InlineKeyboardButton]:
    """
    Клавиатура для перемещения между страницами с вакансиями.
    """
    if page_number == 1:
        return InlineKeyboardBuilder().row(
            InlineKeyboardButton(
                text='Вперёд',
                callback_data=f'next_{page_number + 1}',
            )
        )

    if page_number == count_pages:
        return InlineKeyboardBuilder().row(
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'back_{page_number - 1}',
            ),
            InlineKeyboardButton(
                text='Перейти в избранное',
                callback_data='favorites',
            ),
            InlineKeyboardButton(
                text='Ввести данные заново',
                callback_data='re_enter_data',
            ),
            width=2,
        )
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=f'back_{page_number - 1}',
        ),
        InlineKeyboardButton(
            text='Вперёд',
            callback_data=f'next_{page_number + 1}',
        ),
        InlineKeyboardButton(
            text='Перейти в избранное',
            callback_data='favorites',
        ),
        width=2,
    )


def generation_inline_kb(
    data_for_buttons: List[tuple], width: int
) -> KeyboardBuilder[InlineKeyboardButton]:
    """Функция генерации inline клавиатур на основе полученных данных."""
    bt_list = [
        InlineKeyboardButton(text=x[0], callback_data=str(x[1]))
        for x in data_for_buttons
    ]
    return InlineKeyboardBuilder().row(*bt_list, width=width)
