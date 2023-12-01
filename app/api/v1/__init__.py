from fastapi import APIRouter

from .endpoints import get_co2_emissions

router = APIRouter()

router.include_router(
    get_co2_emissions.router, prefix="/get_co2_emissions", tags=["co2"]
)
