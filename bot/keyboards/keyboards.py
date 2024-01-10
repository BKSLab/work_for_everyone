from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from phrases.texts_for_bot_buttons import TEXT_FOR_BUTTON

# Создание клавиатуры для хендлера, обрабатывающего команду /start
bt_ready = InlineKeyboardButton(
    text=TEXT_FOR_BUTTON.get('ready'), callback_data='ready'
)

bt_help = InlineKeyboardButton(
    text=TEXT_FOR_BUTTON.get('bot_help'), callback_data='bot_help'
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
