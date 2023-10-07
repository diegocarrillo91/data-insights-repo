from typing import List
from datetime import date

from app.schemas.ClienteCompra_schema import ClienteCompraSchema
from app.services.ClienteCompra_service import ClienteCompraService

class ClienteCompraController:
    
    def get_compras_cliente() -> List[ClienteCompraSchema]:
        return ClienteCompraService.get_compras_cliente()