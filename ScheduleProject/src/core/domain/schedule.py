from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date, time
from enum import Enum

class PositionType(str, Enum):
    BAR = "BAR"
    USHERING = "USHERING"
    GROUPS = "GROUPS"
    DELIVERY = "DELIVERY"


class ScheduleIn(BaseModel):
    date: date
    position_type: PositionType
    start_time: time
    end_time: time
    employee_id: int

class Schedule(ScheduleIn):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True, extra="ignore")