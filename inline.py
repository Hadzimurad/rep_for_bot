from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_inline():
    inline_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Сброс❌',
                    callback_data='сброс'
                )
            ]
        ]
    )
    return inline_menu
