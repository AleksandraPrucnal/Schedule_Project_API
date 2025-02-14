from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from datetime import date

from src.container import Container
from src.core.domain.schedule import Schedule, ScheduleIn
from src.infrastructure.dto.scheduledto import ScheduleDTO
from src.infrastructure.dto.statsdto import StatsDTO
from src.infrastructure.services.ischedule import IScheduleService

router = APIRouter(tags = ["Schedule"])

@router.post("/create", response_model=Schedule, status_code=201)
@inject
async def create_schedule(
    schedule: ScheduleIn,
    service: IScheduleService = Depends(Provide[Container.schedule_service]),
) -> dict:
    extended_schedule_data = Schedule(
        **schedule.model_dump(),
    )
    new_schedule = await service.add_schedule(extended_schedule_data)
    return new_schedule.model_dump() if new_schedule else {}


@router.get("/date/{date}", response_model=Iterable[ScheduleDTO], status_code=200)
@inject
async def get_by_date(
    date: date,
    service: IScheduleService = Depends(Provide[Container.schedule_service]),
) -> Iterable:
    schedules = await service.get_by_date(date)
    return schedules


@router.get("/employee_id/{employee_id}", response_model=Iterable[ScheduleDTO], status_code=200)
@inject
async def get_by_employee(
    employee_id: int,
    week_start: date,
    week_end: date,
    service: IScheduleService = Depends(Provide[Container.schedule_service]),
) -> Iterable:
    schedules = await service.get_by_employee(employee_id, week_start, week_end)
    return schedules


@router.get("/position/{position_type}", response_model=Iterable[ScheduleDTO], status_code=200)
@inject
async def get_by_position(
    position_type: str,
    date: date,
    service: IScheduleService = Depends(Provide[Container.schedule_service]),
) -> Iterable:
    schedules = await service.get_by_position(position_type, date)
    return schedules



@router.put("/update/{id}", response_model=Schedule, status_code=200)
@inject
async def update_schedule(
    id: int,
    updated_schedule: ScheduleIn,
    service: IScheduleService = Depends(Provide[Container.schedule_service]),
) -> dict:
    if existing_schedule := await service.get_by_date(updated_schedule.date):
        updated_data = Schedule(**updated_schedule.model_dump())
        updated_schedule = await service.update_schedule(id, updated_data)
        return updated_schedule.model_dump() if updated_schedule else {}
    raise HTTPException(status_code=404, detail="Schedule not found")


@router.delete("/delete/{id}", status_code=204)
@inject
async def delete_schedule(
    id: int,
    service: IScheduleService = Depends(Provide[Container.schedule_service]),
) -> None:
    if await service.delete_schedule(id):
        return
    raise HTTPException(status_code=404, detail="Schedule not found")



@router.get("/employee_hours_summary", status_code=200)
@inject
async def get_employee_hours_summary(
    employee_id: int,
    start_date: date,
    end_date: date,
    service: IScheduleService = Depends(Provide[Container.schedule_service]),
) -> dict:
    total_hours = await service.get_employee_hours_summary(employee_id, start_date, end_date)
    return {"employee_id": employee_id, "total_hours": total_hours}



@router.get("/stats", response_model=StatsDTO, status_code=200)
@inject
async def get_stats(
    week_start: date,
    week_end: date,
    service: IScheduleService = Depends(Provide[Container.schedule_service])
) -> StatsDTO:
    return await service.get_stats(week_start, week_end)