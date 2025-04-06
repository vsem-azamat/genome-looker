from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["api"])

from .main import router as api_router

router.include_router(api_router)
