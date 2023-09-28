from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.controllers.ventas_controller import VentasController
from app.schemas.ventas_schema import VentasSchema

router = APIRouter(
    prefix="/ventas",
    tags=["ventas"],
    responses={404: {"description": "Not found"}},
)

ventas_controller = VentasController()

@router.get("/{start_date}/{end_date}/{goal}/", response_model=List[VentasSchema])
async def get_ventas_by_goal(start_date: str, end_date: str, goal: int):
    return ventas_controller.get_venta_by_goal(start_date, end_date, goal)
