from typing import List
from datetime import date
from app.schemas.ventas_schema import VentasSchema

from app.services.ventas_service import VentasService

class VentasController:


    def get_venta_by_goal(cls, start_date: str, end_date: str, goal: int) -> List[VentasSchema]:
        return VentasService.get_venta_by_goal(start_date, end_date, goal)

    