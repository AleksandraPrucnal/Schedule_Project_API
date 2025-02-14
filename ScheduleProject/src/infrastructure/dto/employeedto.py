from typing import Optional
from asyncpg import Record
from pydantic import UUID4, BaseModel, ConfigDict


class EmployeeDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record) -> "EmployeeDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record: The DB record, typically from a query result.

        Returns:
            EmployeeDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            first_name=record_dict.get("first_name"),
            last_name=record_dict.get("last_name"),
            email=record_dict.get("email"),
            phone_number=record_dict.get("phone_number"),
        )
    


class EmployeeStatsDTO(BaseModel):
    total_hours: float
    total_shifts: int
    total_availability_hours: float

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record) -> "EmployeeStatsDTO":
        
        record_dict = dict(record)

        return cls(
            total_hours=record_dict.get("total_hours", 0.0),
            total_shifts=record_dict.get("total_shifts", 0),
            total_availability_hours=record_dict.get("total_availability_hours", 0.0),
        )