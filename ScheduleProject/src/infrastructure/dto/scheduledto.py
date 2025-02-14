from typing import Optional
from asyncpg import Record
from datetime import time, date
from pydantic import UUID4, BaseModel, ConfigDict


class ScheduleDTO(BaseModel):
    id: int
    date: date
    position_type: str
    start_time: time
    end_time: time
    employee_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record) -> "ScheduleDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record: The DB record, typically from a query result.

        Returns:
            EmployeeDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            date=record_dict.get("date"),
            position_type=record_dict.get("position_type"),
            start_time=record_dict.get("start_time"),
            end_time=record_dict.get("end_time"),
            employee_id=record_dict.get("employee_id"),
        )