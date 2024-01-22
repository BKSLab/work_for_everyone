from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.keyboards import kb_other
from phrases.phrases_for_bot_messages import PHRASES_FOR_MESSAGE

router = Router(name=__name__)


@router.message()
async def send_answer_unprocessed_messages(
    message: Message, state: FSMContext
):
    """
    Хендлер, обрабатывающий сообщения, не обработанные другими хендлерами.
    """
    text = (
        f'{message.from_user.first_name}, '
        f'{PHRASES_FOR_MESSAGE.get("other_answer")}'
    )
    await message.answer(text=text, reply_markup=kb_other.as_markup())
    await message.delete()
