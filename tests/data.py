from datetime import datetime

from aiogram.types import CallbackQuery, Chat, Message, Update, User

test_user = User(
    id=123456,
    is_bot=False,
    first_name='kirill',
    last_name='baraban',
    username='bks_lab_test',
)

test_chat = Chat(id=654321, type='private', username=test_user.username)


def get_message(test_text: str):
    return Message(
        message_id=123321,
        date=datetime.now(),
        chat=test_chat,
        from_user=test_user,
        text=test_text,
    )


def get_update(message: Message = None, callback: CallbackQuery = None):
    return Update(
        update_id=12323455,
        message=message,
        callback_query=callback,
    )
