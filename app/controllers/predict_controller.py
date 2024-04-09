from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.predict_schema import PredictionRequest, PredictionResponse
from app.services.predict_service import predict_sales

router = APIRouter()

# @router.get("/test")
# def test():
#     return {"status": "ok"}

@router.get("/predict/") # response_model=PredictionResponse)
async def predict_sales_endpoint(start_date: str = "", end_date: str = "", horizon: int = 0):
    predictions, mse, mae = predict_sales(start_date, end_date, horizon)
    return {"predictions": predictions, "mse": mse, "mae": mae, "start_date": start_date, "end_date": end_date}