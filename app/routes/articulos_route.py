from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.controllers.articulos_controller import ArticulosController
from app.schemas.articulos_schema import ArticulosSchema

router = APIRouter(
    prefix= "/articulos",
    tags=["articulos"],
    responses={404: {"description": "Not Found"}},
)

articulos_controller = ArticulosController()

@router.get("/{start_date}/{end_date}/", response_model=List[ArticulosSchema])
async def get_articulo(start_date: str, end_date: str):
    return articulos_controller.get_articulo(start_date, end_date)