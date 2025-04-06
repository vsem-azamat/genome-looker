from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import router as api_router
from backend.pages import router as pages_router
from backend.core.dependencies import mount_static_files

app = FastAPI(
    title="Genome Looker",
    version="0.1.0",
)
app.include_router(api_router)
app.include_router(pages_router)

mount_static_files(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def root():
    return {"message": "Ping world"}
