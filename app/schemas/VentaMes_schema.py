from pydantic import BaseModel

class VentaPorMesSchema(BaseModel):
    fecha: str
    total_neto: float