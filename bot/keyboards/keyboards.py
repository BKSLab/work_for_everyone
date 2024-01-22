from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from phrases.texts_for_bot_buttons import TEXT_FOR_BUTTON


def generation_kb(data_list: List[tuple[str, int]]) -> InlineKeyboardBuilder:
    """
    Функция генерации клавиатур с inline кнопками
    для федеральных округов и регионов.
    """
    bt_list = [
        InlineKeyboardButton(text=x[0], callback_data=str(x[1]))
        for x in data_list
    ]
    builder = InlineKeyboardBuilder().row(*bt_list, width=1)
    return builder


# Создание клавиатуры для хендлера, обрабатывающего команду /start
bt_ready = InlineKeyboardButton(
    text=TEXT_FOR_BUTTON.get('ready'), callback_data='ready'
)

bt_help = InlineKeyboardButton(
    text=TEXT_FOR_BUTTON.get('bot_help'), callback_data='bot_help'
)

bt_back_to_selection = InlineKeyboardButton(
    text=TEXT_FOR_BUTTON.get('back_to_selection_f_d'),
    callback_data='back_to_selection_f_d',
)

bt_re_enter_data = InlineKeyboardButton(
    text=TEXT_FOR_BUTTON.get('re_enter_data'),
    callback_data='re_enter_data',
)

bt_start_searching = InlineKeyboardButton(
    text=TEXT_FOR_BUTTON.get('start_searching'),
    callback_data='start_searching',
)

# Создание билдера для хендлера, обрабатывающего команду /start
kb_start_search_or_re_enter_data = InlineKeyboardBuilder()
kb_start_search_or_re_enter_data.row(
    bt_re_enter_data, bt_start_searching, width=2
)

# Создание билдера для хендлера, обрабатывающего команду /start
kb_start = InlineKeyboardBuilder()
kb_start.row(bt_ready, bt_help, width=2)

# Создание билдера для хендлера, обрабатывающего необработанные сообщения
kb_other = InlineKeyboardBuilder()
kb_other.row(bt_help)

# Создание клавиатуры для хендлера, обрабатывающего
# команду /help и нажатие кнопки 'bot_help'
bt_data_input = InlineKeyboardButton(
    text=TEXT_FOR_BUTTON.get('data_input'), callback_data='data_input'
)

# Создание билдера для хендлера, обрабатывающего
# команду /help и нажатие кнопки 'bot_help'
kb_data_input = InlineKeyboardBuilder()
kb_data_input.row(bt_data_input)
