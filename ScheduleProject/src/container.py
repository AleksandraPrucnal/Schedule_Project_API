from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton


from src.infrastructure.repositories.employeedb import EmployeeRepository
from src.infrastructure.repositories.availabilitydb import AvailabilityRepository
from src.infrastructure.repositories.shiftdb import ShiftRepository
from src.infrastructure.repositories.scheduledb import ScheduleRepository

from src.infrastructure.services.employee import EmployeeService
from src.infrastructure.services.availability import AvailabilityService
from src.infrastructure.services.shift import ShiftService
from src.infrastructure.services.schedule import ScheduleService


class Container(DeclarativeContainer):
    employee_repository = Singleton(EmployeeRepository)
    availability_repository = Singleton(AvailabilityRepository)
    shift_repository = Singleton(ShiftRepository)
    schedule_repository = Singleton(ScheduleRepository)

    employee_service = Factory(
        EmployeeService,
        repository=employee_repository,
        availability_repository=availability_repository,
        schedule_repository = schedule_repository,
    )

    availability_service = Factory(
        AvailabilityService,
        repository = availability_repository,
    )

    shift_service = Factory(
        ShiftService,
        repository = shift_repository,
    )

    schedule_service = Factory(
        ScheduleService,
        repository = schedule_repository,
        availability_repository=availability_repository,
    )