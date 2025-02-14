from typing import Any, Iterable

from asyncpg import Record  # type: ignore
from sqlalchemy import select, join

from src.core.repositories.iemployee import IEmployeeRepository
from src.core.domain.employee import Employee, EmployeeIn
from src.db import (employee_table,database)
from src.infrastructure.dto.employeedto import EmployeeDTO


class EmployeeRepository(IEmployeeRepository):

    async def _get_by_id(self, id: int) -> Record | None:

        query = (
            employee_table.select()
            .where(employee_table.c.id == id)
            .order_by(employee_table.c.last_name.asc())
        )

        return await database.fetch_one(query)


    async def get_all_employees(self) -> Iterable[Any]:

        query = employee_table.select().order_by(employee_table.c.last_name.asc())
        employees = await database.fetch_all(query)

        return [Employee(**dict(employee)) for employee in employees]


    async def get_by_id(self, id: int) -> Any | None:

        employee = await self._get_by_id(id)
        return Employee(**dict(employee)) if employee else None


    async def get_by_email(self, email: str) -> Any | None:
        query = (
            employee_table.select()
            .where(employee_table.c.email == email)
        )

        employee = await database.fetch_one(query)
        return Employee(**dict(employee)) if employee else None


    async def get_by_last_name(self, last_name: str) -> Iterable[Any]:
        query = (
            employee_table.select()
            .where(employee_table.c.last_name == last_name)
            .order_by(employee_table.c.first_name.asc())
        )

        employees = await database.fetch_all(query)

        return [Employee(**dict(employee)) for employee in employees]


    async def add_employee(self, data: EmployeeIn) -> Any | None:
        query = employee_table.insert().values(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone_number=data.phone_number
    )
        new_employee_id = await database.execute(query)
        new_employee = await self._get_by_id(new_employee_id)

        return Employee(**dict(new_employee)) if new_employee else None


    async def update_employee(self, id: int, data: EmployeeIn) -> Any | None:
        if self._get_by_id(id):
            query = (
                employee_table.update()
                .where(employee_table.c.id == id)
                .values(
                    first_name=data.first_name,
                    last_name=data.last_name,
                    email=data.email,
                    phone_number=data.phone_number
                )
            )
            await database.execute(query)

            employee = await self._get_by_id(id)

            return Employee(**dict(employee)) if employee else None

        return None



    async def delete_employee(self, id: int) -> bool:
        if self._get_by_id(id):
            query = employee_table \
                .delete() \
                .where(employee_table.c.id == id)
            await database.execute(query)

            return True

        return False