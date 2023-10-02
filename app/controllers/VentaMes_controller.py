from typing import List
from datetime import date

from app.schemas.VentaMes_schema import VentaPorMesSchema

from app.services.VentaMes_service import VentaPorMesService

class VentaPorMesController:
    
    def get_ventas_por_mes(cls, start_date: str, end_date: str) -> List[VentaPorMesSchema]:
        return VentaPorMesService.get_ventas_por_mes(start_date, end_date)