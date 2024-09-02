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


def generating_pagination_kb_by_keyword(
    page_number: int, count_pages: int
) -> KeyboardBuilder[InlineKeyboardButton]:
    """
    Клавиатура для перемещения между страницами
    с вакансиями, найденными по ключевому слову.
    """
    if page_number == 1:
        return InlineKeyboardBuilder().row(
            InlineKeyboardButton(
                text='Вперёд',
                callback_data=f'next-keyword_{page_number + 1}',
            )
        )

    if page_number == count_pages:
        return InlineKeyboardBuilder().row(
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'back-keyword_{page_number - 1}',
            ),
            InlineKeyboardButton(
                text='Перейти в избранное',
                callback_data='favorites',
            ),
            InlineKeyboardButton(
                text='Поиск по ключевому слову',
                callback_data='search_by_vacancies',
            ),
            InlineKeyboardButton(
                text='Показать все вакансии',
                callback_data='show_many_vacancies_1',
            ),
            width=1,
        )
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=f'back-keyword_{page_number - 1}',
        ),
        InlineKeyboardButton(
            text='Вперёд',
            callback_data=f'next-keyword_{page_number + 1}',
        ),
        InlineKeyboardButton(
            text='Перейти в избранное',
            callback_data='favorites',
        ),
        width=2,
    )


def generating_pagination_kb_by_keyword_msk_spb(
    page_number: int, count_pages: int
) -> KeyboardBuilder[InlineKeyboardButton]:
    """
    Клавиатура для перемещения между страницами
    с вакансиями, найденными по ключевому слову.
    """
    if page_number == 1:
        return InlineKeyboardBuilder().row(
            InlineKeyboardButton(
                text='Вперёд',
                callback_data=f'next-keyword-msk-spb_{page_number + 1}',
            )
        )

    if page_number == count_pages:
        return InlineKeyboardBuilder().row(
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'back-keyword-msk-spb_{page_number - 1}',
            ),
            InlineKeyboardButton(
                text='Перейти в избранное',
                callback_data='favorites',
            ),
            InlineKeyboardButton(
                text='Поиск по ключевому слову',
                callback_data='search_by_vacancies_msk_spb',
            ),
            InlineKeyboardButton(
                text='Показать все вакансии',
                callback_data='show_many_vacancies_1',
            ),
            width=1,
        )
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=f'back-keyword-msk-spb_{page_number - 1}',
        ),
        InlineKeyboardButton(
            text='Вперёд',
            callback_data=f'next-keyword-msk-spb_{page_number + 1}',
        ),
        InlineKeyboardButton(
            text='Перейти в избранное',
            callback_data='favorites',
        ),
        width=2,
    )


def generating_pagination_kb_msk_spb(
    page_number: int, count_pages: int
) -> KeyboardBuilder[InlineKeyboardButton]:
    """
    Клавиатура для перемещения между страницами
    с вакансиями, найденными в Москве и Санкт-Петербурге.
    """
    if page_number == 1:
        return InlineKeyboardBuilder().row(
            InlineKeyboardButton(
                text='Вперёд',
                callback_data=f'next-msk-spb_{page_number + 1}',
            )
        )

    if page_number == count_pages:
        return InlineKeyboardBuilder().row(
            InlineKeyboardButton(
                text='Назад',
                callback_data=f'back-msk-spb_{page_number - 1}',
            ),
            InlineKeyboardButton(
                text='Перейти в избранное',
                callback_data='favorites',
            ),
            InlineKeyboardButton(
                text='Поиск по ключевому слову',
                callback_data='search_by_vacancies_msk_spb',
            ),
            InlineKeyboardButton(
                text='Показать все вакансии',
                callback_data='show_many_vacancies_1',
            ),
            width=1,
        )
    return InlineKeyboardBuilder().row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=f'back-msk-spb_{page_number - 1}',
        ),
        InlineKeyboardButton(
            text='Вперёд',
            callback_data=f'next-msk-spb_{page_number + 1}',
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


def generation_inline_kb_with_url(
    data_for_buttons: List[tuple], width: int
) -> KeyboardBuilder[InlineKeyboardButton]:
    """Функция генерации inline клавиатур на основе полученных данных с url."""
    bt_list = [
        InlineKeyboardButton(text=x[0], callback_data=str(x[1]), url=x[2])
        for x in data_for_buttons
    ]
    return InlineKeyboardBuilder().row(*bt_list, width=width)
