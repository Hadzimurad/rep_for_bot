import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')

# Константы компании Русфера - Сургут
COMPANY_NAME = "Русфера"
COMPANY_CITY = "Сургут"
COMPANY_ADDRESS = "Югорская, 34"
COMPANY_OFFICE_PHONE = "+7 (3462) 39-09-14"
COMPANY_EMAIL = "it@rusftera.ru"
COMPANY_WEBSITE = "https://rusfera.ru"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создаем состояния для поэтапной записи на диагностику
class DiagnosticState(StatesGroup):
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_name = State()
    waiting_for_number = State()


# Создаем клавиатуру
def make_main_keyboard():
    buttons = [
        [
            KeyboardButton(text="📞 Вызов мастера"),
            KeyboardButton(text="💰 Услуги и цены")
        ],
        [
            KeyboardButton(text="📍 Контакты"),
            KeyboardButton(text="📅 Запись на диагностику")
        ],
        [
            KeyboardButton(text="Сброс❌")
        ]

    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=False)

# Команда старт
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        f"Добро пожаловать в <b>{COMPANY_NAME}</b> ({COMPANY_CITY})!\n\n"
        "Мы специализируемся на ремонте:\n"
        "🖨️ Принтеров и МФУ\n"
        "💻 Компьютеров и ноутбуков\n"
        "🖥️ Мониторов и периферии\n"
        "🏢 Оргтехники\n\n"
        "⚡ Быстро | 🎯 Качественно | ✅ С гарантией\n\n"
        "📍 г. Сургут, ул. Югорская, д. 34\n\n"
        "Выберите нужную услугу:"
    )
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=make_main_keyboard())

# Команда help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "Доступные команды:\n"
        "/start - Главное меню\n"
        "/help - Помощь\n"
        "/cancel - Отмена текущего действия\n\n"
        "Используйте кнопки меню для навигации."
    )
    await message.answer(help_text)

# Команда кнопки "Сброс❌"
@dp.message(lambda message: message.text == "Сброс❌")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Действие отменено. Используйте кнопки меню.",
        reply_markup=make_main_keyboard()
    )

# Обработка кнопки "📞 Вызов мастера"
@dp.message(lambda message: message.text == "📞 Вызов мастера")
async def handle_call_master(message: types.Message):
    response = (
        "🛠️ <b>Вызов мастера на дом/офис</b>\n\n"
        f"📞 <b>Компания {COMPANY_NAME} — {COMPANY_CITY}</b>\n\n"
        "✅ Приедем быстро и проверим технику\n"
        "✅ Диагностика бесплатно\n"
        "✅ Работаем 6 дней в неделю\n"
        "✅ Гарантия на ремонт\n\n"
        
        "<b>📞 Позвоните нам:</b>\n"
        f"• {COMPANY_OFFICE_PHONE} (офис)\n\n"
        
        "💰 <b>Стоимость выезда:</b> \n"
        "350 руб. (входит в стоимость ремонта)\n\n"
        
        "⏰ <b>Время приезда:</b>\n"
        "По городу Сургут — 1-2 часа\n\n"
        
        f"📍 <b>Адрес:</b> ул. {COMPANY_ADDRESS}"
    )
    await message.answer(response, parse_mode="HTML")

# Обработка кнопки "💰 Услуги и цены"
@dp.message(lambda message: message.text == "💰 Услуги и цены")
async def handle_prices(message: types.Message):
    response = (
        "💼 <b>Услуги и цены — Русфера</b>\n\n"
        
        "<b>🖨️ Принтеры и МФУ:</b>\n"
        "• Диагностика — <b>бесплатно!</b>\n"
        "• Прочистка печатающих головок — 1500 руб.\n"
        "• Замена картриджа/тонера — от 800 руб.\n"
        "• Замена СНПЧ — от 2500 руб.\n"
        "• Ремонт механики — от 2500 руб.\n"
        "• Замена термопленки — от 3000 руб.\n\n"
        
        "<b>💻 Компьютеры и ноутбуки:</b>\n"
        "• Диагностика — <b>бесплатно!</b>\n"
        "• Чистка от пыли — от 1500 руб.\n"
        "• Замена термопасты — 500 руб.\n"
        "• Замена жесткого диска — от 1500 руб.\n"
        "• Установка ОС/ПО — от 1000 руб.\n"
        "• Замена комплектующих — от 800 руб.\n"
        "• Восстановление данных — от 3000 руб.\n\n"
        
        "<b>🖥️ Мониторы и периферия:</b>\n"
        "• Диагностика — <b>бесплатно!</b>\n"
        "• Ремонт мониторов — от 2000 руб.\n"
        "• Замена клавиатуры — от 1500 руб.\n"
        "• Ремонт ИБП — от 1500 руб.\n"
        "• Настройка сетей — от 2000 руб.\n\n"
        
        "🏢 <b>Услуги для организаций:</b>\n"
        "• Договор на обслуживание — специальные цены\n"
        "• Выезд специалиста на место — согласовано\n\n"
        
        "📋 <b>Полный прайс-лист:</b>\n"
        f"{COMPANY_WEBSITE}/price\n\n"
        "<i>* Окончательная стоимость после диагностики</i>"
    )
    await message.answer(response, parse_mode="HTML")



# Обработка кнопки "📍 Контакты"
@dp.message(lambda message: message.text == "📍 Контакты")
async def handle_contacts(message: types.Message):
    response = (
        f"📍 <b>Контакты — {COMPANY_NAME}</b>\n\n"
        
        f"<b>Сервисный центр:</b>\n"
        f"г. {COMPANY_CITY}\n"
        f"ул. {COMPANY_ADDRESS}\n\n"
        
        "<b>⏰ График работы:</b>\n"
        "Пн-Пт: 9:00 - 19:00\n"
        "Сб: 10:00 - 16:00\n"
        "Вс: выходной\n\n"
        
        "<b>☎️ Телефоны:</b>\n"
        f"• {COMPANY_OFFICE_PHONE}\n\n"
        
        "<b>✉️ Электронная почта:</b>\n"
        f"• {COMPANY_EMAIL}\n"
        "• support@rusftera.ru (техподдержка)\n\n"
        
        f"<b>🌐 Сайт:</b> {COMPANY_WEBSITE}\n\n"
        
        f"💡 <b>Совет:</b> Звоните перед визитом!\n"
        "Мы работаем по графику работы."
    )
    
    await message.answer(response, parse_mode="HTML")

# Обработка кнопки "📅 Запись на диагностику"
@dp.message(lambda message: message.text == "📅 Запись на диагностику")
async def handle_appointment(message: types.Message, state: FSMContext):
    response = (
        "📅 <b>Запись на бесплатную диагностику</b>\n\n"
        f"🎁 <b>Компания {COMPANY_NAME} ({COMPANY_CITY}) дарит:</b>\n"
        "✅ Полная бесплатная диагностика техники\n"
        "✅ Консультация опытного специалиста\n"
        "✅ Письменная смета на ремонт\n"
        "✅ Гарантия 30 дней на ремонт\n\n"
        
        "<b>Способы записи:</b>\n\n"
        f"1. 📞 <b>Позвоните:</b>\n{COMPANY_OFFICE_PHONE}\n\n"
        
        "2. 💬 <b>Через этот бот:</b>\n"
        
        "Если запись будет призводиться через бота\n"
        "<b>📝 Введите предпочтительную дату (в формате ДД.ММ.ГГГГ):</b>\n\n"
        "Если вы передумали в ходе записи на диагностику нажмите кнопку Сброс❌ для отмены записи."
    )
    await message.answer(response, parse_mode="HTML")
    await state.set_state(DiagnosticState.waiting_for_date)

@dp.message(DiagnosticState.waiting_for_date)
async def process_date(message: types.Message, state: FSMContext):
    await state.update_data(diagnostic_date=message.text)
    await message.answer("⏰ Теперь введите удобное время (в формате ЧЧ:ММ):")
    await state.set_state(DiagnosticState.waiting_for_time)

@dp.message(DiagnosticState.waiting_for_time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(diagnostic_time=message.text)
    await message.answer("👤 Пожалуйста, введите ваше имя:")
    await state.set_state(DiagnosticState.waiting_for_name)

@dp.message(DiagnosticState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(diagnostic_name=message.text)
    await message.answer("📱 Пожалуйста, введите ваш контактный номер телефона:")
    await state.set_state(DiagnosticState.waiting_for_number)

@dp.message(DiagnosticState.waiting_for_number)
async def process_number(message: types.Message, state: FSMContext):
    await state.update_data(diagnostic_number=message.text)
    data = await state.get_data()

    result_message = (
        "✅ <b>Подтверждение записи на диагностику</b>\n\n"
        f"📅 Дата: <i>{data['diagnostic_date']}</i>\n"
        f"⏰ Время: <i>{data['diagnostic_time']}</i>\n"
        f"👤 Имя: <i>{data['diagnostic_name']}</i>\n"
        f"📱 Контактный номер: <i>{data['diagnostic_number']}</i>\n\n"
    )
    await message.answer(result_message, parse_mode="HTML")
    await state.clear()

# Обработка любого другого текста
@dp.message()
async def handle_other_messages(message: types.Message):
    await message.answer(
        "Пожалуйста, используйте кнопки меню или команды.\n"
        "Для начала работы нажмите /start",
        reply_markup=make_main_keyboard()
    )

# Запуск бота
async def main():
    logger.info("Бот запускается...")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    finally:
        await bot.session.close()
        logger.info("Сессия бота закрыта")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Программа завершена")
        print("\n✅ Бот успешно остановлен")