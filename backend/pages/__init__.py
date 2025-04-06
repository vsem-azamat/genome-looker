from fastapi import APIRouter

router = APIRouter(tags=["pages"])

from .index import router as index_router

router.include_router(index_router)
