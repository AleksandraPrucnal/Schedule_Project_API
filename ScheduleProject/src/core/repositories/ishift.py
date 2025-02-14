from abc import ABC, abstractmethod
from typing import Any, Iterable
from src.core.domain.shift import Shift


class IShiftRepository(ABC):

    @abstractmethod
    async def get_all_shifts(self) -> Iterable[Any]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Any | None:
        pass

    @abstractmethod
    async def add_shift(self, data: Shift) -> Any | None:
        pass

    @abstractmethod
    async def update_shift(self, id: int, data: Shift) -> Any | None:
        pass

    @abstractmethod
    async def delete_shift(self, id: int) -> bool:
        pass