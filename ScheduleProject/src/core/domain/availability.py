from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date, time


class AvailabilityIn(BaseModel):
    date: date
    shift_id: int
    employee_id: int


class Availability(AvailabilityIn):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True, extra="ignore")




"""
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date, time
from src.core.domain.shift import ShiftType, Shift  # Import ShiftType i Shift z shift.py


class AvailabilityIn(BaseModel):
    date: date
    shift: ShiftType = ShiftType.FULL_DAY  # Korzystamy z ShiftType zamiast AvailabilityType
    employee_id: int


class Availability(AvailabilityIn):
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")

"""
