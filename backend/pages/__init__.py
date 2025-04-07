from fastapi import APIRouter
from .index import router as index_router

router = APIRouter(tags=["pages"])

router.include_router(index_router)
