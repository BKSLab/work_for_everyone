from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database.views import get_data_regions
from fsm.fsm import ApplicantState
from keyboards.keyboards import generation_inline_kb
from phrases.msg_generation import msg_verification
from phrases.phrases_for_bot_messages import PHRASES_FOR_MESSAGE
from phrases.texts_for_bot_buttons import ButtonData

router = Router(name=__name__)


@router.message()
async def send_answer_unprocessed_messages(
    message: Message, state: FSMContext
):
    """
    Хендлер, обрабатывающий сообщения, не обработанные другими хендлерами.
    """
    await message.delete()
    fsm_state = await state.get_state()
    if not fsm_state:
        text = (
            f'{message.from_user.first_name}'
            f'{PHRASES_FOR_MESSAGE.get("other_answer")}'
        )
        kb = generation_inline_kb([ButtonData.bot_help], 2)
        await message.edit_text(text=text, reply_markup=kb.as_markup())
    if fsm_state == ApplicantState.federal_district_choice:
        text_warning = (
            f'{message.from_user.first_name}'
            f'{PHRASES_FOR_MESSAGE.get("federal_district_wrong")}'
        )
        await message.answer(text=text_warning)
        kb = generation_inline_kb([*ButtonData.federal_districts], 1)
        text = (
            f'{message.from_user.first_name}, '
            f'{PHRASES_FOR_MESSAGE.get("choice_federal_districts")}'
        )
        await message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.federal_district_choice)

    if fsm_state == ApplicantState.region_name_choice:
        data = await state.get_data()
        fd_code = data.get('fd_code')
        text_warning = (
            f'{message.from_user.first_name}'
            f'{PHRASES_FOR_MESSAGE.get("region_name_wrong")}'
        )
        await message.answer(text=text_warning)
        data = get_data_regions(fd_code)
        data.append(ButtonData.back_to_selection_f_d)
        kb = generation_inline_kb(data, 1)
        text = (
            f'{message.from_user.first_name}, '
            f'{PHRASES_FOR_MESSAGE.get("choice_region_name")}'
        )
        await message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.region_name_choice)
    if fsm_state == ApplicantState.local_name_input:
        text_warning = (
            f'{message.from_user.first_name}'
            f'{PHRASES_FOR_MESSAGE.get("name_locality_wrong")}'
            f'<b>{message.text}</b>\nПредлагаю повторить попытку!'
        )
        await message.answer(text=text_warning)
        text = (
            f'{message.from_user.first_name}, '
            f'{PHRASES_FOR_MESSAGE.get("input_name_locality")}'
        )
        await message.answer(text=text)
        await state.set_state(ApplicantState.local_name_input)
    if fsm_state == ApplicantState.verification_data:
        text_warning = (
            f'{message.from_user.first_name}'
            f'{PHRASES_FOR_MESSAGE.get("data_checking_wrong")}'
        )
        await message.answer(text=text_warning)
        entered_data = await state.get_data()
        kb = generation_inline_kb(
            [ButtonData.start_searching, ButtonData.re_enter_data], 2
        )
        text = msg_verification(entered_data)
        await message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.verification_data)
