import json
from fastapi import (
    APIRouter,
    UploadFile,
    Response,
    status,
    Path,
    File,
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

@router.post("/")
async def upload_dataset(
    genome_service: GenomeServiceDependency,
    file: UploadFile = File(...),
):
    await genome_service.upload_dataset(file)
    return Response(
        status_code=status.HTTP_201_CREATED,
        content=json.dumps({"message": "Dataset uploaded successfully."}),
        media_type="application/json"
    )

@router.delete("/{dataset}")
async def delete_dataset(
    genome_service: GenomeServiceDependency,
    dataset: str = Path(..., description="The name of the dataset to delete"),
):
    genome_service.delete_dataset(dataset)
    return Response(
        status_code=status.HTTP_200_OK,
        content=json.dumps({"message": "Dataset deleted successfully."}),
        media_type="application/json"
    )
