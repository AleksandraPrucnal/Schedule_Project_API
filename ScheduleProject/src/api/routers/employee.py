from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from datetime import date
#from jose import jwt

#from src.infrastructure.utils import consts
from src.container import Container
from src.core.domain.employee import Employee, EmployeeIn
from src.infrastructure.dto.employeedto import EmployeeDTO, EmployeeStatsDTO
from src.infrastructure.services.iemployee import IEmployeeService

#bearer_scheme = HTTPBearer()

router = APIRouter(tags = ["Employee"])


@router.post("/create", response_model=Employee, status_code=201)
@inject
async def create_employee(
    employee: EmployeeIn,
    service: IEmployeeService = Depends(Provide[Container.employee_service]),
    #credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    extended_employee_data = Employee(
        **employee.model_dump(),
    )
    new_employee = await service.add_employee(extended_employee_data)
    return new_employee.model_dump() if new_employee else {}


@router.get("/all", response_model=Iterable[EmployeeDTO], status_code=200)
@inject
async def get_all_employees(service: IEmployeeService = Depends(Provide[Container.employee_service])) -> Iterable:

    employees = await service.get_all_employees()
    return employees


@router.get("/id/{id}", response_model=EmployeeDTO, status_code=200)
@inject
async def get_by_id(id: int, service: IEmployeeService = Depends(Provide[Container.employee_service])) -> dict | None:

    if employee := await service.get_by_id(id):
        return employee.model_dump()

    raise HTTPException(status_code=404, detail="Employee not found")


@router.get("/email/{email}",response_model=EmployeeDTO,status_code=200)
@inject
async def get_by_email(email: str, service: IEmployeeService = Depends(Provide[Container.employee_service])) -> dict | None:

    if employee := await service.get_by_email(email):
        return employee.model_dump()

    raise HTTPException(status_code=404, detail="Employee not found")



@router.get("/last_name/{last_name}", response_model=Iterable[EmployeeDTO], status_code=200)
@inject
async def get_by_last_name(last_name:str, service: IEmployeeService = Depends(Provide[Container.employee_service])) -> Iterable:

    employees = await service.get_by_last_name(last_name)

    return employees


@router.put("/{id}", response_model=Employee, status_code=201)
@inject
async def update_employee(
    id: int,
    updated_employee: EmployeeIn,
    service: IEmployeeService = Depends(Provide[Container.employee_service]),
    #credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:

    if employee_data := await service.get_by_id(id=id):

        extended_updated_employee = Employee(
            **updated_employee.model_dump(),
        )
        updated_employee_data = await service.update_employee(
            id=id,
            data=extended_updated_employee,
        )
        return updated_employee_data.model_dump() if updated_employee_data \
            else {}

    raise HTTPException(status_code=404, detail="Employee not found")


@router.delete("/{id}", status_code=204)
@inject
async def delete_employee(id: int, service: IEmployeeService = Depends(Provide[Container.employee_service])) -> None:

    if await service.get_by_id(id=id):
        await service.delete_employee(id)
        return

    raise HTTPException(status_code=404, detail="Employee not found")


@router.get("/employee_stats", status_code=200)
@inject
async def get_employee_stats(
    employee_id: int,
    week_start: date,
    week_end: date,
    service: IEmployeeService = Depends(Provide[Container.employee_service]),
) -> EmployeeStatsDTO:
    return await service.get_employee_stats(employee_id, week_start, week_end)