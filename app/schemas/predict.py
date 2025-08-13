from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class PredictRecord(BaseModel):
    car_ID: Optional[int] = None
    symboling: Optional[int] = None
    CarName: Optional[str] = None
    fueltype: Optional[str] = None
    aspiration: Optional[str] = None
    doornumber: Optional[str] = None
    carbody: Optional[str] = None
    drivewheel: Optional[str] = None
    enginelocation: Optional[str] = None
    wheelbase: Optional[float] = None
    carlength: Optional[float] = None
    carwidth: Optional[float] = None
    carheight: Optional[float] = None
    curbweight: Optional[int] = None
    enginetype: Optional[str] = None
    cylindernumber: Optional[str] = None
    enginesize: Optional[int] = None
    fuelsystem: Optional[str] = None
    boreratio: Optional[float] = None
    stroke: Optional[float] = None
    compressionratio: Optional[float] = None
    horsepower: Optional[int] = None
    peakrpm: Optional[int] = None
    citympg: Optional[int] = None
    highwaympg: Optional[int] = None

class PredictRequest(BaseModel):
    features: Optional[List[float]] = Field(default=None, description="25-length feature vector")
    record: Optional[PredictRecord] = Field(default=None, description="Partial or full feature object")
    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {"record": {"CarName": "toyota corolla", "enginesize": 130, "horsepower": 100, "citympg": 28}},
            {"features": [0,0,"toyota corolla","gas","std","four","sedan","fwd","front",96.5,175.4,65.2,54.1,2330,"ohc","four",130,"mpfi",3.47,2.68,9.0,100,5500,28,34]}
        ]
    })

class PredictResponse(BaseModel):
    prediction: List[float]
    model_config = ConfigDict(json_schema_extra={"examples": [{"prediction": [12345.67]}]})
