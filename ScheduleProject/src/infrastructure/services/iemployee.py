from abc import ABC, abstractmethod
from typing import Iterable
from datetime import date, timedelta, datetime

from src.core.domain.employee import Employee
from src.infrastructure.dto.employeedto import EmployeeDTO, EmployeeStatsDTO


class IEmployeeService(ABC):

    @abstractmethod
    async def get_all_employees(self) -> Iterable[EmployeeDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> EmployeeDTO | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> EmployeeDTO | None:
        pass

    @abstractmethod
    async def get_by_last_name(self, last_name: str) -> Iterable[Employee]:
        pass

    @abstractmethod
    async def add_employee(self, data: Employee) -> Employee | None:
        pass

    @abstractmethod
    async def update_employee (self, id: int, data: Employee) -> Employee | None:
        pass

    @abstractmethod
    async def delete_employee(self, id: int) -> bool:
        pass

    @abstractmethod
    async def get_employee_stats(self, employee_id: int, week_start: date, week_end: date) -> EmployeeStatsDTO | None:
        pass