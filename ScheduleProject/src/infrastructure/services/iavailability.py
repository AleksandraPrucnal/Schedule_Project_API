from abc import ABC, abstractmethod
from typing import Iterable

from datetime import date

from src.core.domain.availability import Availability
from src.infrastructure.dto.availabilitydto import AvailabilityDTO


class IAvailabilityService(ABC):

    @abstractmethod
    async def get_by_date(self, date: date) -> Iterable[AvailabilityDTO]:
        pass

    @abstractmethod
    async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[AvailabilityDTO]:
        pass

    @abstractmethod
    async def add_availability(self, data: Availability) -> Availability | None:
        pass

    @abstractmethod
    async def update_availability(self, date: date, data: Availability) -> Availability | None:
        pass

    @abstractmethod
    async def delete_availability(self, id: int) -> bool:
        pass