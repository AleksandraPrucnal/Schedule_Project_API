from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Iterable
from src.core.domain.availability import Availability


class IAvailabilityRepository(ABC):

    @abstractmethod
    async def get_by_date(self, date: date) -> Iterable[Any] | None:
        pass

    @abstractmethod
    async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[Any] | None:
        pass

    @abstractmethod
    async def add_availability(self, data: Availability) -> Any | None:
        pass

    @abstractmethod
    async def update_availability(self, date: date, data: Availability) -> Any | None:
        pass

    @abstractmethod
    async def delete_availability(self, id: int) -> bool:
        pass