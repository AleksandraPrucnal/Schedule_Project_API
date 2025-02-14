from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.core.domain.shift import Shift, ShiftIn
from src.infrastructure.dto.shiftdto import ShiftDTO
from src.infrastructure.services.ishift import IShiftService

router = APIRouter(tags = ["Shift"])


@router.post("/create", response_model=Shift, status_code=201)
@inject
async def create_shift(
    shift: ShiftIn,
    service: IShiftService = Depends(Provide[Container.shift_service]),
) -> dict:
    new_shift = await service.add_shift(shift)
    return new_shift.model_dump() if new_shift else {}


@router.get("/all", response_model=Iterable[ShiftDTO], status_code=200)
@inject
async def get_all_shifts(service: IShiftService = Depends(Provide[Container.shift_service])) -> Iterable:
    shifts = await service.get_all_shifts()
    return shifts


@router.get("/id/{id}", response_model=ShiftDTO, status_code=200)
@inject
async def get_shift_by_id(id: int, service: IShiftService = Depends(Provide[Container.shift_service])) -> dict | None:
    if shift := await service.get_by_id(id):
        return shift.model_dump()
    raise HTTPException(status_code=404, detail="Shift not found")


@router.put("/{id}", response_model=Shift, status_code=201)
@inject
async def update_shift(
    id: int,
    updated_shift: ShiftIn,
    service: IShiftService = Depends(Provide[Container.shift_service]),
) -> dict:
    if shift_data := await service.get_by_id(id=id):
        updated_shift_data = await service.update_shift(id=id, data=updated_shift)
        return updated_shift_data.model_dump() if updated_shift_data else {}
    raise HTTPException(status_code=404, detail="Shift not found")


@router.delete("/{id}", status_code=204)
@inject
async def delete_shift(id: int, service: IShiftService = Depends(Provide[Container.shift_service])) -> None:
    if await service.get_by_id(id=id):
        await service.delete_shift(id)
        return
    raise HTTPException(status_code=404, detail="Shift not found")
