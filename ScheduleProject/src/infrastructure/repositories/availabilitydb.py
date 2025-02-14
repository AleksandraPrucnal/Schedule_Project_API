from typing import Any, Iterable

from datetime import date

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from src.core.repositories.iavailability import IAvailabilityRepository
from src.core.domain.availability import Availability, AvailabilityIn
from src.db import (availability_table, employee_table, shift_table, database)
from src.infrastructure.dto.availabilitydto import AvailabilityDTO


class AvailabilityRepository(IAvailabilityRepository):

    async def _get_by_id(self, id: int) -> Record | None :
        query = (
            select(availability_table, employee_table, shift_table)
            .select_from(
                join(
                    availability_table,
                    employee_table,
                    availability_table.c.employee_id == employee_table.c.id
                ).join(
                    shift_table,
                    availability_table.c.shift_id == shift_table.c.id
                )
            )
            .where(availability_table.c.id == id)
            .order_by(availability_table.c.shift_id.asc())
        )
        return await database.fetch_one(query)



    async def get_by_date(self, date: date) -> Iterable[Any] | None:
        query = (
            select(availability_table, employee_table, shift_table)
            .select_from(
                join(
                    availability_table,
                    employee_table,
                    availability_table.c.employee_id == employee_table.c.id
                ).join(
                    shift_table,
                    availability_table.c.shift_id == shift_table.c.id
                )
            )
            .where(availability_table.c.date == date)
        )
        return await database.fetch_all(query)
    

    """
    async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[Any] | None:
        query = (
            select(
                availability_table.c.id,
                availability_table.c.employee_id,
                availability_table.c.date,
                availability_table.c.shift_id,
                shift_table.c.start_time,
                shift_table.c.end_time
            )
            .select_from(
                join(
                    availability_table,
                    shift_table,
                    availability_table.c.shift_id == shift_table.c.id 
                )
            )
            .where(availability_table.c.employee_id == employee_id)
            .where(availability_table.c.date.between(week_start, week_end))
        )

        results = await database.fetch_all(query)
        return [AvailabilityDTO.from_record(result) for result in results]
    """


    async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[Any] | None:
        query = (
            select(
                availability_table.c.id,
                availability_table.c.employee_id,
                availability_table.c.date,
                shift_table.c.id.label("shift_id"),
                shift_table.c.shift_type,
                shift_table.c.start_time,
                shift_table.c.end_time
            )
            .select_from(
                join(
                    availability_table,
                    shift_table,
                    availability_table.c.shift_id == shift_table.c.id
                )
            )
            .where(availability_table.c.employee_id == employee_id)
            .where(availability_table.c.date.between(week_start, week_end))
        )
        availabilities = await database.fetch_all(query)
        print("Fetched availabilities:", [dict(a) for a in availabilities])
        return [AvailabilityDTO.from_record(result) for result in availabilities]


    

    async def add_availability(self, data: Availability) -> Any | None:
        query = availability_table.insert().values(
            employee_id=data.employee_id,
            date=data.date,
            shift_id=data.shift_id,
            )
        new_availability_id = await database.execute(query)
        new_availability = await self._get_by_id(new_availability_id)

        return Availability(**dict(new_availability)) if new_availability else None


    async def update_availability(self, date: date, data: Availability) -> Any | None:
        if self._get_by_id(id):
            query = (
                availability_table.update()
                .where(availability_table.c.id == id)
                .values(
                    employee_id=data.employee_id,
                    date=data.date,
                    shift_id=data.shift_id,
                )
            )
            await database.execute(query)

            availability = await self._get_by_id(id)
            return Availability(**dict(availability)) if availability else None
        
        return None


    async def delete_availability(self, id: int) -> bool:
        if self._get_by_id(id):
            query = availability_table \
                .delete() \
                .where(availability_table.c.id == id)
            await database.execute(query)

            return True

        return False



    """
        async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[Availability]:
        query = (
            select(
                availability_table.c.id,
                availability_table.c.employee_id,
                availability_table.c.date,
                availability_table.c.shift_id,
                shift_table.c.start_time,
                shift_table.c.end_time
            )
            .select_from(
                join(
                    availability_table,
                    shift_table,
                    availability_table.c.shift_id == shift_table.c.id  # Poprawiony warunek `ON`
                )
            )
            .where(availability_table.c.employee_id == employee_id)
            .where(availability_table.c.date.between(week_start, week_end))
        )

        results = await database.fetch_all(query)

        availabilities = [
            Availability(
                id=result["id"],
                employee_id=result["employee_id"],
                date=result["date"],
                shift_id=result["shift_id"],
                start_time=result["start_time"],
                end_time=result["end_time"]
            )
            for result in results
        ]
        return availabilities


    async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[Any] | None:
        query = (
            select(
            availability_table.c.id,
            availability_table.c.employee_id,
            availability_table.c.date,
            availability_table.c.shift_id,
            shift_table.c.start_time,
            shift_table.c.end_time
        )
            .select_from(
                join(
                    availability_table,
                    employee_table,
                    availability_table.c.employee_id == employee_table.c.id
                ).join(
                    availability_table,
                    shift_table,
                    availability_table.c.shift_id == shift_table.c.id
                )
            )
            .where(availability_table.c.employee_id == employee_id)
            .where(availability_table.c.date.between(week_start, week_end))
        )
        results = await database.fetch_all(query)
        availabilities = [
            Availability(
                id=result["id"],
                employee_id=result["employee_id"],
                date=result["date"],
                shift_id=result["shift_id"],
                start_time=result["start_time"],
                end_time=result["end_time"]
            )
            for result in results
        ]
        return availabilities
    """