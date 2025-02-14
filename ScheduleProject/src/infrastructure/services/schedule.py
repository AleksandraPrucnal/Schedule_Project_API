from typing import Iterable
from datetime import date, timedelta, datetime

from src.infrastructure.exceptions.schedule import ScheduleValidationException
from src.core.domain.schedule import Schedule
from src.core.repositories.ischedule import IScheduleRepository

from src.core.repositories.iavailability import IAvailabilityRepository

from src.infrastructure.dto.scheduledto import ScheduleDTO
from src.infrastructure.dto.statsdto import StatsDTO
from src.infrastructure.services.ischedule import IScheduleService


from src.config import MIN_BREAK_HOURS



class ScheduleService(IScheduleService):

    _repository: IScheduleRepository
    _availability_repository: IAvailabilityRepository

    def __init__(self, repository: IScheduleRepository, availability_repository: IAvailabilityRepository
    ) -> None:
        self._repository = repository
        self._availability_repository = availability_repository


    async def get_by_date(self, date: date) -> Iterable[ScheduleDTO]:
        return await self._repository.get_by_date(date)


    async def get_by_employee(self, employee_id: int, week_start: date, week_end: date) -> Iterable[ScheduleDTO]:
        return await self._repository.get_by_employee(employee_id, week_start, week_end)
    

    async def get_by_position(self, position_type: str, date: date) -> Iterable[ScheduleDTO]:
        return await self._repository.get_by_position(position_type, date)



    async def add_schedule(self, data: Schedule) -> Schedule | None:
        
        availability = await self._availability_repository.get_by_employee(
            employee_id = data.employee_id,
            week_start = data.date,
            week_end = data.date
        )

        previous_day = data.date - timedelta(days=1)

        last_schedule = await self._repository.get_by_employee(
            employee_id = data.employee_id,
            week_start = previous_day,
            week_end = previous_day
        )
        
        if not availability:
            raise ScheduleValidationException("Pracownik jest niedostępny we wskazanym terminie.")
        
        for a in availability:
            if a.shift.start_time <= data.start_time and a.shift.end_time >= data.end_time:
                break
            else:
                raise ScheduleValidationException(
                    f"Pracownik jest dostępny tylko w godzinach {a.shift.start_time} - {a.shift.end_time}.")
            
        existing_schedules = await self._repository.get_by_employee(data.employee_id, data.date, data.date)
        for schedule in existing_schedules:
            if schedule.date == data.date:
                raise ScheduleValidationException("Pracownik ma już zmianę we wskazanym terminie.")
        
        for schedule in last_schedule:
            last_shift_end = datetime.combine(schedule.date, schedule.end_time)
            new_shift_start = datetime.combine(data.date, data.start_time)

            if new_shift_start - last_shift_end < timedelta(hours=MIN_BREAK_HOURS):
                raise ScheduleValidationException(
                    f"Minimalny odstęp miedzy kolejnymi zmianami wynosi: {MIN_BREAK_HOURS} godzin.")

        return await self._repository.add_schedule(data)



    async def update_schedule(self, id: int, data: Schedule) -> Schedule | None:

        availability = await self._availability_repository.get_by_employee(
            employee_id=data.employee_id,
            week_start=data.date,
            week_end=data.date
        )

        previous_day = data.date - timedelta(days=1)
        
        last_schedule = await self._repository.get_by_employee(
            employee_id = data.employee_id,
            week_start = previous_day,
            week_end = previous_day
        )
        
        if not availability:
            raise ScheduleValidationException("Pracownik jest niedostępny we wskazanym terminie.")
        
        for a in availability:
            if a.shift.start_time <= data.start_time and a.shift.end_time >= data.end_time:
                break
            else:
                raise ScheduleValidationException(
                    f"Pracownik jest dostępny tylko w godzinach {a.shift.start_time} - {a.shift.end_time}.")
        
        existing_schedules = await self._repository.get_by_employee(data.employee_id, data.date, data.date)
        for schedule in existing_schedules:
            if schedule.id != id and schedule.date == data.date:
                raise ScheduleValidationException("Pracownik ma już zmianę we wskazanym terminie.")
        
        for schedule in last_schedule:
            last_shift_end = datetime.combine(schedule.date, schedule.end_time)
            new_shift_start = datetime.combine(data.date, data.start_time)

            if new_shift_start - last_shift_end < timedelta(hours=MIN_BREAK_HOURS):
                raise ScheduleValidationException(
                    f"Minimalny odstęp miedzy kolejnymi zmianami wynosi: {MIN_BREAK_HOURS} godzin.")
            
        return await self._repository.update_schedule(id, data)



    async def delete_schedule(self, id: int) -> bool:
        return await self._repository.delete_schedule(id)



    async def get_stats(
        self, 
        week_start: date,
        week_end: date
        ) -> StatsDTO | None:

        total_hours = 0
        most_active_day_hours = 0
        most_active_day = None

        current_date = week_start  
        while current_date <= week_end:
            schedules = await self._repository.get_by_date(current_date)
            daily_hours = sum(
                (schedule.end_time.hour + schedule.end_time.minute / 60) -
                (schedule.start_time.hour + schedule.start_time.minute / 60)
                for schedule in schedules
            )

            if daily_hours > most_active_day_hours:
                most_active_day_hours = daily_hours
                most_active_day = current_date
                most_active_day_hours = most_active_day_hours

            total_hours += daily_hours
            current_date += timedelta(days=1)

        stats = StatsDTO(
            total_hours = total_hours,
            most_active_day = most_active_day,
            most_active_day_hours = most_active_day_hours,
        )
        return stats


"""
    async def get_employee_hours_summary(self, employee_id: int, week_start: date, week_end: date) -> int:

        schedules = await self._repository.get_by_employee(employee_id, week_start, week_end)

        total_hours = sum(
            (schedule.end_time.hour + schedule.end_time.minute / 60) - 
            (schedule.start_time.hour + schedule.start_time.minute / 60)
            for schedule in schedules
        )

        return round(total_hours, 2)
"""