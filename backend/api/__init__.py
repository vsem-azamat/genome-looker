from fastapi import APIRouter
from .dataset import router as dataset_router

router = APIRouter(prefix="/api", tags=["api"])

router.include_router(dataset_router, prefix="/dataset", tags=["dataset"])
