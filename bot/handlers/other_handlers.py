from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from data_operations.get_data import get_data_lst_regions
from fsm.fsm import ApplicantState
from keyboards.keyboards import generation_inline_kb
from phrases.msg_generation import msg_verification
from phrases.phrases_for_bot_messages import BotErrorMessages, BotHandlerMessages
from phrases.texts_for_bot_buttons import ButtonData


router = Router(name=__name__)

# хендлер переработан
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
        text = BotErrorMessages.reply_unprocessed_msg.format(
            user_name=message.from_user.first_name
        )
        kb = generation_inline_kb([ButtonData.bot_help], 2)
        await message.answer(text=text, reply_markup=kb.as_markup())
    if fsm_state == ApplicantState.federal_district_choice:
        text = BotErrorMessages.federal_district_wrong.format(
            user_name=message.from_user.first_name
        )
        await message.answer(text=text)
        kb = generation_inline_kb([*ButtonData.federal_districts], 1)
        
        text = BotHandlerMessages.choice_federal_districts.format(
            user_name=message.from_user.first_name
        )
        await message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.federal_district_choice)

    if fsm_state == ApplicantState.region_name_choice:
        data = await state.get_data()
        fd_code = data.get('fd_code')
        text = BotErrorMessages.region_name_wrong.format(
            user_name=message.from_user.first_name
        )
        await message.answer(text=text)
        data = get_data_lst_regions(fd_code)
        data.append(ButtonData.back_to_selection_f_d)
        kb = generation_inline_kb(data, 1)
        text = BotHandlerMessages.choice_region_name.format(
            user_name=message.from_user.first_name
        )
        await message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.region_name_choice)
    if fsm_state == ApplicantState.local_name_input:
        text = BotErrorMessages.name_locality_wrong.format(
            user_name=message.from_user.first_name,
            user_location=message.text
        )
        await message.answer(text=text)
        text = BotHandlerMessages.input_name_locality.format(
            user_name=message.from_user.first_name
        )
        await message.answer(text=text)
        await state.set_state(ApplicantState.local_name_input)
    if fsm_state == ApplicantState.verification_data:
        text = BotErrorMessages.data_checking_wrong.format(
            user_name=message.from_user.first_name
        )
        await message.answer(text=text)
        entered_data = await state.get_data()
        kb = generation_inline_kb(
            [ButtonData.start_searching, ButtonData.re_enter_data], 2
        )
        text = msg_verification(entered_data)
        await message.answer(text=text, reply_markup=kb.as_markup())
        await state.set_state(ApplicantState.verification_data)
