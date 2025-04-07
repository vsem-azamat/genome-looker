from fastapi import (
    APIRouter,
    Path,
)
from fastapi.responses import FileResponse

from backend.core.dependencies import GenomeServiceDependency

router = APIRouter()

@router.get("/{dataset}", response_class=FileResponse)
async def download_dataset(
    genome_service: GenomeServiceDependency,
    dataset: str = Path(..., description="The name of the dataset to download"),
    ) -> FileResponse:
    return await genome_service.download_dataset(dataset)
