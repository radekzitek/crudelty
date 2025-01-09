from fastapi import APIRouter
from .endpoints import organization, department, employee, position, team

api_router = APIRouter()

api_router.include_router(
    organization.router,
    prefix="/organizations",
    tags=["organizations"]
)

api_router.include_router(
    department.router,
    prefix="/departments",
    tags=["departments"]
)

api_router.include_router(
    employee.router,
    prefix="/employees",
    tags=["employees"]
)

api_router.include_router(
    position.router,
    prefix="/positions",
    tags=["positions"]
)

api_router.include_router(
    team.router,
    prefix="/teams",
    tags=["teams"]
) 