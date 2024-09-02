from math import ceil

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from data_operations.check_data import check_vacancy_favorites_exists
from data_operations.delete_data import delete_vacancy_from_favorites
from data_operations.get_data import (
    get_all_vacancies_user_location,
    get_count_all_vacancies_user_location,
    get_data_lst_regions,
    get_one_vacancy,
    get_ten_vacancies,
)
from data_operations.save_data import saving_applicant_data, saving_vacancy_favorites
from filters.favorites_filters import AddVacancyFavoritesFilterr
from filters.main_filters import (
    CollapseDetailedFilter,
    DeleteVacancyFilterr,
    DetailsFilter,
    FederalDistrictFilter,
    NameLocalityFilter,
    RegionFilter,
    ShowManyVacanciesFilterr,
    StartDataEntryFilter,
)
from fsm.fsm import ApplicantState
from keyboards.keyboards import (
    generating_pagination_kb,
    generation_inline_kb,
    generation_inline_kb_with_url,
)
from loading_vacancies.load_manage_vacancies import (
    loading_management_vacancies_user_location,
)
from loading_vacancies.load_vacancies_hh import load_one_vacancy_hh
from loading_vacancies.load_vacancies_trudvsem import load_one_vacancy_trudvsem
from phrases.msg_generation import (
    msg_details_info_vacancy,
    msg_info_vacancy,
    msg_verification,
)
from phrases.phrases_for_bot_messages import (
    BotCommandPhrases,
    BotErrorMessages,
    BotHandlerMessages,
)
from phrases.texts_for_bot_buttons import ButtonData

router = Router(name=__name__)


# handle_favorites_button


# хендлер переработан
@router.callback_query(F.data == ButtonData.bot_help[1])
async def handle_bot_help_button(callback: CallbackQuery):
    """Хендлер, срабатывающий на кнопку 'Справка по боту'."""
    await callback.answer()
    text = BotCommandPhrases.help_command.format(
        user_name=callback.from_user.first_name
    )
    kb = generation_inline_kb([ButtonData.data_input], 1)
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())


# хендлер переработан
@router.callback_query(StartDataEntryFilter())
async def handle_start_data_entry_button(
    callback: CallbackQuery,
    state: FSMContext,
):
    """
    Хендлер, срабатывающий на кнопки 'Готов начать' и 'Начать ввод данных'.
    Осуществляется запуск основной логике бота.
    """
    await callback.answer()
    await state.clear()
    await state.update_data(name_applicant=callback.from_user.first_name)
    await state.update_data(user_tg_id=callback.from_user.id)
    text = BotHandlerMessages.choice_federal_districts.format(
        user_name=callback.from_user.first_name
    )
    kb = generation_inline_kb([*ButtonData.federal_districts], 1)
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.federal_district_choice)


# хендлер переработан, нужно добавить безопасное извлечение данных из БД
@router.callback_query(
    StateFilter(ApplicantState.federal_district_choice),
    FederalDistrictFilter(),
)
async def handle_federal_district_button(
    callback: CallbackQuery,
    state: FSMContext,
):
    """
    Хендлер, срабатывающий на выбор федерального округа.
    В соответствии с выбранным пользователем федеральным округом
    создается inline клавиатура с названиями регионов.
    """
    await callback.answer()
    await state.update_data(fd_code=int(callback.data))

    # доработать запрос к БД, привести его к безопасному варианту
    data = get_data_lst_regions(callback.data)
    data.append(ButtonData.back_to_selection_f_d)

    text = BotHandlerMessages.choice_region_name.format(
        user_name=callback.from_user.first_name
    )
    kb = generation_inline_kb(data, 1)
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.region_name_choice)


# хендлер переработан
@router.callback_query(StateFilter(ApplicantState.region_name_choice), RegionFilter())
async def handle_region_name_button(
    callback: CallbackQuery,
    state: FSMContext,
    region_name: str,
):
    """
    Хендлер, срабатывающий на выбор пользователем региона,
    в федеральном округе.
    """
    await callback.answer()
    await state.update_data(region_code=int(callback.data))
    await state.update_data(region_name=region_name)
    if callback.data in ["92"]:
        await state.update_data(location=region_name)
        entered_data = await state.get_data()
        text = msg_verification(entered_data)
        kb = generation_inline_kb(
            [ButtonData.start_searching, ButtonData.re_enter_data], 2
        )

        await callback.message.edit_text(
            text=text,
            reply_markup=kb.as_markup(),
        )
        await state.set_state(ApplicantState.verification_data)
    else:
        text = BotHandlerMessages.input_name_locality.format(
            user_name=callback.from_user.first_name
        )
        await callback.message.edit_text(text=text)
        await state.set_state(ApplicantState.local_name_input)


# хендлер переработан
@router.message(
    StateFilter(ApplicantState.local_name_input),
    NameLocalityFilter(),
)
async def handle_locality_name_input(
    message: Message,
    locality_name: str,
    state: FSMContext,
):
    """
    Хендлер, срабатывающий на ввод пользователем наименования
    населенного пункта, в котором необходимо искать вакансии.
    """
    await state.update_data(location=locality_name)
    entered_data = await state.get_data()
    text = msg_verification(entered_data)
    kb = generation_inline_kb([ButtonData.re_enter_data, ButtonData.start_searching], 1)
    await message.answer(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.verification_data)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.verification_data),
    F.data == ButtonData.start_searching[1],
)
async def handle_start_search_vacancies_button(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, отвечающий за обработку кнопки 'Начать поиск вакансий'."""
    await callback.answer()
    text = BotHandlerMessages.search_vacancies.format(
        user_name=callback.from_user.first_name
    )
    await callback.message.edit_text(text=text)
    query_result = saving_applicant_data(await state.get_data())
    if not query_result.get("status"):
        text = BotErrorMessages.data_error.format(
            user_name=callback.from_user.first_name
        )
        kb = generation_inline_kb(
            [
                ButtonData.feedback,
            ],
            1,
        )
        await callback.message.answer(text=text, reply_markup=kb.as_markup())
    else:
        aplicant_instance = query_result.get("instance")
        result_operation = await loading_management_vacancies_user_location(
            aplicant_instance=aplicant_instance,
        )
        if not result_operation.get("status"):
            text = BotErrorMessages.main_request_error.format(
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
        if (
            result_operation.get("status")
            and result_operation.get("total_vacancies") == 0
        ):
            text = BotHandlerMessages.vacancies_not_found.format(
                user_name=callback.from_user.first_name,
                user_location=aplicant_instance.location
            )
            kb = generation_inline_kb([ButtonData.re_enter_data], 1)
            await callback.message.edit_text(
                text=text, reply_markup=kb.as_markup()
            )

        if (
            result_operation.get("status")
            and 0 < result_operation.get("total_vacancies") <= 10
        ):
            await state.update_data(
                count_vacancies=result_operation.get("total_vacancies")
            )
            text = BotHandlerMessages.show_vacancies.format(
                user_name=callback.from_user.first_name,
                total_vacancies=str(result_operation.get("total_vacancies")),
                user_location=aplicant_instance.location,
                count_vacancy_trudvsem=str(result_operation.get("count_vacancy_trudvsem")),
                count_vacancy_hh=str(result_operation.get("count_vacancy_hh")),
            )
            kb = generation_inline_kb([ButtonData.show_few_vacancies], 1)
            await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
            await state.set_state(ApplicantState.show_vacancies_mode)

        if (
            result_operation.get("status")
            and result_operation.get("total_vacancies") > 10
        ):
            await state.update_data(
                count_vacancies=result_operation.get("total_vacancies")
            )
            text = BotHandlerMessages.show_vacancies.format(
                user_name=callback.from_user.first_name,
                total_vacancies=str(result_operation.get("total_vacancies")),
                user_location=aplicant_instance.location,
                count_vacancy_trudvsem=str(result_operation.get("count_vacancy_trudvsem")),
                count_vacancy_hh=str(result_operation.get("count_vacancy_hh")),
            )
            kb = generation_inline_kb(
                [
                    ButtonData.show_many_vacancies,
                    ButtonData.search_by_vacancies,
                ],
                1,
            )
            await callback.message.edit_text(
                text=text, reply_markup=kb.as_markup()
            )
            await state.set_state(ApplicantState.show_vacancies_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode),
    F.data == ButtonData.show_few_vacancies[1],
)
async def handle_show_few_vacancies_button(
    callback: CallbackQuery,
    state: FSMContext,
):
    """
    Хендлер, отвечающий за показ пользователю найденных вакансий,
    в случае, если их меньше или равно 10.
    """
    await callback.answer()
    query_result = get_all_vacancies_user_location(callback.from_user.id)
    if not query_result.get("status"):
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
        vacancies = query_result.get("vacancies")
        vacancies_list = [vacancy for vacancy in vacancies.dicts()]
        for vacancy in vacancies_list:
            query_result = check_vacancy_favorites_exists(
                vacancy_id=vacancy.get("vacancy_id"),
                user_tg_id=callback.from_user.id,
            )
            if not query_result.get("status"):
                text = BotErrorMessages.data_error.format(
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
                if query_result.get("check_status"):
                    kb = generation_inline_kb_with_url(
                        [
                            (
                                "Удалить из избранного",
                                f'{vacancy.get("vacancy_id")}_delete',
                                None,
                            ),
                            (
                                "Подробнее",
                                f'{vacancy.get("vacancy_id")}_details',
                                None,
                            ),
                            (
                                "Откликнуться на {}".format(
                                    vacancy.get("vacancy_source")
                                ),
                                None,
                                vacancy.get("vacancy_url"),
                            ),
                        ],
                        2,
                    )
                if not query_result.get("check_status"):
                    kb = generation_inline_kb_with_url(
                        [
                            (
                                "Добавить в избранное",
                                f'{vacancy.get("vacancy_id")}_favorites',
                                None,
                            ),
                            (
                                "Подробнее",
                                f'{vacancy.get("vacancy_id")}_details',
                                None,
                            ),
                            (
                                "Откликнуться на {}".format(
                                    vacancy.get("vacancy_source")
                                ),
                                None,
                                vacancy.get("vacancy_url"),
                            ),
                        ],
                        2,
                    )

            text = msg_info_vacancy(vacancy)
            await callback.message.answer(text=text, reply_markup=kb.as_markup())

        text = BotHandlerMessages.show_completed.format(
            user_name=callback.from_user.first_name
        )
        kb = generation_inline_kb(
            [ButtonData.favorites, ButtonData.re_enter_data], 2
        )
        await callback.message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.show_vacancies_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode), ShowManyVacanciesFilterr()
)
async def handle_show_many_vacancies_button(
    callback: CallbackQuery, state: FSMContext, page_number: int
):
    """
    Хендлер, отвечающий за показ пользователю найденных вакансий,
    в случае, если их больше 10.
    """
    await callback.answer()
    query_result = get_count_all_vacancies_user_location(
        user_tg_id=callback.from_user.id
    )
    if not query_result.get("status"):
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
        count_vacancies = query_result.get("count_vacancies")
        count_pages = ceil(count_vacancies / 10)
        query_result = get_ten_vacancies(
            user_tg_id=callback.from_user.id, page_number=page_number
        )
        if not query_result.get("status"):
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
            ten_vacancies = query_result.get("ten_vacancies")
            vacancies_list = [vacancy for vacancy in ten_vacancies.dicts()]
            for vacancy in vacancies_list:
                query_result = check_vacancy_favorites_exists(
                    vacancy_id=vacancy.get("vacancy_id"),
                    user_tg_id=callback.from_user.id,
                )
                if not query_result.get("status"):
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
                    if query_result.get("check_status"):
                        kb = generation_inline_kb_with_url(
                            [
                                (
                                    "Удалить из избранного",
                                    f'{vacancy.get("vacancy_id")}_delete',
                                    None,
                                ),
                                (
                                    "Подробнее",
                                    f'{vacancy.get("vacancy_id")}_details',
                                    None,
                                ),
                                (
                                    "Откликнуться на {}".format(
                                        vacancy.get("vacancy_source")
                                    ),
                                    None,
                                    vacancy.get("vacancy_url"),
                                ),
                            ],
                            2,
                        )
                    if not query_result.get("check_status"):
                        kb = generation_inline_kb_with_url(
                            [
                                (
                                    "Добавить в избранное",
                                    f'{vacancy.get("vacancy_id")}_favorites',
                                    None,
                                ),
                                (
                                    "Подробнее",
                                    f'{vacancy.get("vacancy_id")}_details',
                                    None,
                                ),
                                (
                                    "Откликнуться на {}".format(
                                        vacancy.get("vacancy_source")
                                    ),
                                    None,
                                    vacancy.get("vacancy_url"),
                                ),
                            ],
                            2,
                        )

                text = msg_info_vacancy(vacancy)
                await callback.message.answer(text=text, reply_markup=kb.as_markup())
            kb = generating_pagination_kb(page_number, count_pages)
            if page_number == count_pages:
                vacancies_shown = count_vacancies
            else:
                vacancies_shown = 10 * page_number
            text = BotHandlerMessages.show_information.format(
                user_name=callback.from_user.first_name,
                vacancies_shown=vacancies_shown,
                count_vacancies=count_vacancies
            )
            await callback.message.answer(
                text=text, reply_markup=kb.as_markup(),
            )
            await state.set_state(ApplicantState.show_vacancies_mode)


# хендлер переработан, проверить формирование последнего сообщения
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode), DetailsFilter()
)
async def handle_show_details_button(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, срабатывающий на нажатие кнопки 'Подробнее'"""
    await callback.answer()
    vacancy_id = callback.data.split("_")[0]
    query_result = get_one_vacancy(
        vacancy_id=vacancy_id, user_tg_id=callback.from_user.id
    )
    if not query_result.get("status"):
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
        vacancy = query_result.get("vacancy")
        vacancy_source = vacancy.vacancy_source
        # загрузка данных о вакансии
        if vacancy_source == "Работа России":
            result_loading = await load_one_vacancy_trudvsem(
                vacancy_id=vacancy.vacancy_id,
                company_code=vacancy.company_code,
            )
            if not result_loading.get("status"):
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
            else:
                vacancy = result_loading.get("vacancy")

        if vacancy_source == "hh.ru":
            result_loading = await load_one_vacancy_hh(vacancy_id=vacancy.vacancy_id)
            if not result_loading.get("status"):
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
                await callback.message.answer(
                    text=text, reply_markup=kb.as_markup()
                )
            else:
                vacancy = result_loading.get("vacancy")

        query_result = check_vacancy_favorites_exists(
            vacancy_id=vacancy.get("vacancy_id"),
            user_tg_id=callback.from_user.id,
        )
        if not query_result.get("status"):
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
            if query_result.get("check_status"):
                kb = generation_inline_kb_with_url(
                    [
                        (
                            "Удалить из избранного",
                            f'{vacancy.get("vacancy_id")}_delete',
                            None,
                        ),
                        (
                            "Свернуть",
                            f'{vacancy.get("vacancy_id")}_collapse',
                            None,
                        ),
                        (
                            "Откликнуться на {}".format(vacancy.get("vacancy_source")),
                            None,
                            vacancy.get("vacancy_url"),
                        ),
                    ],
                    2,
                )
            else:
                kb = generation_inline_kb_with_url(
                    [
                        (
                            "Добавить в избранное",
                            f'{vacancy.get("vacancy_id")}_favorites',
                            None,
                        ),
                        (
                            "Свернуть",
                            f'{vacancy.get("vacancy_id")}_collapse',
                            None,
                        ),
                        (
                            "Откликнуться на {}".format(vacancy.get("vacancy_source")),
                            None,
                            vacancy.get("vacancy_url"),
                        ),
                    ],
                    2,
                )
        text = msg_details_info_vacancy(vacancy)
        await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.show_vacancies_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode),
    CollapseDetailedFilter(),
)
async def handle_collapse_details_button(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, срабатывающий на нажатие кнопки 'Свернуть'"""
    await callback.answer()
    vacancy_id = callback.data.split("_")[0]
    query_result = get_one_vacancy(
        vacancy_id=vacancy_id, user_tg_id=callback.from_user.id
    )
    if not query_result.get("status"):
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
        vacancy = query_result.get("vacancy")

        query_result = check_vacancy_favorites_exists(
            vacancy_id=vacancy.vacancy_id,
            user_tg_id=callback.from_user.id,
        )
        if not query_result.get("status"):
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
            if query_result.get("check_status"):
                kb = generation_inline_kb_with_url(
                    [
                        (
                            "Удалить из избранного",
                            f"{vacancy.vacancy_id}_delete",
                            None,
                        ),
                        (
                            "Подробнее",
                            f"{vacancy.vacancy_id}_details",
                            None,
                        ),
                        (
                            "Откликнуться на {}".format(vacancy.vacancy_source),
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
                            "Добавить в избранное",
                            f"{vacancy.vacancy_id}_favorites",
                            None,
                        ),
                        (
                            "Подробнее",
                            f"{vacancy.vacancy_id}_details",
                            None,
                        ),
                        (
                            "Откликнуться на {}".format(vacancy.vacancy_source),
                            None,
                            vacancy.vacancy_url,
                        ),
                    ],
                    2,
                )
        text = msg_info_vacancy(vacancy.__dict__.get("__data__"))
        await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.show_vacancies_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode),
    AddVacancyFavoritesFilterr(),
)
async def handle_add_vacancy_favorites_button(
    callback: CallbackQuery, state: FSMContext, vacancy_id: str
):
    """Хендлер, срабатывающий на нажатие кнопки 'Добавить в избранное'"""
    await callback.answer()
    query_result = get_one_vacancy(
        vacancy_id=vacancy_id, user_tg_id=callback.from_user.id
    )
    if not query_result.get("status"):
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
        vacancy = query_result.get("vacancy")
        saving_result = saving_vacancy_favorites(
            vacancy_instance=vacancy, user_tg_id=callback.from_user.id
        )
        if not saving_result.get("status"):
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
            saved_vacancy = saving_result.get("instance")
            kb = generation_inline_kb_with_url(
                [
                    (
                        "Удалить из избранного",
                        f"{saved_vacancy.vacancy_id}_delete",
                        None,
                    ),
                    (
                        "Подробнее",
                        f"{saved_vacancy.vacancy_id}_details",
                        None,
                    ),
                    (
                        "Откликнуться на {}".format(saved_vacancy.vacancy_source),
                        None,
                        saved_vacancy.vacancy_url,
                    ),
                ],
                2,
            )
            text = msg_info_vacancy(
                vacancy=saved_vacancy.__dict__.get("__data__")
            )
            await callback.message.edit_text(
                text=text, reply_markup=kb.as_markup()
            )
            await state.set_state(ApplicantState.show_vacancies_mode)


# хендлер переработан
@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode),
    DeleteVacancyFilterr(),
)
async def handle_delete_vacancy_from_favorites_button(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, срабатывающий на нажатие кнопки 'Удалить из избранного'"""
    await callback.answer()
    vacancy_id = callback.data.split("_")[0]
    query_result = get_one_vacancy(
        vacancy_id=vacancy_id, user_tg_id=callback.from_user.id
    )
    if not query_result.get("status"):
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
        vacancy = query_result.get("vacancy")
        deleting_result = delete_vacancy_from_favorites(
            vacancy_id=vacancy.vacancy_id,
            user_tg_id=callback.from_user.id,
            vacancy_source=vacancy.vacancy_source,
        )
        if not deleting_result.get("status"):
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
                        "Добавить в избранное",
                        f"{vacancy.vacancy_id}_favorites",
                        None,
                    ),
                    (
                        "Подробнее",
                        f"{vacancy.vacancy_id}_details",
                        None,
                    ),
                    (
                        "Откликнуться на {}".format(vacancy.vacancy_source),
                        None,
                        vacancy.vacancy_url,
                    ),
                ],
                2,
            )
            text = msg_info_vacancy(vacancy.__dict__.get("__data__"))
            await callback.message.edit_text(
                text=text, reply_markup=kb.as_markup()
            )
            await state.set_state(ApplicantState.show_vacancies_mode)


# хендлер переработан
@router.callback_query(F.data == ButtonData.feedback[1])
async def handle_feedback_button(callback: CallbackQuery):
    """Хендлер, отвечающий за нажатие кнопки 'Обратная связь'."""
    await callback.answer()
    text = BotCommandPhrases.feedback_command.format(
        user_name=callback.from_user.first_name
    )
    kb = generation_inline_kb(
        [
            ButtonData.ready_favorites,
            ButtonData.bot_help,
            ButtonData.favorites,
        ],
        2,
    )
    await callback.message.edit_text(
        text=text, reply_markup=kb.as_markup()
    )
