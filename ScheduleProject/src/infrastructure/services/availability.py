from typing import Iterable

from datetime import date

from src.core.domain.availability import Availability
from src.core.repositories.iavailability import IAvailabilityRepository
from src.infrastructure.dto.availabilitydto import  AvailabilityDTO
from src.infrastructure.services.iavailability import IAvailabilityService


class AvailabilityService(IAvailabilityService):

    _repository: IAvailabilityRepository

    def __init__(self, repository: IAvailabilityRepository) -> None:
        self._repository = repository

    async def get_by_date(self, date: date) -> Iterable[AvailabilityDTO]:
        return await self._repository.get_by_date(date)

    async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[AvailabilityDTO]:
        return await self._repository.get_by_employee(employee_id, week_start, week_end)

    async def add_availability(self, data: Availability) -> Availability | None:
        return await self._repository.add_availability(data)

    async def update_availability(self, date: date, data: Availability) -> Availability | None:
        return await self._repository.update_availability(date, data)

    async def delete_availability(self, id: int) -> bool:
        return await self._repository.delete_availability(id)