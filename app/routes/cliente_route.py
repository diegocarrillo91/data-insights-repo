from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.controllers.cliente_controller import ClienteController
from app.schemas.cliente_schema import ClienteSchema

router = APIRouter(
    prefix= "/cliente",
    tags=["cliente"],
    responses={404: {"description": "Not Found"}},
)

cliente_controller = ClienteController()

@router.get("/{cedula}/{start_date}/{end_date}/", response_model=List[ClienteSchema])
async def get_cliente_route(cedula: str, start_date: str, end_date: str):
    try:
        result = cliente_controller.get_cliente(cedula, start_date, end_date)
        return result
    except HTTPException as e:
        raise e
