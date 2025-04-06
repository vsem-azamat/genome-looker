import os
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

def mount_static_files(app: FastAPI) -> None:
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(backend_dir)  # Adjust path to point to the backend directory
    
    templates_dir = os.path.join(backend_dir, "templates")
    app.mount("/templates", StaticFiles(directory=templates_dir), name="templates")

    static_dir = os.path.join(backend_dir, "static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

def get_templates() -> Jinja2Templates:
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(backend_dir)  # Adjust path to point to the backend directory
    
    templates_dir = os.path.join(backend_dir, "templates")
    return Jinja2Templates(directory=templates_dir)

TemplatesDependency = Annotated[Jinja2Templates, Depends(get_templates)]
