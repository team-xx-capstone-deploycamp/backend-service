from fastapi import APIRouter
from app.schemas.hello import HelloResponse
from importlib.metadata import version

router = APIRouter()

@router.get("/ping", tags=["health"])
def ping():
    return {"ping": "pong"}

@router.get("/hello", response_model=HelloResponse, tags=["demo"])
def hello(name: str = "world"):
    return HelloResponse(message=f"Hello, {name}!")

@router.get("/versions", tags=["debug"])
def versions():
    return {
        "sklearn": version("scikit-learn"),
        "numpy": version("numpy"),
        "xgboost": version("xgboost"),
    }
