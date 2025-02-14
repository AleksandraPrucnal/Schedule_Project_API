from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from src.core.repositories.ishift import IShiftRepository
from src.core.domain.shift import Shift, ShiftIn
from src.db import (shift_table,database)
from src.infrastructure.dto.shiftdto import ShiftDTO


class ShiftRepository(IShiftRepository):

    async def _get_by_id(self, id: int) -> Record | None:

        query = (
            shift_table.select()
            .where(shift_table.c.id == id)
            .order_by(shift_table.c.start_time.asc())
        )

        return await database.fetch_one(query)


    async def get_all_shifts(self) -> Iterable[Any]:

        query = shift_table.select().order_by(shift_table.c.start_time.asc())
        shifts = await database.fetch_all(query)

        return [Shift(**dict(shift)) for shift in shifts]


    async def get_by_id(self, id: int) -> Any | None:

        shift = await self._get_by_id(id)
        return Shift(**dict(shift)) if shift else None
    

    async def add_shift(self, data: ShiftIn) -> Any | None:
        query = shift_table.insert().values(
            shift_type=data.shift_type,
            start_time=data.start_time,
            end_time=data.end_time,
    )
        new_shift_id = await database.execute(query)
        new_shift = await self._get_by_id(new_shift_id)

        return Shift(**dict(new_shift)) if new_shift else None


    async def update_shift(self, id: int, data: ShiftIn) -> Any | None:
        if self._get_by_id(id):
            query = (
                shift_table.update()
                .where(shift_table.c.id == id)
                .values(
                    shift_type=data.shift_type,
            start_time=data.start_time,
            end_time=data.end_time,
                )
            )
            await database.execute(query)

            shift = await self._get_by_id(id)

            return Shift(**dict(shift)) if shift else None

        return None
    
    
    async def delete_shift(self, id: int) -> bool:
        if self._get_by_id(id):
            query = shift_table \
                .delete() \
                .where(shift_table.c.id == id)
            await database.execute(query)

            return True

        return False

