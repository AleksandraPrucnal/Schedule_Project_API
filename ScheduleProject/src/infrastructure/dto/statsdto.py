from typing import Optional, Dict
from asyncpg import Record
from datetime import time, date
from pydantic import UUID4, BaseModel, ConfigDict


class StatsDTO(BaseModel):
    total_hours: float
    most_active_day: Optional[date]
    most_active_day_hours : float

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record) -> "StatsDTO":
        
        record_dict = dict(record)

        return cls(
            total_hours=record_dict.get("total_hours", 0.0),
            most_active_day=record_dict.get("most_active_day"),
            most_active_day_hours = record_dict.get("most_active_day_hours", 0.0),
        )