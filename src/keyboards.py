from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="🔍 Search", callback_data="search"),
        InlineKeyboardButton(text="ℹ️ Info", callback_data="info")
    ).add(
        InlineKeyboardButton(text="🌎 Website", url="https://example.com")
    )
    return keyboard
