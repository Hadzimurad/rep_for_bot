from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboard.reply import main_menu, menu_admin
from keyboard.Inline import main_inline
from database_module.core import save_diagnostic, get_diagnostics_by_date
from datetime import datetime
from handlers.commands import AdminLogIn

# Константы компании
COMPANY_NAME = "Русфера"
COMPANY_CITY = "Сургут"
COMPANY_OFFICE_PHONE = "+7 (3462) 39-09-14"


# Создаем состояния для поэтапной записи на диагностику
class DiagnosticState(StatesGroup):
    waiting_for_date = State()
    waiting_for_time = State()
    waiting_for_name = State()
    waiting_for_number = State()


class AdminDiagnosticState(StatesGroup):
    waiting_for_date = State()


def validate_date(date_str: str) -> tuple[bool, str]:
    """Валидация даты: проверка формата и что дата не в прошлом"""
    try:
        date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if date_obj < today:
            return False, "❌ Дата не может быть в прошлом. Пожалуйста, введите актуальную дату."
        return True, ""
    except ValueError:
        return False, "❌ Неверный формат даты. Используйте формат ДД.ММ.ГГГГ (например, 25.12.2024)"


def validate_time(time_str: str) -> tuple[bool, str]:
    """Валидация времени: проверка формата"""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True, ""
    except ValueError:
        return False, "❌ Неверный формат времени. Используйте формат ЧЧ:ММ (например, 14:30)"


def validate_date_format(date_str: str) -> tuple[bool, str]:
    """Валидация только формата даты (без проверки на прошлое) - для админа"""
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True, ""
    except ValueError:
        return False, "❌ Неверный формат даты. Используйте формат ДД.ММ.ГГГГ (например, 25.12.2024)"


def setup_diagnostic(dp):
    """Регистрация хендлеров для записи на диагностику"""
    @dp.callback_query(F.data == 'сброс')
    async def callback_hadler(callback_query: types.CallbackQuery, state: FSMContext):
        await state.clear()
        await callback_query.message.answer(text="Дейстие отменено", reply_markup=main_menu())
        await callback_query.answer()


    @dp.message(F.text == "📅 Запись на диагностику")
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
            "<b>📝 Введите предпочтительную дату (в формате ДД.ММ.ГГГГ):</b>"
            
        )
        res2 = (
            "Если вы передумали в ходе записи на диагностику нажмите кнопку Сброс❌ для отмены записи."
        )
        await message.answer(response, parse_mode="HTML",reply_markup=types.ReplyKeyboardRemove())
        await message.answer(res2, parse_mode="HTML", reply_markup=main_inline())
        await state.set_state(DiagnosticState.waiting_for_date)
    
    @dp.message(DiagnosticState.waiting_for_date)
    async def process_date(message: types.Message, state: FSMContext):
        date_str = message.text.strip()
        is_valid, error_msg = validate_date(date_str)
        if not is_valid:
            await message.answer(error_msg + "\n\n<b>📝 Введите дату еще раз (формат ДД.ММ.ГГГГ):</b>", parse_mode="HTML")
            return
        
        await state.update_data(diagnostic_date=date_str)
        await message.answer("⏰ Теперь введите удобное время (в формате ЧЧ:ММ):")
        await state.set_state(DiagnosticState.waiting_for_time)

    @dp.message(DiagnosticState.waiting_for_time)
    async def process_time(message: types.Message, state: FSMContext):
        time_str = message.text.strip()
        is_valid, error_msg = validate_time(time_str)
        if not is_valid:
            await message.answer(error_msg + "\n\n<b>⏰ Введите время еще раз (формат ЧЧ:ММ):</b>", parse_mode="HTML")
            return
        
        await state.update_data(diagnostic_time=time_str)
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
        
        # Сохраняем запись в БД
        try:
            await save_diagnostic(
                user_id=message.from_user.id,
                username=message.from_user.username,
                name=data['diagnostic_name'],
                phone=data['diagnostic_number'],
                date=data['diagnostic_date'],
                time=data['diagnostic_time'],
            )
        except Exception as e:
            await message.answer(
                f"⚠️ Произошла ошибка при сохранении записи. Пожалуйста, попробуйте позже.",
                reply_markup=main_menu()
            )
            await state.clear()
            return
        
        result_message = (
            "✅ <b>Подтверждение записи на диагностику</b>\n\n"
            f"📅 Дата: <i>{data['diagnostic_date']}</i>\n"
            f"⏰ Время: <i>{data['diagnostic_time']}</i>\n"
            f"👤 Имя: <i>{data['diagnostic_name']}</i>\n"
            f"📱 Контактный номер: <i>{data['diagnostic_number']}</i>\n\n"
            "✅ <b>Ваша запись успешно сохранена!</b>"
        )
        await message.answer(result_message, parse_mode="HTML", reply_markup=main_menu())
        await state.clear()

    # Админ-функционал для просмотра записей
    @dp.message(F.text == "Записи на диагностику📅")
    async def admin_view_diagnostics(message: types.Message, state: FSMContext):
        """Админ: запрос даты для просмотра записей"""
        current_state = await state.get_state()
        # Проверяем, что пользователь в админ-панели
        if current_state != AdminLogIn.admin_state:
            await message.answer("❌ Доступно только администраторам. Используйте /admin для входа.")
            return
        
        await message.answer(
            "📅 <b>Просмотр записей на диагностику</b>\n\n"
            "Введите дату в формате <b>ДД.ММ.ГГГГ</b> для просмотра записей на этот день.\n"
            "Например: 25.12.2024",
            parse_mode="HTML"
        )
        await state.set_state(AdminDiagnosticState.waiting_for_date)

    @dp.message(AdminDiagnosticState.waiting_for_date)
    async def admin_process_date(message: types.Message, state: FSMContext):
        """Админ: обработка введенной даты и показ записей"""
        date_str = message.text.strip()
        is_valid, error_msg = validate_date_format(date_str)
        
        if not is_valid:
            await message.answer(
                error_msg + "\n\nВведите дату еще раз:",
                reply_markup=menu_admin()
            )
            return
        
        # Получаем записи на указанную дату
        try:
            records = await get_diagnostics_by_date(date_str)
            
            if not records:
                await message.answer(
                    f"📅 На дату <b>{date_str}</b> записей нет.",
                    parse_mode="HTML",
                    reply_markup=menu_admin()
                )
                await state.set_state(AdminLogIn.admin_state)
                return
            
            # Формируем сообщение со всеми записями
            lines = [f"📅 <b>Записи на {date_str}</b>\n"]
            for i, rec in enumerate(records, 1):
                lines.append(
                    f"\n<b>Запись #{i}</b>\n"
                    f"⏰ Время: {rec.time}\n"
                    f"👤 Имя: {rec.name}\n"
                    f"📱 Телефон: {rec.phone}\n"
                    f"🆔 Пользователь: @{rec.username if rec.username else 'не указан'}\n"
                    f"📝 ID записи: {rec.id}"
                )
            
            # Разбиваем на части если сообщение слишком длинное
            full_text = "\n".join(lines)
            if len(full_text) > 4000:
                # Разбиваем на части
                chunk = ""
                for line in lines:
                    if len(chunk + line) > 4000:
                        await message.answer(chunk, parse_mode="HTML")
                        chunk = line + "\n"
                    else:
                        chunk += line + "\n"
                if chunk:
                    await message.answer(chunk, parse_mode="HTML")
            else:
                await message.answer(full_text, parse_mode="HTML")
            
            await message.answer(
                f"✅ Всего записей на {date_str}: <b>{len(records)}</b>",
                parse_mode="HTML",
                reply_markup=menu_admin()
            )
            await state.set_state(AdminLogIn.admin_state)
            
        except Exception as e:
            await message.answer(
                f"⚠️ Произошла ошибка при получении записей: {str(e)}",
                reply_markup=menu_admin()
            )
            await state.set_state(AdminLogIn.admin_state)
