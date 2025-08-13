from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.routes import router as v1_base_router
from app.api.v1.predict import router as v1_predict_router

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz", tags=["health"])
def healthz():
    return {"status": "ok"}

# Versioned APIs
app.include_router(v1_base_router, prefix="/v1")
app.include_router(v1_predict_router, prefix="/v1")
