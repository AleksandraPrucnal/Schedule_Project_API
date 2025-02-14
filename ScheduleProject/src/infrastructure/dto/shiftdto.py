from typing import Optional
from asyncpg import Record  # type: ignore
from datetime import time, date
from pydantic import UUID4, BaseModel, ConfigDict
from enum import Enum


class ShiftType(str, Enum):
    FULL_DAY = "FULL_DAY"
    OFF = "OFF"
    MORNING_SHIFT = "MORNING_SHIFT"
    EVENING_SHIFT = "EVENING_SHIFT"



class ShiftDTO(BaseModel):
    id: int
    shift_type: ShiftType
    start_time: time
    end_time: time

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record) -> "ShiftDTO":
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
            shift_type=record_dict.get("shift_type"),
            start_time=record_dict.get("start_time"),
            end_time=record_dict.get("end_time"),
        )