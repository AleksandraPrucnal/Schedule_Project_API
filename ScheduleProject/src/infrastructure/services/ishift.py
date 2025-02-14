from abc import ABC, abstractmethod
from typing import Iterable

from src.core.domain.shift import Shift
from src.infrastructure.dto.shiftdto import ShiftDTO


class IShiftService(ABC):

    @abstractmethod
    async def get_all_shifts(self) -> Iterable[ShiftDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> ShiftDTO | None:
        pass

    @abstractmethod
    async def add_shift(self, data: Shift) -> Shift | None:
        pass

    @abstractmethod
    async def update_shift (self, id: int, data: Shift) -> Shift | None:
        pass

    @abstractmethod
    async def delete_shift(self, id: int) -> bool:
        pass