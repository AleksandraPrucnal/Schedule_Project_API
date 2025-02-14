from datetime import date
from typing import Any, Iterable
from sqlalchemy import select, join, func

from src.core.repositories.ischedule import IScheduleRepository
from src.core.domain.schedule import Schedule, ScheduleIn
from src.db import (schedule_table, employee_table, database)
from src.infrastructure.dto.scheduledto import ScheduleDTO


class ScheduleRepository(IScheduleRepository):

    async def _get_by_id(self, id: int) -> Any | None:
        query = (
            select(schedule_table, employee_table)
            .select_from(
                join(
                    schedule_table,
                    employee_table,
                    schedule_table.c.employee_id == employee_table.c.id,
                )
            )
            .where(schedule_table.c.id == id)
        )
        return await database.fetch_one(query)

    async def get_by_date(self, date: date) -> Iterable[Any] | None:
        query = (
            select(schedule_table, employee_table)
            .select_from(
                join(
                    schedule_table,
                    employee_table,
                    schedule_table.c.employee_id == employee_table.c.id,
                )
            )
            .where(schedule_table.c.date == date)
        )
        return await database.fetch_all(query)
    

    async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[Any] | None:
        query = (
            select(schedule_table, employee_table)
            .select_from(
                join(
                    schedule_table,
                    employee_table,
                    schedule_table.c.employee_id == employee_table.c.id,
                )
            )
            .where(schedule_table.c.employee_id == employee_id)
            .where(schedule_table.c.date.between(week_start, week_end))
        )
        schedules = await database.fetch_all(query)
        return [Schedule(**dict(schedule)) for schedule in schedules]
    

    async def get_by_position(self, position_type: str, date: date) -> Iterable[Any]| None:
        query = (
            select(schedule_table, employee_table)
            .select_from(
                join(
                    schedule_table,
                    employee_table,
                    schedule_table.c.employee_id == employee_table.c.id,
                )
            )
            .where(schedule_table.c.position_type == position_type)
            .where(schedule_table.c.date == date)
        )
        schedules = await database.fetch_all(query)
        return [Schedule(**dict(schedule)) for schedule in schedules]


    async def add_schedule(self, data: Schedule) -> Any | None:
        query = schedule_table.insert().values(
            employee_id=data.employee_id,
            date=data.date,
            position_type=data.position_type,
            start_time=data.start_time,
            end_time=data.end_time,
        )
        new_schedule_id = await database.execute(query)
        new_schedule = await self._get_by_id(new_schedule_id)

        return Schedule(**dict(new_schedule)) if new_schedule else None


    async def update_schedule(self, id: int, data: Schedule) -> Any | None:
        if await self._get_by_id(id):
            query = (
                schedule_table.update()
                .where(schedule_table.c.id == id)
                .values(
                    employee_id=data.employee_id,
                    date=data.date,
                    position_type=data.position_type,
                    start_time=data.start_time,
                    end_time=data.end_time,
                )
            )
            await database.execute(query)

            updated_schedule = await self._get_by_id(id)
            return Schedule(**dict(updated_schedule)) if updated_schedule else None

        return None

    async def delete_schedule(self, id: int) -> bool:
        if await self._get_by_id(id):
            query = schedule_table.delete().where(schedule_table.c.id == id)
            await database.execute(query)
            return True
        return False