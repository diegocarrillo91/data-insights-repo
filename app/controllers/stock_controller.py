from typing import List
from datetime import date
from app.schemas.stock_schema import StockSchema

from app.services.stock_service import StockService

class StockController:
    
    @classmethod
    def get_stock(cls, codBarras: str) -> List[StockSchema]:
        return StockService.get_stock(codBarras)