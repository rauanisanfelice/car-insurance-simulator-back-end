from fastapi import APIRouter

from app.interface.api.v1.endpoints import (
    insurance,
)

router = APIRouter()
router.include_router(
    router=insurance.router,
    tags=["insurance"],
    prefix="/insurance",
)
