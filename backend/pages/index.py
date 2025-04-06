from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from backend.core.dependencies import TemplatesDependency

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request, templates: TemplatesDependency):
    """
    Main page of the application.
    """
    return templates.TemplateResponse("index.html", {
        "request": request,
        "now": datetime.now(),
        "results": []
    })
