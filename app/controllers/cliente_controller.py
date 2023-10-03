from typing import List
from datetime import date

from app.schemas.cliente_schema import ClienteSchema
from app.services.cliente_service import ClienteService

class ClienteController:
    
    def get_cliente(cls, cedula, start_date: str, end_date: str) -> List[ClienteSchema]:
        return ClienteService.get_cliente(cedula, start_date, end_date)