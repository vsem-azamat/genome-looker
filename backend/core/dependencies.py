import os
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.core.config import cnfg
from backend.services.genome_service import GenomeService

def mount_static_files(app: FastAPI) -> None:
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(backend_dir)
    
    templates_dir = os.path.join(backend_dir, "templates")
    app.mount("/templates", StaticFiles(directory=templates_dir), name="templates")

    static_dir = os.path.join(backend_dir, "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

def get_templates() -> Jinja2Templates:
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(backend_dir)
    
    templates_dir = os.path.join(backend_dir, "templates")
    return Jinja2Templates(directory=templates_dir)

TemplatesDependency = Annotated[Jinja2Templates, Depends(get_templates)]

def get_genome_service() -> GenomeService:
    datasets_dir = cnfg.DATASETS_DIR
    if not os.path.exists(datasets_dir):
        raise ValueError(f"Dataset directory {datasets_dir} does not exist.")
    if not os.path.isdir(datasets_dir):
        raise ValueError(f"Dataset directory {datasets_dir} is not a directory.")
    
    return GenomeService(datasets_dir=Path(datasets_dir))

GenomeServiceDependency = Annotated[GenomeService, Depends(get_genome_service)]
