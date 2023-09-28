from pydantic import BaseModel

class VentasSchema(BaseModel):
    codvendedor: int
    nombre_vendedor: str
    ventas: float
