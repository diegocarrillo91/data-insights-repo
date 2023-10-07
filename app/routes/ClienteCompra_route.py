from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.controllers.ClienteCompra_controller import ClienteCompraController
from app.schemas.ClienteCompra_schema import ClienteCompraSchema
from app.services.ClienteCompra_service import ClienteCompraService

router = APIRouter(
    prefix="/clientecompra",
    tags=["clientecompra"],
    responses={404: {"description": "Not Found"}}
)

clientecompra_controller = ClienteCompraController()

@router.get("/", response_model=List[ClienteCompraSchema])
async def get_compras_cliente():
    df = ClienteCompraService.get_compras_cliente()
    clientes = []
    for _, row in df.iterrows():
        cliente = ClienteCompraSchema(
            cedula=row['Cedula'], 
            nombre=row['Nombre'], 
            importe_total=row['ImporteTotal'],  
            ultima_compra=str(row['UltimaCompra']) 
        )
        clientes.append(cliente)
    return clientes