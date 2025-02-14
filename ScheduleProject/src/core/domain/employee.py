from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, UUID4

class EmployeeIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str

class Employee(EmployeeIn):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True, extra="ignore")