from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.controllers.stock_controller import StockController
from app.schemas.stock_schema import StockSchema
from app.services.stock_service import StockService

router = APIRouter(
    prefix="/stock",
    tags=["stock"],
    responses={404:{"description": "Not Found"}}
)

@router.get("/{codBarras}", response_model=List[StockSchema])
async def get_stock(codBarras: str):
    return StockController.get_stock(codBarras)

