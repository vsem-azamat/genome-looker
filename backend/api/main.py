from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Request,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from backend.schemes.bedtools import JaccardResult
from backend.core.dependencies import GenomeServiceDependency

templates = Jinja2Templates(directory="backend/templates")

router = APIRouter()

@router.post("/jaccards", response_model=List[JaccardResult])
async def jaccards(
    genome_service: GenomeServiceDependency,
    file: UploadFile = File(...),
):
    """
    Calculate Jaccard similarities for the uploaded BED file.
    """
    results = genome_service.calculate_jaccard(file)
    return sorted(results, key=lambda x: x.jaccard, reverse=True)

@router.post("/jaccards_html", response_class=HTMLResponse)
async def jaccards_html(
    request: Request,
    genome_service: GenomeServiceDependency,
    file: UploadFile = File(...),
):
    """
    Calculate Jaccard similarities and return HTML for HTMX.
    """
    results = genome_service.calculate_jaccard(file)
    sorted_results = sorted(results, key=lambda x: x.jaccard, reverse=True)
    return templates.TemplateResponse("partials/results.html", {
        "request": request,
        "results": sorted_results
    })
