from typing import Iterable

from src.core.domain.shift import Shift
from src.core.repositories.ishift import IShiftRepository
from src.infrastructure.dto.shiftdto import  ShiftDTO
from src.infrastructure.services.ishift import IShiftService


class ShiftService(IShiftService):

    _repository: IShiftRepository

    def __init__(self, repository: IShiftRepository) -> None:
        self._repository = repository


    async def get_all_shifts(self) -> Iterable[ShiftDTO]:
        return await self._repository.get_all_shifts()


    async def get_by_id(self, id: int) -> ShiftDTO | None:
        return await self._repository.get_by_id(id)


    async def add_shift(self, data: Shift) -> Shift | None:
        return await self._repository.add_shift(data)


    async def update_shift(self, id: int, data: Shift) -> Shift | None:
        return await self._repository.update_employee(id=id,data=data)


    async def delete_shift(self, id: int) -> bool:
        return await self._repository.delete_shift(id)