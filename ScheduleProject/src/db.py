import asyncio

import databases
import sqlalchemy
from sqlalchemy.sql import text
from sqlalchemy import Enum, Table, ForeignKey, Column, Integer, String, Date, Time
from enum import Enum as PyEnum
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.mutable import MutableList
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)
from src.config import config



class PositionType(PyEnum):
    BAR = "BAR"
    USHERING = "USHERING"
    GROUPS = "GROUPS"
    DELIVERY = "DELIVERY"


class ShiftType(PyEnum):
    FULL_DAY = "FULL_DAY"
    OFF = "OFF"
    MORNING_SHIFT = "MORNING_SHIFT"
    EVENING_SHIFT = "EVENING_SHIFT"


metadata = sqlalchemy.MetaData()

shift_table = Table(
    "shifts",
    metadata,
    sqlalchemy.Column("id", Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("shift_type", Enum(ShiftType, name="shift_type_enum"), nullable=False),
    sqlalchemy.Column("start_time", Time, nullable=True),
    sqlalchemy.Column("end_time", Time, nullable=True),
)


employee_table = sqlalchemy.Table(
    "employees",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True,  autoincrement=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),  # unique=True
    sqlalchemy.Column("phone_number", sqlalchemy.String),
)

schedule_table = sqlalchemy.Table(
    "schedule",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("date", sqlalchemy.Date),
    sqlalchemy.Column("position_type", Enum(PositionType, name="position_type_enum"), nullable=False),
    sqlalchemy.Column("start_time", sqlalchemy.Time),
    sqlalchemy.Column("end_time", sqlalchemy.Time),
    sqlalchemy.Column(
        "employee_id",
        sqlalchemy.ForeignKey("employees.id" , ondelete="CASCADE"),
        nullable=False,
    ),
)


availability_table = Table(
    "availabilities",
    metadata,
    sqlalchemy.Column("id", Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column(
        "employee_id",
        ForeignKey("employees.id" , ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "shift_id",
        ForeignKey("shifts.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column("date", Date),
)



db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=True,
)


async def run_sql_file(file_path: str):
    with open(file_path, "r") as file:
        statements = file.read().split(";")
    async with engine.begin() as conn:
        for statement in statements:
            if statement.strip():
                await conn.execute(text(statement.strip()))



async def init_db(retries: int = 5, delay: int = 5) -> None:
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all) 
            await run_sql_file("./src/data.sql")  
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")

