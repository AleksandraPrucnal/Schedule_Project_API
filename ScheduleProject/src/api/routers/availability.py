from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
#from jose import jwt

#from src.infrastructure.utils import consts
from src.container import Container

from datetime import date

from src.core.domain.availability import Availability, AvailabilityIn
from src.infrastructure.dto.availabilitydto import AvailabilityDTO
from src.infrastructure.services.iavailability import IAvailabilityService

#bearer_scheme = HTTPBearer()

router = APIRouter(tags = ["Availability"])

@router.post("/create", response_model=Availability, status_code=201)
@inject
async def create_availability(
    availability: AvailabilityIn,``
    service: IAvailabilityService = Depends(Provide[Container.availability_service]),
) -> dict:
    extended_availability_data = Availability(
        **availability.model_dump(),
    )
    new_availability = await service.add_availability(extended_availability_data)
    return new_availability.model_dump() if new_availability else {}


@router.get("/date/{date}", response_model=Iterable[AvailabilityDTO], status_code=200)
@inject
async def get_by_date(
    date: date,
    service: IAvailabilityService = Depends(Provide[Container.availability_service]),
) -> Iterable:
    availabilities= await service.get_by_date(date)
    return availabilities


@router.get("/employee_id/{employee_id}", response_model=Iterable[AvailabilityDTO], status_code=200)
@inject
async def get_by_employee(
    employee_id: int,
    week_start: date,
    week_end: date,
    service: IAvailabilityService = Depends(Provide[Container.availability_service]),
) -> Iterable:
    
    availabilities = await service.get_by_employee(employee_id, week_start, week_end)
    return availabilities



@router.put("/{id}", response_model=Availability, status_code=200)
@inject
async def update_availability(
    id:int,
    updated_availability: AvailabilityIn,
    service: IAvailabilityService = Depends(Provide[Container.availability_service]),
) -> dict:
    if existing_availability := await service.get_by_date(date):
        updated_data = Availability(**updated_availability.model_dump())
        updated_availability = await service.update_availability(date, updated_data)
        return updated_availability.model_dump() if updated_availability else {}
    raise HTTPException(status_code=404, detail="Availability not found")


@router.delete("/delete/{id}", status_code=204)
@inject
async def delete_availability(
    id: int,
    service: IAvailabilityService = Depends(Provide[Container.availability_service]),
) -> None:
    if await service.delete_availability(id):
        return
    raise HTTPException(status_code=404, detail="Availability not found")
