from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from data_operations.get_data import get_vacancies_from_favorites
from fsm.fsm import ApplicantState
from keyboards.keyboards import (
    generation_inline_kb,
    generation_inline_kb_with_url,
)
from loading_vacancies.load_vacancies_hh import load_one_vacancy_hh
from loading_vacancies.load_vacancies_trudvsem import load_one_vacancy_trudvsem
from phrases.msg_generation import msg_info_vacancy_favorites
from phrases.phrases_for_bot_messages import (
    BotCommandPhrases,
    BotErrorMessages,
    BotHandlerMessages,
)
from phrases.texts_for_bot_buttons import ButtonData


router = Router(name=__name__)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """Хендлер, срабатывающий на команду /start."""
    await message.delete()
    await state.clear()
    text = BotCommandPhrases.start_command.format(
        user_name=message.from_user.first_name
    )
    kb = generation_inline_kb(
        [
            ButtonData.ready,
            ButtonData.bot_help,
            ButtonData.favorites,
            ButtonData.feedback,
        ],
        2,
    )
    await message.answer(
        text=text,
        reply_markup=kb.as_markup(),
    )


@router.message(Command(commands='help'))
async def help_command(message: Message):
    """Хендлер, срабатывающий на команду /help."""
    await message.delete()
    text = BotCommandPhrases.help_command.format(
        user_name=message.from_user.first_name
    )
    kb = generation_inline_kb([ButtonData.data_input], 1)
    await message.answer(text=text, reply_markup=kb.as_markup())


@router.message(Command(commands='feedback'))
async def feedback_command(message: Message):
    """Хендлер, отвечающий за обработку команды /feedback."""
    await message.delete()
    text = BotCommandPhrases.feedback_command.format(
        user_name=message.from_user.first_name
    )
    kb = generation_inline_kb(
        [
            ButtonData.ready_favorites,
            ButtonData.bot_help,
            ButtonData.favorites,
        ],
        2,
    )
    await message.answer(text=text, reply_markup=kb.as_markup())


@router.message(Command(commands='cancel'))
async def cancel_command(message: Message, state: FSMContext):
    """Хендлер, отвечающий за обработку команды /cancel."""
    await message.delete()
    text = BotCommandPhrases.cancel_command.format(
        user_name=message.from_user.first_name
    )
    kb = generation_inline_kb(
        [
            ButtonData.data_input,
            ButtonData.bot_help,
            ButtonData.favorites,
        ],
        2,
    )
    await message.answer(text=text, reply_markup=kb.as_markup())
    await state.clear()


@router.message(Command(commands='favorites'))
async def favorites_command(message: Message, state: FSMContext):
    """Хендлер, отвечающий за обработку команды /favorites."""
    await message.delete()
    query_result = get_vacancies_from_favorites(
        user_tg_id=message.from_user.id
    )
    if not query_result.get('status'):
        text = BotErrorMessages.favorites_error.format(
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
        vacancies = query_result.get('vacancies')
        if not vacancies:
            text = BotHandlerMessages.no_vacancies_in_favorites.format(
                user_name=message.from_user.first_name
            )
            kb = generation_inline_kb(
                [ButtonData.ready, ButtonData.bot_help], 2
            )

            await message.answer(text=text, reply_markup=kb.as_markup())
            await state.set_state(ApplicantState.federal_district_choice)
        else:
            vacancies_list = [vacancy for vacancy in vacancies.dicts()]
            for vacancy in vacancies_list:
                status_archival = False
                # проверка актуальности вакансий, добавленных в избранное
                vacancy_source = vacancy.get('vacancy_source')
                if vacancy_source == 'Работа России':
                    result_loading = await load_one_vacancy_trudvsem(
                        vacancy_id=vacancy.get('vacancy_id'),
                        company_code=vacancy.get('company_code'),
                    )
                    result_loading = {'status': False}
                    # проверка актуальности вакансии после запроса
                    # к сайту Работа России
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
                        text = BotErrorMessages.trudvsem_request_error.format(
                            user_name=message.from_user.first_name
                        )
                        kb = generation_inline_kb(
                            [
                                ButtonData.feedback,
                            ],
                            1,
                        )
                        await message.answer(
                            text=text, reply_markup=kb.as_markup()
                        )
                if vacancy_source == 'hh.ru':
                    result_loading = await load_one_vacancy_hh(
                        vacancy_id=vacancy.get('vacancy_id')
                    )
                    if not result_loading.get('status'):
                        text = BotErrorMessages.hh_request_error.format(
                            user_name=message.from_user.first_name
                        )
                        kb = generation_inline_kb(
                            [
                                ButtonData.feedback,
                            ],
                            1,
                        )
                        await message.answer(
                            text=text, reply_markup=kb.as_markup()
                        )
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
                                (
                                    f'{vacancy.get("vacancy_id")}_'
                                    'favorites.delete'
                                ),
                                None,
                            ),
                            (
                                'Подробнее',
                                (
                                    f'{vacancy.get("vacancy_id")}_'
                                    'favorites.details'
                                ),
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
                    await message.answer(
                        text=text, reply_markup=kb.as_markup()
                    )
                    await state.set_state(ApplicantState.show_vacancies_mode)

                if status and not status_archival:
                    kb = generation_inline_kb_with_url(
                        [
                            (
                                'Удалить из избранного',
                                (
                                    f'{vacancy.get("vacancy_id")}_'
                                    'favorites.delete'
                                ),
                                None,
                            ),
                            (
                                'Подробнее',
                                (
                                    f'{vacancy.get("vacancy_id")}_'
                                    'favorites.details'
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
                    text = msg_info_vacancy_favorites(
                        vacancy=vacancy, status_information=status_information
                    )
                    await message.answer(
                        text=text, reply_markup=kb.as_markup()
                    )
                    await state.set_state(ApplicantState.show_vacancies_mode)

                if not status:
                    kb = generation_inline_kb_with_url(
                        [
                            (
                                'Удалить из избранного',
                                (
                                    f'{vacancy.get("vacancy_id")}_'
                                    'favorites.delete'
                                ),
                                None,
                            ),
                        ],
                        1,
                    )
                    text = msg_info_vacancy_favorites(
                        vacancy=vacancy, status_information=status_information
                    )
                    await message.answer(
                        text=text, reply_markup=kb.as_markup()
                    )
                    await state.set_state(ApplicantState.show_vacancies_mode)

            text = BotHandlerMessages.message_in_favorites.format(
                user_name=message.from_user.first_name,
                vacancies_count=vacancies.count(),
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
