from abc import ABC, abstractmethod
from typing import Iterable
from datetime import date

from src.core.domain.schedule import Schedule
from src.infrastructure.dto.scheduledto import ScheduleDTO
from src.infrastructure.dto.statsdto import StatsDTO


class IScheduleService(ABC):

    @abstractmethod
    async def get_by_date(self, date: date) -> Iterable[ScheduleDTO]:
        pass

    @abstractmethod
    async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[ScheduleDTO]:
        pass

    @abstractmethod
    async def get_by_position(self, position_type: str, date: date) -> Iterable[ScheduleDTO]:
        pass

    @abstractmethod
    async def add_schedule(self, data: Schedule) -> Schedule | None:
        pass

    @abstractmethod
    async def update_schedule(self, id: int, data: Schedule) -> Schedule | None:
        pass

    @abstractmethod
    async def delete_schedule(self, id: int) -> bool:
        pass

    @abstractmethod
    async def get_stats(
        self, 
        week_start: date,
        week_end: date
        ) -> StatsDTO | None:
        pass
