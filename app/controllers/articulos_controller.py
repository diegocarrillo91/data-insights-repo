from typing import List
from datetime import date
from app.schemas.articulos_schema import ArticulosSchema

from app.services.articulos_service import ArticulosService

class ArticulosController:
    
    def get_articulo(cls, start_date: str, end_date: str) -> List[ArticulosSchema]:
        return ArticulosService.get_articulo(start_date, end_date)
