from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from database.views import get_data_regions
from filters.filters import (
    CommanDdataEntryFilter,
    FederalDistrictFilter,
    NameLocalityFilter,
    RegionNameFilter,
)
from fsm.fsm import ApplicantState
from keyboards.keyboards import (
    bt_back_to_selection,
    generation_kb,
    kb_data_input,
    kb_start,
    kb_start_search_or_re_enter_data,
)
from phrases.phrases_for_bot_messages import PHRASES_FOR_MESSAGE
from phrases.texts_for_bot_buttons import TEXT_FOR_BUTTON
from utils.utils import message_generation

router = Router(name=__name__)


@router.message(CommandStart())
async def start_command_processing(message: Message):
    """Хендлер, срабатывающий на команду /start."""
    text = (
        f'{message.from_user.first_name}, '
        f'{PHRASES_FOR_MESSAGE.get("start_command")}'
    )
    await message.answer(
        text=text,
        reply_markup=kb_start.as_markup(),
    )
    await message.delete()


@router.message(Command(commands='help'))
async def help_command_processing(message: Message):
    """Хендлер, срабатывающий на команду /help."""
    text = (
        f'{message.from_user.first_name}, '
        f'{PHRASES_FOR_MESSAGE.get("help_command")}'
    )
    await message.answer(text=text, reply_markup=kb_data_input.as_markup())
    await message.delete()


@router.callback_query(F.data == 'bot_help')
async def bot_help_button_processing(callback: CallbackQuery):
    """Хендлер, срабатывающий на кнопку 'bot_help'."""
    text = (
        f'{callback.message.chat.first_name}, '
        f'{PHRASES_FOR_MESSAGE.get("help_command")}'
    )
    await callback.message.edit_text(
        text=text, reply_markup=kb_data_input.as_markup()
    )


@router.callback_query(CommanDdataEntryFilter())
async def ready_for_data_entry_button_processing(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, срабатывающий на кнопки 'ready' и 'data_input'."""
    await state.update_data(name_applicant=callback.from_user.first_name)
    await state.update_data(user_tg_id=callback.from_user.id)

    text = (
        f'{callback.message.chat.first_name}, '
        f'{PHRASES_FOR_MESSAGE.get("choice_federal_districts")}'
    )
    kb = generation_kb(list(TEXT_FOR_BUTTON.get('federal_districts').items()))
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.federal_district_choice)


@router.callback_query(
    StateFilter(ApplicantState.federal_district_choice),
    FederalDistrictFilter(),
)
async def federal_district_button_processing(
    callback: CallbackQuery, state: FSMContext
):
    """Хендлер, срабатывающий на выбор федерального округа."""
    await state.update_data(fd_code=int(callback.data))
    data = get_data_regions(int(callback.data))
    kb = generation_kb(data)
    kb.add(bt_back_to_selection).adjust(1)
    text = (
        f'{callback.message.chat.first_name}, '
        f'{PHRASES_FOR_MESSAGE.get("choice_region_name")}'
    )
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())
    await state.set_state(ApplicantState.region_name_choice)


@router.callback_query(
    StateFilter(ApplicantState.region_name_choice), RegionNameFilter()
)
async def region_name_button_processing(
    callback: CallbackQuery, state: FSMContext, region_name: str
):
    """Хендлер, срабатывающий на выбор региона."""
    await state.update_data(region_code=int(callback.data))
    await state.update_data(region_name=region_name)
    if callback.data in ['77', '78']:
        await state.update_data(location=region_name)
        entered_data = await state.get_data()
        text = message_generation(entered_data)
        await callback.message.edit_text(
            text=text,
            reply_markup=kb_start_search_or_re_enter_data.as_markup(),
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
    StateFilter(ApplicantState.local_name_input), NameLocalityFilter()
)
async def local_name_processing(
    message: Message,
    locality_name: str,
    state: FSMContext,
):
    await state.update_data(location=locality_name)
    entered_data = await state.get_data()
    text = message_generation(entered_data)
    await message.answer(
        text=text, reply_markup=kb_start_search_or_re_enter_data.as_markup()
    )
    await state.set_state(ApplicantState.verification_data)


@router.callback_query(
    StateFilter(ApplicantState.verification_data), F.data == 'start_searching'
)
async def start_searching_vacancies_processing(
    callback: CallbackQuery, state: FSMContext
):
    await callback.message.edit_text('Скоро здесь появятся вакансии')
