from enum import Enum
from typing import Optional
from datetime import time, date
from pydantic import BaseModel, ConfigDict


class ShiftType(str, Enum):
    FULL_DAY = "FULL_DAY"
    OFF = "OFF"
    MORNING_SHIFT = "MORNING_SHIFT"
    EVENING_SHIFT = "EVENING_SHIFT"


class ShiftIn(BaseModel):
    shift_type: ShiftType
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class Shift(ShiftIn):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True, extra="ignore")



"""
shift_instance = Shift(
    id=1,
    date=date(2024, 12, 7),
    shift=ShiftType.MORNING_SHIFT,
    start_time=time(8, 0),  # 08:00 AM
    end_time=time(12, 0)    # 12:00 PM
)

print(shift_instance)

"""
"""
class Shift:
    SHIFTS = {
        ShiftType.FULL_DAY: {"start": time(9, 0), "end": time(23, 0)},
        ShiftType.OFF: {"start": None, "end": None},
        ShiftType.MORNING_SHIFT: {"start": time(9, 0), "end": time(17, 0)},
        ShiftType.EVENING_SHIFT: {"start": time(15, 0), "end": time(23, 0)},
    }

    @staticmethod
    def get_shift_times(shift_type: ShiftType):
        return Shift.SHIFTS[shift_type]
"""
