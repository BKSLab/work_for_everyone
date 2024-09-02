from math import ceil

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loading_vacancies.load_vacancies_hh import load_one_vacancy_hh
from loading_vacancies.load_vacancies_trudvsem import load_one_vacancy_trudvsem
from data_operations.check_data import check_vacancy_favorites_exists
from data_operations.delete_data import delete_vacancy_from_favorites
from data_operations.get_msk_spb_data import (
    get_count_many_vacancies_msk_spb,
    get_count_vacancies_msk_spb,
    get_one_vacancy_msk_spb,
    get_ten_vacancies_msk_spb,
)
from data_operations.save_data import (
    saving_applicant_data,
    saving_vacancy_favorites,
)
from database.models import VacancyMSK, VacancySPB
from filters.msk_spb_filters import (
    AddVacancyMSKSPBFavoritesFilterr,
    CollapseDetailedMSKSPBFilter,
    DeleteVacancyMSKSPBFavoritesFilterr,
    DetailsMSKSPBFilter,
    MSKAndSPBFilter,
    ShowManyVacanciesMSKSPBFilterr,
)
from fsm.fsm import ApplicantState
from keyboards.keyboards import (
    generating_pagination_kb_msk_spb,
    generation_inline_kb,
    generation_inline_kb_with_url,
)
from phrases.msg_generation import msg_details_info_vacancy, msg_info_vacancy
from phrases.phrases_for_bot_messages import (
    BotErrorMessages,
    BotHandlerMessages
)
from phrases.texts_for_bot_buttons import ButtonData


router = Router(name=__name__)


@router.callback_query(MSKAndSPBFilter())
async def handle_start_show_vacancies_msk_and_spb_button(
    callback: CallbackQuery, state: FSMContext
):
    """
    Хендлер, отвечающий за начала показа вакансий в Москве и Санк-Петербурге.
    """
    await callback.answer()
    cities = {'77': 'Москва', '78': 'Санкт-Петербург'}
    city_name = cities.get(callback.data)

    # Сохраняем код региона
    await state.update_data(region_code=int(callback.data))
    # Сохраняем наименования региона
    await state.update_data(region_name=city_name)
    # Сохраняем выбранный пользователем город
    await state.update_data(location=city_name)

    # Сохраняем в БД данные о пользователе
    query_result = saving_applicant_data(await state.get_data())
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
        # получаем количество вакансий в запрошенном пользователем городе
        if callback.data == '77':
            query_result_msk_hh = get_count_vacancies_msk_spb(
                vacancy_source='hh.ru',
                model=VacancyMSK,
            )
            query_result_msk_trud = get_count_vacancies_msk_spb(
                vacancy_source='Работа России',
                model=VacancyMSK,
            )
            if not query_result_msk_hh.get(
                'status'
            ) or not query_result_msk_trud.get('status'):
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
                # Формирую сообщение о количестве найденных вакансий
                count_vac_msk_hh = query_result_msk_hh.get('count_vacancies')
                count_vac_msk_trud = query_result_msk_trud.get(
                    'count_vacancies'
                )
                total_count = count_vac_msk_hh + count_vac_msk_trud
                text_msg = BotHandlerMessages.show_vacancies_msk_spb.format(
                    user_name=callback.from_user.first_name,
                    total=total_count,
                    city=city_name,
                    count_hh=count_vac_msk_hh,
                    count_trud=count_vac_msk_trud,
                )
                await state.update_data(count_vacancies_msk=total_count)
                kb = generation_inline_kb(
                    [
                        ButtonData.show_vacancies_msk_spb,
                        ButtonData.search_by_vacancies_msk_spb,
                    ],
                    1,
                )
                await callback.message.edit_text(
                    text=text_msg, reply_markup=kb.as_markup()
                )
                await state.set_state(
                    ApplicantState.show_vacancies_msk_spb_mode
                )

        if callback.data == '78':
            query_result_spb_hh = get_count_vacancies_msk_spb(
                vacancy_source='hh.ru',
                model=VacancySPB,
            )

            query_result_spb_trud = get_count_vacancies_msk_spb(
                vacancy_source='Работа России',
                model=VacancySPB,
            )
            if not query_result_spb_hh.get(
                'status'
            ) or not query_result_spb_trud.get('status'):
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
                # Формирую сообщение о количестве найденных вакансий
                count_vac_spb_hh = query_result_spb_hh.get('count_vacancies')
                count_vac_spb_trud = query_result_spb_trud.get(
                    'count_vacancies'
                )
                total_count = count_vac_spb_hh + count_vac_spb_trud
                text_msg = BotHandlerMessages.show_vacancies_msk_spb.format(
                    user_name=callback.message.chat.first_name,
                    total=total_count,
                    city=city_name,
                    count_hh=count_vac_spb_hh,
                    count_trud=count_vac_spb_trud,
                )
                await state.update_data(count_vacancies_spb=total_count)
                kb = generation_inline_kb(
                    [
                        ButtonData.show_vacancies_msk_spb,
                        ButtonData.search_by_vacancies_msk_spb,
                    ],
                    1,
                )
                await callback.message.edit_text(
                    text=text_msg, reply_markup=kb.as_markup()
                )
                await state.set_state(
                    ApplicantState.show_vacancies_msk_spb_mode
                )


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_msk_spb_mode),
    DetailsMSKSPBFilter(),
)
async def handle_show_details_vacancy_msk_spb_button(
    callback: CallbackQuery, state: FSMContext
):
    """
    Хендлер, срабатывающий на нажатие кнопки 'Подробнее' при показе
    вакансий в Москве и Санкт-Петербурге
    """
    await callback.answer()
    vacancy_id = callback.data.split('_')[0]
    data_applicant = await state.get_data()
    city = data_applicant.get('location')
    cities = {'Москва': VacancyMSK, 'Санкт-Петербург': VacancySPB}
    search_model = cities.get(city)
    query_result = get_one_vacancy_msk_spb(
        model=search_model, vacancy_id=vacancy_id
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
        vacancy = query_result.get('vacancy')
        vacancy_source = vacancy.vacancy_source
        # загрузка данных о вакансии
        if vacancy_source == 'Работа России':
            result_loading = await load_one_vacancy_trudvsem(
                vacancy_id=vacancy.vacancy_id,
                company_code=vacancy.company_code,
            )
            if not result_loading.get('status'):
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
                await callback.message.answer(
                    text=text, reply_markup=kb.as_markup()
                )
            else:
                vacancy = result_loading.get('vacancy')

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
                            'Свернуть',
                            f'{vacancy.get("vacancy_id")}_mskspb.collapse',
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
            else:
                kb = generation_inline_kb_with_url(
                    [
                        (
                            'Добавить в избранное',
                            f'{vacancy.get("vacancy_id")}_mskspb.favorites',
                            None,
                        ),
                        (
                            'Свернуть',
                            f'{vacancy.get("vacancy_id")}_mskspb.collapse',
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
        text = msg_details_info_vacancy(vacancy)
        await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
        await state.set_state(ApplicantState.show_vacancies_msk_spb_mode)


# Хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_msk_spb_mode),
    CollapseDetailedMSKSPBFilter(),
)
async def handle_collapse_details_vacancy_msk_spb_button(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, срабатывающий на нажатие кнопки 'Свернуть'"""
    await callback.answer()
    vacancy_id = callback.data.split('_')[0]
    data_applicant = await state.get_data()
    city = data_applicant.get('location')
    cities = {'Москва': VacancyMSK, 'Санкт-Петербург': VacancySPB}
    search_model = cities.get(city)
    query_result = get_one_vacancy_msk_spb(
        model=search_model, vacancy_id=vacancy_id
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
        vacancy = query_result.get('vacancy')

        query_result = check_vacancy_favorites_exists(
            vacancy_id=vacancy.vacancy_id,
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
                            f'{vacancy.vacancy_id}_mskspb.delete',
                            None,
                        ),
                        (
                            'Подробнее',
                            f'{vacancy.vacancy_id}_mskspb.details',
                            None,
                        ),
                        (
                            'Откликнуться на {}'.format(
                                vacancy.vacancy_source
                            ),
                            None,
                            vacancy.vacancy_url,
                        ),
                    ],
                    2,
                )
            else:
                kb = generation_inline_kb_with_url(
                    [
                        (
                            'Добавить в избранное',
                            f'{vacancy.vacancy_id}_mskspb.favorites',
                            None,
                        ),
                        (
                            'Подробнее',
                            f'{vacancy.vacancy_id}_mskspb.details',
                            None,
                        ),
                        (
                            'Откликнуться на {}'.format(
                                vacancy.vacancy_source
                            ),
                            None,
                            vacancy.vacancy_url,
                        ),
                    ],
                    2,
                )
        text = msg_info_vacancy(vacancy.__dict__.get('__data__'))
        await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
        await state.set_state(ApplicantState.show_vacancies_msk_spb_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_msk_spb_mode),
    ShowManyVacanciesMSKSPBFilterr(),
)
async def handle_show_many_vacancies_msk_spb_button(
    callback: CallbackQuery, state: FSMContext, page_number: int
):
    """
    Хендлер, отвечающий за показ пользователю найденных вакансий,
    в случае, если их больше 10.
    """
    await callback.answer()
    data_applicant = await state.get_data()
    city = data_applicant.get('location')
    cities = {'Москва': VacancyMSK, 'Санкт-Петербург': VacancySPB}
    search_model = cities.get(city)
    query_result = get_count_many_vacancies_msk_spb(model=search_model)
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
        query_result = get_ten_vacancies_msk_spb(
            model=search_model, page_number=page_number
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
            ten_vacancies = query_result.get('ten_vacancies')
            vacancies_list = [vacancy for vacancy in ten_vacancies.dicts()]
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
                                    (
                                        f'{vacancy.get("vacancy_id")}_'
                                        'mskspb.delete'
                                    ),
                                    None,
                                ),
                                (
                                    'Подробнее',
                                    (
                                        f'{vacancy.get("vacancy_id")}_'
                                        'mskspb.details'
                                    ),
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
                                    (
                                        f'{vacancy.get("vacancy_id")}_'
                                        'mskspb.favorites'
                                    ),
                                    None,
                                ),
                                (
                                    'Подробнее',
                                    (
                                        f'{vacancy.get("vacancy_id")}_'
                                        'mskspb.details'
                                    ),
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
            kb = generating_pagination_kb_msk_spb(page_number, count_pages)
            if page_number == count_pages:
                vacancies_shown = count_vacancies
            else:
                vacancies_shown = 10 * page_number
            text = BotHandlerMessages.show_information.format(
                user_name=callback.from_user.first_name,
                vacancies_shown=vacancies_shown,
                count_vacancies=count_vacancies,
            )
            await callback.message.answer(
                text=text, reply_markup=kb.as_markup()
            )
            await state.set_state(ApplicantState.show_vacancies_msk_spb_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_msk_spb_mode),
    AddVacancyMSKSPBFavoritesFilterr(),
)
async def handle_add_vacancy_favorites_msk_spb_button(
    callback: CallbackQuery, state: FSMContext, vacancy_id: str
):
    """Хендлер, срабатывающий на нажатие кнопки 'Добавить в избранное'"""
    await callback.answer()
    data_applicant = await state.get_data()
    city = data_applicant.get('location')
    cities = {'Москва': VacancyMSK, 'Санкт-Петербург': VacancySPB}
    search_model = cities.get(city)

    query_result = get_one_vacancy_msk_spb(
        model=search_model,
        vacancy_id=vacancy_id,
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
        vacancy = query_result.get('vacancy')
        saving_result = saving_vacancy_favorites(
            vacancy_instance=vacancy, user_tg_id=callback.from_user.id
        )
        if not saving_result.get('status'):
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
            saved_vacancy = saving_result.get('instance')
            kb = generation_inline_kb_with_url(
                [
                    (
                        'Удалить из избранного',
                        f'{saved_vacancy.vacancy_id}_mskspb.delete',
                        None,
                    ),
                    (
                        'Подробнее',
                        f'{saved_vacancy.vacancy_id}_mskspb.details',
                        None,
                    ),
                    (
                        'Откликнуться на {}'.format(
                            saved_vacancy.vacancy_source
                        ),
                        None,
                        saved_vacancy.vacancy_url,
                    ),
                ],
                2,
            )
            text = msg_info_vacancy(
                vacancy=saved_vacancy.__dict__.get('__data__')
            )
            await callback.message.edit_text(
                text=text, reply_markup=kb.as_markup()
            )
            await state.set_state(ApplicantState.show_vacancies_msk_spb_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_msk_spb_mode),
    DeleteVacancyMSKSPBFavoritesFilterr(),
)
async def handle_delete_vacancy_from_favorites_msk_spb_button(
    callback: CallbackQuery, state: FSMContext, vacancy_id: str
):
    """Хендлер, срабатывающий на нажатие кнопки 'Удалить из избранного'"""
    await callback.answer()
    data_applicant = await state.get_data()
    city = data_applicant.get('location')
    cities = {'Москва': VacancyMSK, 'Санкт-Петербург': VacancySPB}
    search_model = cities.get(city)
    query_result = get_one_vacancy_msk_spb(
        model=search_model,
        vacancy_id=vacancy_id,
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
        vacancy = query_result.get('vacancy')
        deleting_result = delete_vacancy_from_favorites(
            vacancy_id=vacancy.vacancy_id,
            user_tg_id=callback.from_user.id,
            vacancy_source=vacancy.vacancy_source,
        )
        if not deleting_result.get('status'):
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
            kb = generation_inline_kb_with_url(
                [
                    (
                        'Добавить в избранное',
                        f'{vacancy.vacancy_id}_mskspb.favorites',
                        None,
                    ),
                    (
                        'Подробнее',
                        f'{vacancy.vacancy_id}_mskspb.details',
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
            text = msg_info_vacancy(vacancy.__dict__.get('__data__'))
            await callback.message.edit_text(
                text=text, reply_markup=kb.as_markup()
            )
        await state.set_state(ApplicantState.show_vacancies_msk_spb_mode)
