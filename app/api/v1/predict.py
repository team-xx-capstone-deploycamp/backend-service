from fastapi import APIRouter, Depends, HTTPException
from app.schemas.predict import PredictRequest, PredictResponse
from app.deps.auth import verify_basic_auth
from app.services import model as model_service

router = APIRouter(tags=["predict"])

@router.post("/predict", response_model=PredictResponse, dependencies=[Depends(verify_basic_auth)])
def predict(req: PredictRequest):
    try:
        if req.record is not None:
            pred = model_service.predict(record=req.record.model_dump(exclude_none=True))
        else:
            pred = model_service.predict(features=req.features, record=None)
        return PredictResponse(prediction=pred)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")
