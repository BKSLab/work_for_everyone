from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.views import get_data_regions
from filters.filters import FederalDistrictFilter, RegionNameFilter
from keyboards.keyboards import (bt_back_to_selection, generation_kb,
                                 kb_data_input, kb_start)
from phrases.phrases_for_bot_messages import PHRASES_FOR_MESSAGE
from phrases.texts_for_bot_buttons import TEXT_FOR_BUTTON

router = Router(name=__name__)
entered_data = {}


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


@router.callback_query(
    F.data.in_(['ready', 'data_input', 'back_to_selection_f_d'])
)
async def ready_for_data_entry_button_processing(callback: CallbackQuery):
    """Хендлер, срабатывающий на кнопки 'ready' и 'data_input'."""
    text = (
        f'{callback.message.chat.first_name}, '
        f'{PHRASES_FOR_MESSAGE.get("choice_federal_districts")}'
    )
    kb = generation_kb(list(TEXT_FOR_BUTTON.get('federal_districts').items()))
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())


@router.callback_query(FederalDistrictFilter())
async def federal_district_button_processing(callback: CallbackQuery):
    """Хендлер, срабатывающий на выбор федерального округа."""
    data = get_data_regions(int(callback.data))
    kb = generation_kb(data)
    kb.add(bt_back_to_selection).adjust(1)
    text = (
        f'{callback.message.chat.first_name}, '
        f'{PHRASES_FOR_MESSAGE.get("choice_region_name")}'
    )
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())


@router.callback_query(RegionNameFilter())
async def region_name_button_processing(callback: CallbackQuery):
    """Хендлер, срабатывающий на выбор региона."""
    await callback.message.edit_text(
        text=callback.data,
        # reply_markup=kb.as_markup()
    )
