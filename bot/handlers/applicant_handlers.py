from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from keyboards.keyboards import kb_data_input, kb_start
from phrases.phrases_for_bot_messages import PHRASES_FOR_MESSAGE


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
    await message.answer(
        text=text,
        reply_markup=kb_data_input.as_markup()
    )
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


@router.callback_query(F.data.in_(['ready', 'data_input']))
async def ready_for_data_entry_button_processing(callback: CallbackQuery):
    """Хендлер, срабатывающий на кнопки 'ready' и 'data_input'."""
    text = f'{callback.message.chat.first_name}, далее выбор ФО'
    await callback.message.edit_text(text=text)
