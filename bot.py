import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers.commands import setup_commands
from handlers.menu_buttons import setup_menu_buttons
from handlers.diagnostic import setup_diagnostic
from database_module.database import init_db

TOKEN = BOT_TOKEN

# Константы компании Русфера - Сургут
# COMPANY_NAME = "Русфера"
# COMPANY_CITY = "Сургут"
# COMPANY_ADDRESS = "Югорская, 34"
# COMPANY_OFFICE_PHONE = "+7 (3462) 39-09-14"
# COMPANY_EMAIL = "it@rusftera.ru"
# COMPANY_WEBSITE = "https://rusfera.ru"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация хендлеров
setup_commands(dp)
setup_diagnostic(dp)
setup_menu_buttons(dp)

# Запуск бота
async def main():
    logger.info("Бот запускается...")
    try:
        # Инициализация БД
        await init_db()
        logger.info("База данных инициализирована")
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
