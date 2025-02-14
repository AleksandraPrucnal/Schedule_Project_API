from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Iterable
from src.core.domain.schedule import Schedule

class IScheduleRepository(ABC):

    @abstractmethod
    async def get_by_date(self, date: date) -> Iterable[Any] | None:
        pass

    @abstractmethod
    async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[Any] | None:
        pass

    @abstractmethod
    async def add_schedule(self, data: Schedule) -> Any | None:
        pass

    @abstractmethod
    async def get_by_position(self, position_type: str, date: date) -> Iterable[Any] | None:
        pass

    @abstractmethod
    async def update_schedule(self, date: date, data: Schedule) -> Any | None:
        pass

    @abstractmethod
    async def delete_schedule(self, id: int) -> bool:
        pass