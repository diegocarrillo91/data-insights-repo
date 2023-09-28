from pydantic import BaseModel

class ArticulosSchema(BaseModel):
    codarticulo : int
    total_unidades : int
    descripcion : str