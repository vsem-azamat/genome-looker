from datetime import datetime
from fastapi import (
    APIRouter, 
    Request,
    UploadFile,
    File,
)
from asyncio import to_thread
from fastapi.responses import HTMLResponse

from backend.schemes import DatasetModel
from backend.core.dependencies import TemplatesDependency, GenomeServiceDependency

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index_page(
    request: Request, 
    templates: TemplatesDependency,
    genome_service: GenomeServiceDependency,
    ):
    """
    Main page of the application.
    """
    datasets = genome_service.get_datasets()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "now": datetime.now(),
        "results": [],
        "datasets": [DatasetModel(name=d.name).model_dump() for d in datasets],
    })

@router.post("/jaccards_html", response_class=HTMLResponse)
async def jaccards_html(
    request: Request,
    genome_service: GenomeServiceDependency,
    templates: TemplatesDependency,
    file: UploadFile = File(...),
):
    results = await to_thread(genome_service.calculate_jaccard, file)
    sorted_results = sorted(results, key=lambda x: x.jaccard, reverse=True)
    
    return templates.TemplateResponse(
        "partials/results.html",
        {"request": request, "results": [r.model_dump() for r in sorted_results]}
    )
