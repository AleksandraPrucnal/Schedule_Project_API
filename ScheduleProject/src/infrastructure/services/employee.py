from typing import Iterable
from datetime import date, timedelta, datetime

from src.core.domain.employee import Employee
from src.core.repositories.iemployee import IEmployeeRepository
from src.infrastructure.dto.employeedto import  EmployeeDTO, EmployeeStatsDTO
from src.infrastructure.services.iemployee import IEmployeeService

from src.core.repositories.ischedule import IScheduleRepository
from src.core.repositories.iavailability import IAvailabilityRepository


class EmployeeService(IEmployeeService):

    _repository: IEmployeeRepository
    _schedule_repository: IScheduleRepository
    _availability_repository: IAvailabilityRepository

    def __init__(
        self,
        repository: IEmployeeRepository,
        schedule_repository: IScheduleRepository,
        availability_repository: IAvailabilityRepository
    ) -> None:
        
        self._repository = repository
        self._schedule_repository = schedule_repository
        self._availability_repository = availability_repository

    async def get_all_employees(self) -> Iterable[EmployeeDTO]:
        return await self._repository.get_all_employees()

    async def get_by_id(self, id: int) -> EmployeeDTO | None:
        return await self._repository.get_by_id(id)


    async def get_by_email(self, email: str) -> EmployeeDTO | None:
        return await self._repository.get_by_email(email)
    

    async def get_by_last_name(self, last_name: str) -> Iterable[EmployeeDTO]:
        return await self._repository.get_by_last_name(last_name)


    async def add_employee(self, data: Employee) -> Employee | None:
        return await self._repository.add_employee(data)


    async def update_employee(self, id: int, data: Employee) -> Employee | None:
        return await self._repository.update_employee(id=id,data=data)


    async def delete_employee(self, id: int) -> bool:
        return await self._repository.delete_employee(id)
    

    async def get_employee_stats(
        self, 
        employee_id: int,
        week_start: date,
        week_end: date
        ) -> EmployeeStatsDTO | None:

        schedules = await self._schedule_repository.get_by_employee(employee_id, week_start, week_end)
        availabilities = await self._availability_repository.get_by_employee(employee_id, week_start, week_end)

        total_shifts = len(schedules)

        total_hours = sum(
            (schedule.end_time.hour + schedule.end_time.minute / 60) - 
            (schedule.start_time.hour + schedule.start_time.minute / 60)
            for schedule in schedules
        )

        total_availability_hours = sum(
            (availability.shift.end_time.hour + availability.shift.end_time.minute / 60) - 
            (availability.shift.start_time.hour + availability.shift.start_time.minute / 60)
            for availability in availabilities
        )

        stats = EmployeeStatsDTO(
            total_hours=total_hours,
            total_availability_hours=total_availability_hours,
            total_shifts=total_shifts
        )

        return stats