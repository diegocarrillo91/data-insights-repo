from pydantic import BaseModel

class StockSchema(BaseModel):
    referencia: str
    descripcion: str
    color: str
    talla: str
    stock: int
    valor: float