from math import ceil

from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from api_trudvsem.api_requests import (
    get_data_one_vacancy,
    get_data_vacancies_from_api,
)
from api_trudvsem.data_processing import (
    preparing_data_for_vacancy_tb,
    preparing_data_one_vacancy,
)
from database.views import (
    check_vacancy_favorites_exists,
    delete_vacancy_from_favorites,
    deleting_vacancy_data,
    get_count_vacancies,
    get_data_regions,
    get_ten_vacancies,
    get_vacancies,
    get_vacancies_from_favorites,
    saving_applicant_data,
    saving_vacancies_data,
    saving_vacancy_favorites,
)
from filters.filters import (
    AddVacancyFavoritesFilterr,
    CollapseDetailedFilter,
    DeleteVacancyFavoritesFilterr,
    DetailsFilter,
    FavoritesFilterr,
    FederalDistrictFilter,
    NameLocalityFilter,
    RegionFilter,
    ShowManyVacanciesFilterr,
    StartDataEntryFilter,
)
from fsm.fsm import ApplicantState
from keyboards.keyboards import generating_pagination_kb, generation_inline_kb
from phrases.msg_generation import (
    msg_details_info_vacancy,
    msg_info_vacancy,
    msg_verification,
)
from phrases.phrases_for_bot_messages import PHRASES_FOR_MESSAGE
from phrases.texts_for_bot_buttons import ButtonData

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_processing(message: Message, state: FSMContext):
    """Хендлер, срабатывающий на команду /start."""
    await message.delete()
    await state.clear()
    text = (
        f'<b>{message.from_user.first_name}'
        f'{PHRASES_FOR_MESSAGE.get("start_command")}'
    )
    kb = generation_inline_kb(
        [ButtonData.ready, ButtonData.bot_help, ButtonData.favorites], 2
    )
    await message.answer(
        text=text,
        reply_markup=kb.as_markup(),
    )


@router.message(Command(commands='help'))
async def help_command_processing(message: Message):
    """Хендлер, срабатывающий на команду /help."""
    await message.delete()
    kb = generation_inline_kb([ButtonData.data_input], 1)
    text = (
        f'{message.from_user.first_name}'
        f'{PHRASES_FOR_MESSAGE.get("help_command")}'
    )
    await message.answer(text=text, reply_markup=kb.as_markup())


@router.callback_query(F.data == ButtonData.bot_help[1])
async def bot_help_button_processing(callback: CallbackQuery):
    """Хендлер, срабатывающий на кнопку 'Справка по боту'."""
    kb = generation_inline_kb([ButtonData.data_input], 1)
    text = (
        f'{callback.message.chat.first_name}'
        f'{PHRASES_FOR_MESSAGE.get("help_command")}'
    )
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())


@router.callback_query(StartDataEntryFilter())
async def start_data_entry_processing(
    callback: CallbackQuery,
    state: FSMContext,
):
    """
    Хендлер, срабатывающий на кнопки 'Готов начать' и 'Начать ввод данных'.
    Осуществляется запуск основной логике бота.
    """
    await state.clear()
    await state.update_data(name_applicant=callback.from_user.first_name)
    await state.update_data(user_tg_id=callback.from_user.id)
    kb = generation_inline_kb([*ButtonData.federal_districts], 1)
    text = (
        f'{callback.message.chat.first_name}'
        f'{PHRASES_FOR_MESSAGE.get("choice_federal_districts")}'
    )

    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.federal_district_choice)


@router.callback_query(
    StateFilter(ApplicantState.federal_district_choice),
    FederalDistrictFilter(),
)
async def choice_federal_district_processing(
    callback: CallbackQuery,
    state: FSMContext,
):
    """
    Хендлер, срабатывающий на выбор федерального округа.
    В соответствии с выбранным пользователем федеральным округом
    создается inline клавиатура с названиями регионов.
    """
    await state.update_data(fd_code=int(callback.data))

    data = get_data_regions(int(callback.data))
    data.append(ButtonData.back_to_selection_f_d)
    kb = generation_inline_kb(data, 1)
    text = (
        f'{callback.message.chat.first_name}'
        f'{PHRASES_FOR_MESSAGE.get("choice_region_name")}'
    )
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.region_name_choice)


@router.callback_query(
    StateFilter(ApplicantState.region_name_choice), RegionFilter()
)
async def choice_region_name_processing(
    callback: CallbackQuery,
    state: FSMContext,
    region_name: str,
):
    """
    Хендлер, срабатывающий на выбор пользователем региона,
    в федеральном округе.
    """
    await state.update_data(region_code=int(callback.data))
    await state.update_data(region_name=region_name)

    if callback.data in ['77', '78']:
        await state.update_data(location=region_name)
        entered_data = await state.get_data()
        kb = generation_inline_kb(
            [ButtonData.start_searching, ButtonData.re_enter_data], 2
        )
        text = msg_verification(entered_data)
        await callback.message.edit_text(
            text=text,
            reply_markup=kb.as_markup(),
        )
        await state.set_state(ApplicantState.verification_data)
    else:
        text = (
            f'{callback.message.chat.first_name}, '
            f'{PHRASES_FOR_MESSAGE.get("input_name_locality")}'
        )
        await callback.message.edit_text(text=text)
        await state.set_state(ApplicantState.local_name_input)


@router.message(
    StateFilter(ApplicantState.local_name_input),
    NameLocalityFilter(),
)
async def local_name_processing(
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
    kb = generation_inline_kb(
        [ButtonData.start_searching, ButtonData.re_enter_data], 2
    )
    text = msg_verification(entered_data)
    await message.answer(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.verification_data)


@router.callback_query(
    StateFilter(ApplicantState.verification_data),
    F.data == ButtonData.start_searching[1],
)
async def start_searching_vacancies_processing(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, отвечающий за обработку кнопки 'Начать поиск вакансий'."""
    await callback.message.edit_text(
        text=(
            f'{callback.message.chat.first_name}'
            f'{PHRASES_FOR_MESSAGE.get("process_of_searching")}'
        )
    )
    instance = saving_applicant_data(await state.get_data())
    responce = get_data_vacancies_from_api(instance.region.region_code)
    if responce.get('status'):
        processed_data = preparing_data_for_vacancy_tb(
            responce.get('data'), instance.location, callback.from_user.id
        )
        if not processed_data.get('status'):
            await callback.message.edit_text(processed_data.get('error_text'))
        else:
            deleting_vacancy_data(callback.from_user.id)
            saving_vacancies_data(processed_data.get('vacancies'))
    else:
        await callback.message.edit_text(responce.get('error_text'))

    count_vacancies = get_count_vacancies(callback.from_user.id)
    await state.update_data(count_vacancies=count_vacancies)
    if count_vacancies == 0:
        kb = generation_inline_kb([ButtonData.re_enter_data], 1)
        text = (
            f'{callback.message.chat.first_name}, '
            f'{PHRASES_FOR_MESSAGE.get("vacancies_not_found")}'
            f'{instance.location}'
        )
        await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
    else:
        if count_vacancies <= 10:
            kb = generation_inline_kb([ButtonData.show_few_vacancies], 1)
        else:
            kb = generation_inline_kb([ButtonData.show_many_vacancies], 1)
        text = (
            f'{str(count_vacancies)}'
            f'{PHRASES_FOR_MESSAGE.get("show_vacancies")}'
        )
        await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
        await state.set_state(ApplicantState.show_vacancies_mode)


@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode),
    F.data == ButtonData.show_few_vacancies[1],
)
async def show_few_vacancies_processing(
    callback: CallbackQuery,
    state: FSMContext,
):
    """
    Хендлер, отвечающий за показ пользователю найденных вакансий,
    в случае, если их меньше или равно 10.
    """
    select_vacancies = get_vacancies(callback.from_user.id)
    vacancies_list = [vacancy for vacancy in select_vacancies.dicts()]
    for vacancy in vacancies_list:
        if check_vacancy_favorites_exists(
            vacancy.get('company_code'),
            vacancy.get('vacancy_id'),
            callback.from_user.id,
        ):
            kb = generation_inline_kb(
                [
                    (
                        'Удалить из избранного',
                        f'{vacancy.get("vacancy_id")}_delete',
                    ),
                    ('Подробнее', f'{vacancy.get("vacancy_id")}_details'),
                ],
                2,
            )
        else:
            kb = generation_inline_kb(
                [
                    (
                        'Добавить в избранное',
                        f'{vacancy.get("vacancy_id")}_favorites',
                    ),
                    ('Подробнее', f'{vacancy.get("vacancy_id")}_details'),
                ],
                2,
            )

        text = msg_info_vacancy(vacancy)

        await callback.message.answer(text=text, reply_markup=kb.as_markup())

    text = (
        f'{callback.message.chat.first_name}, '
        f'{PHRASES_FOR_MESSAGE.get("show_completed")}'
    )

    kb = generation_inline_kb(
        [ButtonData.favorites, ButtonData.re_enter_data], 2
    )
    await callback.message.answer(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.show_vacancies_mode)


@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode), ShowManyVacanciesFilterr()
)
async def show_many_vacancies_processing(
    callback: CallbackQuery, state: FSMContext, page_number: int
):
    """
    Хендлер, отвечающий за показ пользователю найденных вакансий,
    в случае, если их больше 10.
    """
    count_vacancies = get_vacancies(callback.from_user.id).count()
    count_pages = ceil(count_vacancies / 10)
    vacancies = get_ten_vacancies(callback.from_user.id, page_number)
    vacancies_list = [vacancy for vacancy in vacancies.dicts()]
    for vacancy in vacancies_list:
        if check_vacancy_favorites_exists(
            vacancy.get('company_code'),
            vacancy.get('vacancy_id'),
            callback.from_user.id,
        ):
            kb = generation_inline_kb(
                [
                    (
                        'Удалить из избранного',
                        f'{vacancy.get("vacancy_id")}_delete',
                    ),
                    ('Подробнее', f'{vacancy.get("vacancy_id")}_details'),
                ],
                2,
            )
        else:
            kb = generation_inline_kb(
                [
                    (
                        'Добавить в избранное',
                        f'{vacancy.get("vacancy_id")}_favorites',
                    ),
                    ('Подробнее', f'{vacancy.get("vacancy_id")}_details'),
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
    await callback.message.answer(
        text=(
            f'Показано {vacancies_shown} из {count_vacancies} найденных '
            f'вакансий\n\n{callback.message.chat.first_name}, используй '
            'для навигации кнопки <b>"Вперед"</b> и <b>"Назад"</b>.\n'
            'Подходящие вакансии можешь добавлять в избранное.'
        ),
        reply_markup=kb.as_markup(),
    )
    await state.set_state(ApplicantState.show_vacancies_mode)


@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode), DetailsFilter()
)
async def show_details_processing(
    callback: CallbackQuery, state: FSMContext, vacancy: dict, mode: str
):
    """Хендлер, срабатывающий на нажатие кнопки 'Подробнее'"""
    responce = get_data_one_vacancy(
        vacancy.get('company_code'), vacancy.get('vacancy_id')
    )
    if responce.get('status'):
        processed_data = preparing_data_one_vacancy(responce.get('data'))
        if not processed_data.get('status'):
            await callback.message.answer(processed_data.get('error_text'))
        else:
            if mode == 'details.fav':
                kb = generation_inline_kb(
                    [
                        (
                            'Удалить из избранного',
                            f'{vacancy.get("vacancy_id")}_delete.fav',
                        ),
                        (
                            'Свернуть',
                            f'{vacancy.get("vacancy_id")}_collapse.fav',
                        ),
                    ],
                    2,
                )
            elif mode == 'details':
                if check_vacancy_favorites_exists(
                    vacancy.get('company_code'),
                    vacancy.get('vacancy_id'),
                    callback.from_user.id,
                ):
                    kb = generation_inline_kb(
                        [
                            (
                                'Удалить из избранного',
                                f'{vacancy.get("vacancy_id")}_delete',
                            ),
                            (
                                'Свернуть',
                                f'{vacancy.get("vacancy_id")}_collapse',
                            ),
                        ],
                        2,
                    )
                else:
                    kb = generation_inline_kb(
                        [
                            (
                                'Добавить в избранное',
                                f'{vacancy.get("vacancy_id")}_favorites',
                            ),
                            (
                                'Свернуть',
                                f'{vacancy.get("vacancy_id")}_collapse',
                            ),
                        ],
                        2,
                    )
            text = msg_details_info_vacancy(processed_data.get('vacancy'))
            await callback.message.edit_text(
                text=text, reply_markup=kb.as_markup()
            )
            await state.set_state(ApplicantState.show_vacancies_mode)
    else:
        await callback.message.answer(responce.get('error_text'))


@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode),
    CollapseDetailedFilter(),
)
async def collapse_details_processing(
    callback: CallbackQuery, state: FSMContext, vacancy: dict, mode: str
):
    """Хендлер, срабатывающий на нажатие кнопки 'Свернуть'"""
    if mode == 'collapse.fav':
        kb = generation_inline_kb(
            [
                (
                    'Удалить из избранного',
                    f'{vacancy.get("vacancy_id")}_delete.fav',
                ),
                ('Подробнее', f'{vacancy.get("vacancy_id")}_details.fav'),
            ],
            2,
        )
    elif mode == 'collapse':
        if check_vacancy_favorites_exists(
            vacancy.get('company_code'),
            vacancy.get('vacancy_id'),
            callback.from_user.id,
        ):
            kb = generation_inline_kb(
                [
                    (
                        'Удалить из избранного',
                        f'{vacancy.get("vacancy_id")}_delete',
                    ),
                    ('Подробнее', f'{vacancy.get("vacancy_id")}_details'),
                ],
                2,
            )
        else:
            kb = generation_inline_kb(
                [
                    (
                        'Добавить в избранное',
                        f'{vacancy.get("vacancy_id")}_favorites',
                    ),
                    ('Подробнее', f'{vacancy.get("vacancy_id")}_details'),
                ],
                2,
            )
    text = msg_info_vacancy(vacancy)
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.show_vacancies_mode)


@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode),
    AddVacancyFavoritesFilterr(),
)
async def add_vacancy_favorites_processing(
    callback: CallbackQuery, state: FSMContext, vacancy: dict
):
    """Хендлер, срабатывающий на нажатие кнопки 'В избранное'"""
    saving_vacancy_favorites(vacancy)
    kb = generation_inline_kb(
        [
            ('Удалить из избранного', f'{vacancy.get("vacancy_id")}_delete'),
            ('Подробнее', f'{vacancy.get("vacancy_id")}_details'),
        ],
        2,
    )
    text = msg_info_vacancy(vacancy)
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.show_vacancies_mode)


@router.callback_query(
    StateFilter(ApplicantState.show_vacancies_mode),
    DeleteVacancyFavoritesFilterr(),
)
async def delete_vacancy_from_favorites_processing(
    callback: CallbackQuery, state: FSMContext, vacancy: dict, mode: str
):
    """Хендлер, срабатывающий на нажатие кнопки 'Удалить из избранного'"""
    vacancy_name = vacancy.get('vacancy_name')
    delete_vacancy_from_favorites(
        vacancy.get('company_code'),
        vacancy.get('vacancy_id'),
        callback.from_user.id,
    )
    if mode == 'delete':
        kb = generation_inline_kb(
            [
                (
                    'Добавить в избранное',
                    f'{vacancy.get("vacancy_id")}_favorites',
                ),
                ('Подробнее', f'{vacancy.get("vacancy_id")}_details'),
            ],
            2,
        )
        text = msg_info_vacancy(vacancy)
        await callback.message.edit_text(text=text, reply_markup=kb)
    else:
        await callback.message.edit_text(
            f'Вакансия {vacancy_name} удалена из избранного'
        )
    await state.set_state(ApplicantState.show_vacancies_mode)


@router.callback_query(
    FavoritesFilterr(),
)
async def favorites_processing(
    callback: CallbackQuery,
    state: FSMContext,
):
    """Хендлер, отвечающий за обработку кнопки 'Перейти в избранное'"""
    vacancies = get_vacancies_from_favorites(callback.from_user.id)
    if not vacancies:
        kb = generation_inline_kb([ButtonData.ready, ButtonData.bot_help], 2)
        text = (
            f'{callback.message.chat.first_name}'
            f'{PHRASES_FOR_MESSAGE.get("no_vacancies_in_favorites")}'
        )
        await callback.message.edit_text(
            text=text, reply_markup=kb.as_markup()
        )
        await state.set_state(ApplicantState.federal_district_choice)
    else:
        await callback.message.delete()
        await callback.message.answer(
            f'Всего добавлено {vacancies.count()} вакансий в избранное'
        )
        vacancies_list = [vacancy for vacancy in vacancies.dicts()]
        for vacancy in vacancies_list:
            kb = generation_inline_kb(
                [
                    (
                        'Удалить из избранного',
                        f'{vacancy.get("vacancy_id")}_delete.fav',
                    ),
                    ('Подробнее', f'{vacancy.get("vacancy_id")}_details.fav'),
                ],
                2,
            )
            text = msg_info_vacancy(vacancy)

            await callback.message.answer(
                text=text, reply_markup=kb.as_markup()
            )
            await state.set_state(ApplicantState.show_vacancies_mode)

        text = (
            f'{callback.message.chat.first_name}'
            f'{PHRASES_FOR_MESSAGE.get("message_in_favorites")}'
        )
        kb = generation_inline_kb(
            [
                ButtonData.data_input,
                ButtonData.bot_help,
            ],
            2,
        )
        await callback.message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.show_vacancies_mode)


@router.message(Command(commands='favorites'))
async def favorites_command_processing(message: Message, state: FSMContext):
    """Хендлер, отвечающий за обработку команды /favorites."""
    vacancies = get_vacancies_from_favorites(message.from_user.id)
    if not vacancies:
        await message.delete()
        kb = generation_inline_kb([ButtonData.ready, ButtonData.bot_help], 2)
        text = (
            f'{message.from_user.first_name}'
            f'{PHRASES_FOR_MESSAGE.get("no_vacancies_in_favorites")}'
        )
        await message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.federal_district_choice)
    else:
        await message.delete()
        await message.answer(
            f'Всего добавлено {vacancies.count()} вакансий в избранное'
        )
        vacancies_list = [vacancy for vacancy in vacancies.dicts()]
        for vacancy in vacancies_list:
            kb = generation_inline_kb(
                [
                    (
                        'Удалить из избранного',
                        f'{vacancy.get("vacancy_id")}_delete.fav',
                    ),
                    ('Подробнее', f'{vacancy.get("vacancy_id")}_details.fav'),
                ],
                2,
            )
            text = msg_info_vacancy(vacancy)

            await message.answer(text=text, reply_markup=kb.as_markup())
            await state.set_state(ApplicantState.show_vacancies_mode)

        text = (
            f'{message.from_user.first_name}'
            f'{PHRASES_FOR_MESSAGE.get("message_in_favorites")}'
        )
        kb = generation_inline_kb(
            [
                ButtonData.data_input,
                ButtonData.bot_help,
            ],
            2,
        )
        await message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.show_vacancies_mode)


@router.message(Command(commands='cancel'))
async def cancel_command_processing(message: Message, state: FSMContext):
    """Хендлер, отвечающий за обработку команды /cancel."""
    await message.delete()
    text = (
        f'{message.from_user.first_name}'
        f'{PHRASES_FOR_MESSAGE.get("cancel")}'
    )
    kb = generation_inline_kb(
        [ButtonData.data_input, ButtonData.bot_help, ButtonData.favorites],
        2,
    )
    await message.answer(text=text, reply_markup=kb.as_markup())
    await state.clear()


@router.message(Command(commands='feedback'))
async def feedback_command_processing(message: Message):
    """Хендлер, отвечающий за обработку команды /feedback."""
    await message.delete()
    text = (
        f'<b>{message.from_user.first_name}'
        f'{PHRASES_FOR_MESSAGE.get("feedback")}'
    )
    kb = generation_inline_kb(
        [ButtonData.data_input, ButtonData.bot_help, ButtonData.favorites],
        2,
    )
    await message.answer(text=text, reply_markup=kb.as_markup())
