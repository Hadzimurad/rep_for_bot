from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboard.reply import main_menu, menu_admin
from keyboard.Inline import main_inline




right_password = '4532'
class AdminLogIn(StatesGroup):
    waiting_for_password = State()
    admin_state = State()



def setup_commands(dp):

    @dp.message(CommandStart())
    async def cmd_start(message: types.Message):
        welcome_text = (
            f"👋 Привет, {message.from_user.first_name}!\n\n"
            f"Добро пожаловать в <b>Русфера</b> (Сургут)!\n\n"
            "Мы специализируемся на ремонте:\n"
            "🖨️ Принтеров и МФУ\n"
            "💻 Компьютеров и ноутбуков\n"
            "🖥️ Мониторов и периферии\n"
            "🏢 Оргтехники\n\n"
            "⚡ Быстро | 🎯 Качественно | ✅ С гарантией\n\n"
            "📍 г. Сургут, ул. Югорская, д. 34\n\n"
            "Выберите нужную услугу:"
        )
        await message.answer(welcome_text, parse_mode="HTML", reply_markup=main_menu())

    @dp.message(Command("admin"))
    async def cmd_admin(message: types.Message, state: FSMContext):
        admin_text = (
            "Для получения доступа к админ-панели\n"
            "<b>Введите пароль:</b>"
        )
        # await state.update_data(password=message.text)
        await message.answer(admin_text, parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(AdminLogIn.waiting_for_password)  
    
    @dp.message(AdminLogIn.waiting_for_password)
    async def procces_password(message: types.Message, state: FSMContext):
        user_data = await state.update_data(password=message.text)
        password_user = user_data.get('password')
        if (password_user == right_password): 
            await message.answer("Здравствуйте! Вы вошли в Админ панель", reply_markup=menu_admin())
            await state.set_state(AdminLogIn.admin_state)
        else:
            await message.answer("Пароль не верный\nПожалуйста повторите попытку", reply_markup=main_inline())

    @dp.message(Command("help"))
    async def cmd_help(message: types.Message):
        help_text = (
            "Доступные команды:\n"
            "/start - Главное меню\n"
            "/help - Помощь\n"
            "Используйте кнопки меню для навигации."
        )
        await message.answer(help_text)
