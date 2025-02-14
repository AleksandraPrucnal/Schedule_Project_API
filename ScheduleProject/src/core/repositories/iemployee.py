from abc import ABC, abstractmethod
from typing import Any, Iterable
from src.core.domain.employee import Employee


class IEmployeeRepository(ABC):

    @abstractmethod
    async def get_all_employees(self) -> Iterable[Any]:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Any | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        pass

    @abstractmethod
    async def get_by_last_name(self, last_name: str) -> Iterable[Any] | None:
        pass

    @abstractmethod
    async def add_employee(self, data: Employee) -> Any | None:
        pass

    @abstractmethod
    async def update_employee(self, id: int, data: Employee) -> Any | None:
        pass

    @abstractmethod
    async def delete_employee(self, id: int) -> bool:
        pass
