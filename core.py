from sqlalchemy import select
from database_module.models import Diagnostic
from database_module.database import async_session
from typing import List, Optional


async def save_diagnostic(
    user_id: Optional[int],
    username: Optional[str],
    name: str,
    phone: str,
    date: str,
    time: str,
) -> Diagnostic:
    """Сохранить запись на диагностику в БД"""
    async with async_session() as session:
        diagnostic = Diagnostic(
            user_id=user_id,
            username=username,
            name=name,
            phone=phone,
            date=date,
            time=time,
        )
        session.add(diagnostic)
        await session.commit()
        await session.refresh(diagnostic)
        return diagnostic

"""Получить все записи на указанную дату"""
async def get_diagnostics_by_date(date: str) -> List[Diagnostic]:
    async with async_session() as session:
        result = await session.execute(
            select(Diagnostic).where(Diagnostic.date == date).order_by(Diagnostic.time)
        )
        return list(result.scalars().all())

"""Получить все записи (последние limit записей)"""
async def get_all_diagnostics(limit: int = 10) -> List[Diagnostic]:
    async with async_session() as session:
        result = await session.execute(
            select(Diagnostic).order_by(Diagnostic.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())
