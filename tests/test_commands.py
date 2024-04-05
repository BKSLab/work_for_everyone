from unittest.mock import AsyncMock

import pytest
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.methods import SendMessage
from aiogram.types import Message

from bot.fsm.fsm import ApplicantState
from bot.handlers.applicant_handlers import (
    start_command_processing,
    start_data_entry_processing,
)
from bot.keyboards.keyboards import generation_inline_kb
from bot.phrases.phrases_for_bot_messages import PHRASES_FOR_MESSAGE
from bot.phrases.texts_for_bot_buttons import ButtonData
from tests.data import get_message, get_update, test_chat, test_user


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_start_data_entry_processing(memory_storage, bot):
    callback = AsyncMock()
    state = FSMContext(
        storage=memory_storage,
        key=StorageKey(
            bot_id=bot.id,
            chat_id=test_chat.id,
            user_id=test_user.id,
        ),
    )
    await start_data_entry_processing(callback=callback, state=state)
    # assert state.get_data is None
    assert await state.get_state() == ApplicantState.federal_district_choice


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_start_command_processing(memory_storage, bot):
    message: Message = AsyncMock()
    state = FSMContext(
        storage=memory_storage,
        key=StorageKey(
            bot_id=bot.id,
            chat_id=test_chat.id,
            user_id=test_user.id,
        ),
    )
    await start_command_processing(message, state)
    assert await state.get_state() is None
    message.delete.assert_any_call()
    text = (
        f'<b>{message.from_user.first_name}'
        f'{PHRASES_FOR_MESSAGE.get("start_command")}'
    )
    kb = generation_inline_kb(
        [ButtonData.ready, ButtonData.bot_help, ButtonData.favorites], 2
    )
    message.answer.assert_called_with(text=text, reply_markup=kb.as_markup())


@pytest.mark.asyncio
async def test_start_cmd(dispatcher: Dispatcher, bot: Bot):
    res = await dispatcher.feed_update(
        bot=bot, update=get_update(message=get_message(test_text='/start'))
    )
    assert isinstance(res, SendMessage)
    text = (
        f'<b>{test_user.first_name}'
        f'{PHRASES_FOR_MESSAGE.get("start_command")}'
    )
    assert res.text == text
    assert (
        res.reply_markup
        == generation_inline_kb(
            [ButtonData.ready, ButtonData.bot_help, ButtonData.favorites], 2
        ).as_markup()
    )
