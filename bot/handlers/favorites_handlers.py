from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from data_operations.delete_data import delete_vacancy_from_favorites
from data_operations.get_data import (get_one_vacancy_from_favorites,
                                      get_vacancies_from_favorites)
from filters.favorites_filters import (CollapseDetailedFavoritesFilter,
                                       DeleteVacancyFavoritesFilterr,
                                       DetailsFavoritesFilter)
from fsm.fsm import ApplicantState
from keyboards.keyboards import (generation_inline_kb,
                                 generation_inline_kb_with_url)
from loading_vacancies.load_vacancies_hh import load_one_vacancy_hh
from loading_vacancies.load_vacancies_trudvsem import load_one_vacancy_trudvsem
from phrases.msg_generation import (msg_details_info_vacancy,
                                    msg_info_vacancy_favorites)
from phrases.phrases_for_bot_messages import (
    BotErrorMessages,
    BotHandlerMessages,
)
from phrases.texts_for_bot_buttons import ButtonData


router = Router(name=__name__)

# хендлер переработан
@router.callback_query(F.data == ButtonData.favorites[1])
async def handle_favorites_button(
    callback: CallbackQuery,
    state: FSMContext,
):
    """Хендлер, отвечающий за обработку кнопки 'Перейти в избранное'"""
    await callback.answer()
    query_result = get_vacancies_from_favorites(
        user_tg_id=callback.from_user.id
    )
    if not query_result.get('status'):
        text = BotErrorMessages.favorites_error.format(
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
        vacancies = query_result.get('vacancies')
        if not vacancies:
            text = BotHandlerMessages.no_vacancies_in_favorites.format(
                user_name=callback.from_user.first_name
            )
            kb = generation_inline_kb(
                [ButtonData.ready, ButtonData.bot_help], 2
            )
            await callback.message.edit_text(
                text=text, reply_markup=kb.as_markup()
            )
            await state.set_state(ApplicantState.federal_district_choice)
        else:
            vacancies_list = [vacancy for vacancy in vacancies.dicts()]
            for vacancy in vacancies_list:
                status_archival = False
                vacancy_source = vacancy.get('vacancy_source')

                if vacancy_source == 'Работа России':
                    result_loading = await load_one_vacancy_trudvsem(
                        vacancy_id=vacancy.get('vacancy_id'),
                        company_code=vacancy.get('company_code'),
                    )
                    # проверка актуальности вакансии после запроса к сайту Работа России
                    if (
                        not result_loading.get('status')
                        and 'vacancy_status' in result_loading
                    ):
                        status = False
                        status_information = 'Вакансия удалена'
                    else:
                        status = True
                        status_information = 'Вакансия актуальная'
                    if (
                        not result_loading.get('status')
                        and 'vacancy_status' not in result_loading
                    ):
                        # Блок кода для отправки пользователю сообщения о неудачной работе
                        text = BotErrorMessages.trudvsem_request_error.format(
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
                if vacancy_source == 'hh.ru':
                    result_loading = await load_one_vacancy_hh(
                        vacancy_id=vacancy.get('vacancy_id')
                    )
                    if not result_loading.get('status'):
                        # Блок кода для отправки пользователю сообщения о неудачной работе
                        text = BotErrorMessages.hh_request_error.format(
                            user_name=callback.from_user.first_name
                        )
                        kb = generation_inline_kb(
                            [
                                ButtonData.feedback,
                            ],
                            1,
                        )
                        await callback.message.edit_text(
                            text=text, reply_markup=kb.as_markup()
                        )
                    # проверка наличие вакансии после запроса к
                    # сайту hh.ru
                    elif (
                        result_loading.get('status')
                        and 'vacancy_status' in result_loading
                    ):
                        vacancy_status = result_loading.get('vacancy_status')
                        if vacancy_status == 'does_not_exist':
                            status = False
                            status_information = 'Вакансия удалена'
                        if vacancy_status == 'archival':
                            status = True
                            status_archival = True
                            status_information = 'Вакансия в архиве'
                        if vacancy_status == 'actual':
                            status = True
                            status_information = 'Вакансия актуальная'

                if status and status_archival:
                    kb = generation_inline_kb_with_url(
                        [
                            (
                                'Удалить из избранного',
                                f'{vacancy.get("vacancy_id")}_favorites.delete',
                                None,
                            ),
                            (
                                'Подробнее',
                                f'{vacancy.get("vacancy_id")}_favorites.details',
                                None,
                            ),
                            (
                                'Посмотреть на {}'.format(
                                    vacancy.get('vacancy_source')
                                ),
                                None,
                                vacancy.get('vacancy_url'),
                            ),
                        ],
                        2,
                    )

                    text = msg_info_vacancy_favorites(
                        vacancy=vacancy, status_information=status_information
                    )
                    await callback.message.answer(
                        text=text, reply_markup=kb.as_markup()
                    )
                    await state.set_state(ApplicantState.show_vacancies_mode)

                if status and not status_archival:
                    kb = generation_inline_kb_with_url(
                        [
                            (
                                'Удалить из избранного',
                                f'{vacancy.get("vacancy_id")}_favorites.delete',
                                None,
                            ),
                            (
                                'Подробнее',
                                f'{vacancy.get("vacancy_id")}_favorites.details',
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

                    text = msg_info_vacancy_favorites(
                        vacancy=vacancy, status_information=status_information
                    )
                    await callback.message.answer(
                        text=text, reply_markup=kb.as_markup()
                    )
                    await state.set_state(ApplicantState.show_vacancies_mode)

                if not status:
                    kb = generation_inline_kb_with_url(
                        [
                            (
                                'Удалить из избранного',
                                f'{vacancy.get("vacancy_id")}_favorites.delete',
                                None,
                            ),
                        ],
                        1,
                    )
                    text = msg_info_vacancy_favorites(
                        vacancy=vacancy, status_information=status_information
                    )
                    await callback.message.answer(
                        text=text, reply_markup=kb.as_markup()
                    )
                    await state.set_state(ApplicantState.show_vacancies_mode)

            text = BotHandlerMessages.message_in_favorites.format(
                user_name=callback.from_user.first_name,
                vacancies_count=vacancies.count(),
            )
            kb = generation_inline_kb(
                [
                    ButtonData.data_input,
                    ButtonData.bot_help,
                ],
                2,
            )
            await callback.message.answer(
                text=text, reply_markup=kb.as_markup()
            )
            await state.set_state(ApplicantState.show_vacancies_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode), DetailsFavoritesFilter()
)
async def handle_show_details_favorites_button(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, срабатывающий на нажатие кнопки 'Подробнее' в избранном."""
    await callback.answer()
    vacancy_id = callback.data.split('_')[0]
    query_result = get_one_vacancy_from_favorites(
        vacancy_id=vacancy_id, user_tg_id=callback.from_user.id
    )
    if not query_result.get('status'):
        text = BotErrorMessages.favorites_error.format(
            user_name=callback.from_user.first_name
        )
        kb = generation_inline_kb(
            [
                ButtonData.feedback,
            ],
            1,
        )
        await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
    else:
        vacancy = query_result.get('vacancy')
        vacancy_source = vacancy.vacancy_source
        if vacancy_source == 'Работа России':
            result_loading = await load_one_vacancy_trudvsem(
                vacancy_id=vacancy.vacancy_id,
                company_code=vacancy.company_code,
            )
            if not result_loading.get('status'):
                # Блок кода для отправки пользователю сообщения о неудачной работе
                text = BotErrorMessages.trudvsem_request_error.format(
                    user_name=callback.from_user.first_name
                )
                kb = generation_inline_kb(
                    [
                        ButtonData.feedback,
                    ],
                    1,
                )
                await callback.message.edit_text(
                    text=text, reply_markup=kb.as_markup()
                )
            else:
                vacancy = result_loading.get('vacancy')

        if vacancy_source == 'hh.ru':
            result_loading = await load_one_vacancy_hh(
                vacancy_id=vacancy.vacancy_id
            )
            if not result_loading.get('status'):
                text = BotErrorMessages.hh_request_error.format(
                    user_name=callback.from_user.first_name
                )
                kb = generation_inline_kb(
                    [
                        ButtonData.feedback,
                    ],
                    1,
                )
                await callback.message.edit_text(
                    text=text, reply_markup=kb.as_markup()
                )
            else:
                vacancy = result_loading.get('vacancy')
        kb = generation_inline_kb_with_url(
            [
                (
                    'Удалить из избранного',
                    f'{vacancy.get("vacancy_id")}_favorites.delete',
                    None,
                ),
                (
                    'Свернуть',
                    f'{vacancy.get("vacancy_id")}_favorites.collapse',
                    None,
                ),
                (
                    'Откликнуться на {}'.format(vacancy.get('vacancy_source')),
                    None,
                    vacancy.get('vacancy_url'),
                ),
            ],
            2,
        )
        text = msg_details_info_vacancy(vacancy)
        await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
        await state.set_state(ApplicantState.show_vacancies_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode),
    CollapseDetailedFavoritesFilter(),
)
async def handle_collapse_details_favorites_button(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, срабатывающий на нажатие кнопки 'Свернуть'"""
    await callback.answer()
    vacancy_id = callback.data.split('_')[0]
    query_result = get_one_vacancy_from_favorites(
        vacancy_id=vacancy_id, user_tg_id=callback.from_user.id
    )
    if not query_result.get('status'):
        text = BotErrorMessages.favorites_error.format(
            user_name=callback.from_user.first_name
        )
        kb = generation_inline_kb(
            [
                ButtonData.feedback,
            ],
            1,
        )
        await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
    else:
        vacancy = query_result.get('vacancy')
        kb = generation_inline_kb_with_url(
            [
                (
                    'Удалить из избранного',
                    f'{vacancy.vacancy_id}_favorites.delete',
                    None,
                ),
                (
                    'Подробнее',
                    f'{vacancy.vacancy_id}_favorites.details',
                    None,
                ),
                (
                    'Откликнуться на {}'.format(vacancy.vacancy_source),
                    None,
                    vacancy.vacancy_url,
                ),
            ],
            2,
        )
        text = msg_info_vacancy_favorites(
            vacancy=vacancy.__dict__.get('__data__'),
            status_information='Вакансия актуальна',
        )
        await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
        await state.set_state(ApplicantState.show_vacancies_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode),
    DeleteVacancyFavoritesFilterr(),
)
async def handle_delete_vacancy_from_favorites_button(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, срабатывающий на нажатие кнопки 'Удалить из избранного'"""
    await callback.answer()
    vacancy_id = callback.data.split('_')[0]
    query_result = get_one_vacancy_from_favorites(
        vacancy_id=vacancy_id, user_tg_id=callback.from_user.id
    )
    if not query_result.get('status'):
        text = BotErrorMessages.favorites_error.format(
            user_name=callback.from_user.first_name
        )
        kb = generation_inline_kb(
            [
                ButtonData.feedback,
            ],
            1,
        )
        await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
    else:
        vacancy = query_result.get('vacancy')
        vacancy_name = vacancy.vacancy_name
        deleting_result = delete_vacancy_from_favorites(
            vacancy_id=vacancy.vacancy_id,
            user_tg_id=callback.from_user.id,
            vacancy_source=vacancy.vacancy_source,
        )
        if not deleting_result.get('status'):
            text = BotErrorMessages.favorites_error.format(
                user_name=callback.from_user.first_name
            )
            kb = generation_inline_kb(
                [
                    ButtonData.feedback,
                ],
                1,
            )
            await callback.message.edit_text(
                text=text, reply_markup=kb.as_markup()
            )
        else:
            text = BotHandlerMessages.vacancy_deleted.format(
                vacancy_name=vacancy_name
            )
            await callback.message.edit_text(text=text)
            await state.set_state(ApplicantState.show_vacancies_mode)
