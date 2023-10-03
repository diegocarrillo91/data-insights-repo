from pydantic import BaseModel

class ClienteSchema(BaseModel):
    cliente: int
    total_gastado: float
    numero_compras: int
    promedio_gasto: float
    grupo: str