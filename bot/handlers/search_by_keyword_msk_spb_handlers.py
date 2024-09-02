from math import ceil

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from data_operations.check_data import check_vacancy_favorites_exists
from data_operations.get_msk_spb_data import (
    get_count_vacancies_by_keyword_msk_spb,
    get_ten_vacancies_by_keyword_msk_spb, get_vacancies_by_keyword_msk_spb)
from database.models import VacancyMSK, VacancySPB
from filters.keyword_filters import (KeywordMSKSPBFilter,
                             ShowManyVacanciesByKeywordMSKSPBFilterr)
from fsm.fsm import ApplicantState
from keyboards.keyboards import (generating_pagination_kb_by_keyword_msk_spb,
                                 generation_inline_kb,
                                 generation_inline_kb_with_url)
from phrases.msg_generation import msg_info_vacancy
from phrases.phrases_for_bot_messages import BotErrorMessages, BotHandlerMessages
from phrases.texts_for_bot_buttons import ButtonData


router = Router(name=__name__)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_msk_spb_mode),
    F.data == ButtonData.search_by_vacancies_msk_spb[1],
)
async def handle_keyword_search_msk_spb_info_button(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, отвечающий за обработку кнопки 'Поиск по ключевому слову'."""
    await callback.answer()
    await state.update_data(status_keyword_msk_spb=1)
    text = BotHandlerMessages.keyword_search_info.format(
        user_name=callback.from_user.first_name
    )
    await callback.message.edit_text(text=text)
    await state.set_state(ApplicantState.show_vacancies_msk_spb_mode)


# хендлер переработан
@router.message(
    StateFilter(ApplicantState.show_vacancies_msk_spb_mode),
    KeywordMSKSPBFilter(),
)
async def handle_search_by_keyword_msk_spb_button(
    message: Message,
    state: FSMContext,
):
    """
    Хендлер, срабатывающий на ввод пользователем ключевого слова
    для уточненного поиска по вакансиям, добавленным в БД.
    """
    data_applicant = await state.get_data()
    city = data_applicant.get('location')
    cities = {'Москва': VacancyMSK, 'Санкт-Петербург': VacancySPB}
    search_model = cities.get(city)
    query_result = get_count_vacancies_by_keyword_msk_spb(
        keyword=message.text,
        model=search_model
    )
    await state.update_data(keyword_msk_spb=message.text)
    await state.update_data(status_keyword_msk_spb=0)
    if not query_result.get('status'):
        text = BotErrorMessages.data_error.format(
            user_name=message.from_user.first_name
        )
        kb = generation_inline_kb(
            [
                ButtonData.feedback,
            ],
            1,
        )
        await message.answer(text=text, reply_markup=kb.as_markup())
    else:
        count_vacancies_by_keyword = query_result.get('count_vacancies')
        if count_vacancies_by_keyword == 0:
            kb = generation_inline_kb(
                [
                    ButtonData.show_many_vacancies,
                    ButtonData.search_by_vacancies_msk_spb,
                ],
                1,
            )
            text = BotHandlerMessages.vacancies_not_found_by_keyword.format(
                user_name=message.from_user.first_name,
                keyword=message.text
            )
            await message.answer(text=text, reply_markup=kb.as_markup())
        if 0 < count_vacancies_by_keyword <= 10:
            kb = generation_inline_kb(
                [
                    ButtonData.show_few_vacancies_by_keyword_msk_spb,
                ],
                1,
            )
            text = BotHandlerMessages.show_vacancies_by_keyword.format(
                user_name=message.from_user.first_name,
                total_vacancies=str(count_vacancies_by_keyword),
                keyword=message.text
            )
            await message.answer(text=text, reply_markup=kb.as_markup())
        if count_vacancies_by_keyword > 10:
            await state.update_data(
                count_vacancies_by_keyword_msk_spb=count_vacancies_by_keyword
            )
            kb = generation_inline_kb(
                [
                    ButtonData.show_many_vacancies_by_keyword_msk_spb,
                ],
                1,
            )
            text = BotHandlerMessages.show_vacancies_by_keyword.format(
                user_name=message.from_user.first_name,
                total_vacancies=str(count_vacancies_by_keyword),
                keyword=message.text
            )
            await message.answer(text=text, reply_markup=kb.as_markup())


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_msk_spb_mode),
    F.data == ButtonData.show_few_vacancies_by_keyword_msk_spb[1],
)
async def handle_show_few_vacancies_by_keyword_msk_spb_button(
    callback: CallbackQuery,
    state: FSMContext,
):
    """
    Хендлер, отвечающий за показ пользователю найденных вакансий
    по введенному ключевому слову,
    в случае, если их меньше или равно 10.
    """
    await callback.answer()
    data_applicant = await state.get_data()
    city = data_applicant.get('location')
    cities = {'Москва': VacancyMSK, 'Санкт-Петербург': VacancySPB}
    keyword = data_applicant.get('keyword_msk_spb')
    search_model = cities.get(city)
    query_result = get_vacancies_by_keyword_msk_spb(
        model=search_model,
        keyword=keyword,
    )
    if not query_result.get('status'):
        text = BotErrorMessages.data_error.format(
            user_name=callback.from_user.first_name
        )
        kb = generation_inline_kb(
            [
                ButtonData.feedback,
            ],
            1,
        )
        await callback.message.answer(
            text=text, reply_markup=kb.as_markup()
        )
    else:
        vacancies_by_keyword = query_result.get('vacancies')
        vacancies_list = [vacancy for vacancy in vacancies_by_keyword.dicts()]
        for vacancy in vacancies_list:
            query_result = check_vacancy_favorites_exists(
                vacancy_id=vacancy.get('vacancy_id'),
                user_tg_id=callback.from_user.id,
            )
            if not query_result.get('status'):
                text = BotErrorMessages.data_error.format(
                    user_name=callback.from_user.first_name
                )
                kb = generation_inline_kb(
                    [
                        ButtonData.feedback,
                    ],
                    1,
                )
                await callback.message.answer(
                    text=text, reply_markup=kb.as_markup()
                )
            else:
                if query_result.get('check_status'):
                    kb = generation_inline_kb_with_url(
                        [
                            (
                                'Удалить из избранного',
                                f'{vacancy.get("vacancy_id")}_mskspb.delete',
                                None,
                            ),
                            (
                                'Подробнее',
                                f'{vacancy.get("vacancy_id")}_mskspb.details',
                                None,
                            ),
                            (
                                'Откликнуться на {}'.format(
                                    vacancy.get('vacancy_source')
                                ),
                                None,
                                vacancy.get('vacancy_url'),
                            ),
                        ],
                        2,
                    )
                if not query_result.get('check_status'):
                    kb = generation_inline_kb_with_url(
                        [
                            (
                                'Добавить в избранное',
                                f'{vacancy.get("vacancy_id")}_mskspb.favorites',
                                None,
                            ),
                            (
                                'Подробнее',
                                f'{vacancy.get("vacancy_id")}_mskspb.details',
                                None,
                            ),
                            (
                                'Откликнуться на {}'.format(
                                    vacancy.get('vacancy_source')
                                ),
                                None,
                                vacancy.get('vacancy_url'),
                            ),
                        ],
                        2,
                    )

            # end block
            text = msg_info_vacancy(vacancy)
            await callback.message.answer(
                text=text, reply_markup=kb.as_markup()
            )

        text = BotHandlerMessages.show_completed_by_keyword.format(
            user_name=callback.from_user.first_name
        )
        kb = generation_inline_kb(
            [
                ButtonData.favorites,
                ButtonData.show_vacancies_msk_spb,
                ButtonData.search_by_vacancies_msk_spb,
            ],
            2,
        )
        await callback.message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.show_vacancies_msk_spb_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_msk_spb_mode),
    ShowManyVacanciesByKeywordMSKSPBFilterr(),
)
async def handle_show_many_vacancies_by_keyword_msk_spb_button(
    callback: CallbackQuery,
    state: FSMContext,
    page_number: int,
):
    """
    Хендлер, отвечающий за показ пользователю найденных вакансий
    по введенному ключевому слову,
    в случае, если их больше 10.
    """
    await callback.answer()
    data_applicant = await state.get_data()
    city = data_applicant.get('location')
    cities = {'Москва': VacancyMSK, 'Санкт-Петербург': VacancySPB}
    keyword = data_applicant.get('keyword_msk_spb')
    search_model = cities.get(city)
    query_result = get_count_vacancies_by_keyword_msk_spb(
        model=search_model,
        keyword=keyword,
    )
    if not query_result.get('status'):
        text = BotErrorMessages.data_error.format(
            user_name=callback.from_user.first_name
        )
        kb = generation_inline_kb(
            [
                ButtonData.feedback,
            ],
            1,
        )
        await callback.message.answer(
            text=text, reply_markup=kb.as_markup()
        )
    else:
        count_vacancies = query_result.get('count_vacancies')
        count_pages = ceil(count_vacancies / 10)
        query_result = get_ten_vacancies_by_keyword_msk_spb(
            model=search_model,
            page_number=page_number,
            keyword=keyword,
        )
        if not query_result.get('status'):
            text = BotErrorMessages.data_error.format(
                user_name=callback.from_user.first_name
            )
            kb = generation_inline_kb(
                [
                    ButtonData.feedback,
                ],
                1,
            )
            await callback.message.answer(
                text=text, reply_markup=kb.as_markup()
            )
        else:
            vacancies_by_keyword = query_result.get('vacancies_by_keyword')
            vacancies_list = [
                vacancy for vacancy in vacancies_by_keyword.dicts()
            ]
            for vacancy in vacancies_list:
                query_result = check_vacancy_favorites_exists(
                    vacancy_id=vacancy.get('vacancy_id'),
                    user_tg_id=callback.from_user.id,
                )
                if not query_result.get('status'):
                    text = BotErrorMessages.data_error.format(
                        user_name=callback.from_user.first_name
                    )
                    kb = generation_inline_kb(
                        [
                            ButtonData.feedback,
                        ],
                        1,
                    )
                    await callback.message.answer(
                        text=text, reply_markup=kb.as_markup()
                    )
                else:
                    if query_result.get('check_status'):
                        kb = generation_inline_kb_with_url(
                            [
                                (
                                    'Удалить из избранного',
                                    f'{vacancy.get("vacancy_id")}_mskspb.delete',
                                    None,
                                ),
                                (
                                    'Подробнее',
                                    f'{vacancy.get("vacancy_id")}_mskspb.details',
                                    None,
                                ),
                                (
                                    'Откликнуться на {}'.format(
                                        vacancy.get('vacancy_source')
                                    ),
                                    None,
                                    vacancy.get('vacancy_url'),
                                ),
                            ],
                            2,
                        )
                    if not query_result.get('check_status'):
                        kb = generation_inline_kb_with_url(
                            [
                                (
                                    'Добавить в избранное',
                                    f'{vacancy.get("vacancy_id")}_mskspb.favorites',
                                    None,
                                ),
                                (
                                    'Подробнее',
                                    f'{vacancy.get("vacancy_id")}_mskspb.details',
                                    None,
                                ),
                                (
                                    'Откликнуться на {}'.format(
                                        vacancy.get('vacancy_source')
                                    ),
                                    None,
                                    vacancy.get('vacancy_url'),
                                ),
                            ],
                            2,
                        )

                text = msg_info_vacancy(vacancy)
                await callback.message.answer(
                    text=text, reply_markup=kb.as_markup()
                )

            kb = generating_pagination_kb_by_keyword_msk_spb(page_number, count_pages)
            if page_number == count_pages:
                vacancies_shown = count_vacancies
            else:
                vacancies_shown = 10 * page_number
            text = BotHandlerMessages.show_information_by_keyword.format(
                user_name=callback.from_user.first_name,
                vacancies_shown=vacancies_shown,
                count_vacancies=count_vacancies,
                keyword=keyword
            )
            await callback.message.answer(
                text=text, reply_markup=kb.as_markup()
            )
            await state.set_state(ApplicantState.show_vacancies_msk_spb_mode)
