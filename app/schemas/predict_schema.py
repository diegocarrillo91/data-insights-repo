from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    start_date: str
    end_date: str
    horizon: int
    
class PredictionResponse(BaseModel):
    predictions: List[float]
    mse: float
    mae: float