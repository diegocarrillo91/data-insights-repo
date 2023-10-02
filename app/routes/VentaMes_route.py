from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.controllers.VentaMes_controller import VentaPorMesController
from app.schemas.VentaMes_schema import VentaPorMesSchema

router = APIRouter(
    prefix= "/ventames",
    tags=["ventames"],
    responses={404:{"description": "Not Found"}}
)

ventames_controller = VentaPorMesController()

@router.get("/{start_date}/{end_date}/", response_model=List[VentaPorMesSchema])
async def get_ventas_por_mes(start_date: str, end_date: str):
    print(f"start_date: {start_date}, end_date: {end_date}")
    return ventames_controller.get_ventas_por_mes(start_date, end_date)
