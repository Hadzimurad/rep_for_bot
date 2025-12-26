from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📞 Вызов мастера"),
                KeyboardButton(text="💰 Услуги и цены")
            ],
            [
                KeyboardButton(text="📍 Контакты"),
                KeyboardButton(text="📅 Запись на диагностику")
            ]
        ],
        resize_keyboard=True
    )


def menu_admin():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Записи на диагностику📅")
            ],
            [
                KeyboardButton(text="Выйти🚪")
            ]
        ],
        resize_keyboard=True
    )
