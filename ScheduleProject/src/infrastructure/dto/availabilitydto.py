from typing import Optional
from asyncpg import Record  # type: ignore
from pydantic import UUID4, BaseModel, ConfigDict
from datetime import date
from src.infrastructure.dto.shiftdto import ShiftDTO

class AvailabilityDTO(BaseModel):
    id: int
    date: date
    shift: ShiftDTO
    employee_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record) -> "AvailabilityDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record: The DB record, typically from a query result.

        Returns:
            EmployeeDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            employee_id=record_dict.get("employee_id"),
            date=record_dict.get("date"),
            shift=ShiftDTO(
                id=record_dict.get("shift_id"),
                shift_type=record_dict.get("shift_type"),
                start_time=record_dict.get("start_time"),
                end_time=record_dict.get("end_time"),
            ),
        )
