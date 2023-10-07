from pydantic import BaseModel

class ClienteCompraSchema(BaseModel):
    cedula: str
    nombre: str
    importe_total: float
    ultima_compra: str