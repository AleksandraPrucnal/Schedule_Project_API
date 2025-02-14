from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse

from datetime import date, time, datetime

from src.api.routers.employee import router as employee_router
from src.api.routers.availability import router as availability_router
from src.api.routers.shift import router as shift_router
from src.api.routers.schedule import router as schedule_router

from src.infrastructure.exceptions.schedule import ScheduleValidationException

from src.container import Container
from src.db import database, init_db
from src.config import config

print("Connecting to database...")
print(f"Host: {config.DB_HOST}")
print(f"Name: {config.DB_NAME}")
print(f"User: {config.DB_USER}")


container = Container()
container.wire(modules=[
    "src.api.routers.employee",
    "src.api.routers.availability",
    "src.api.routers.shift",
    "src.api.routers.schedule"
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(employee_router, prefix="/employee")
app.include_router(availability_router, prefix="/availability")
app.include_router(shift_router, prefix="/shift")
app.include_router(schedule_router, prefix="/schedule")


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:

    return await http_exception_handler(request, exception)


@app.exception_handler(ScheduleValidationException)
async def schedule_validation_error_handler(request: Request, exc: ScheduleValidationException):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )