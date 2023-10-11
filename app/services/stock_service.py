from typing import List
from datetime import datetime
from app.db import engine
from sqlalchemy import create_engine, text

import pandas as pd
import numpy as np

from app.schemas.stock_schema import StockSchema

class StockService:
    
    @classmethod
    def get_stock(cls, codBarras: str) -> List[StockSchema]:
        sql_query = text("""
            SELECT
                Articulos.REFPROVEEDOR AS referencia,  -- Alias para que coincida con StockSchema
                Articulos.DESCRIPCION AS descripcion,  -- Alias para que coincida con StockSchema
                Stocks.COLOR AS color,
                Stocks.TALLA AS talla,
                Stocks.STOCK AS stock,
                CASE
                    WHEN GETDATE() BETWEEN desde2 AND HASTA2 THEN PNETO2
                    ELSE PNETO
                END AS valor
            FROM
                STOCKS
            INNER JOIN
                ARTICULOS ON ARTICULOS.CODARTICULO = STOCKS.CODARTICULO
            INNER JOIN
                ARTICULOSLIN ON ARTICULOSLIN.CODARTICULO = ARTICULOS.CODARTICULO
                    AND ARTICULOSLIN.TALLA = STOCKS.TALLA
                    AND ARTICULOSLIN.COLOR = STOCKS.COLOR
            INNER JOIN
                PRECIOSVENTA ON PRECIOSVENTA.CODARTICULO = ARTICULOSLIN.CODARTICULO
                    AND PRECIOSVENTA.TALLA = ARTICULOSLIN.TALLA
                    AND PRECIOSVENTA.COLOR = ARTICULOSLIN.COLOR
            WHERE
                STOCKS.STOCK <> 0
                AND CODBARRAS LIKE :codBarras
        """)
        
        df = pd.read_sql_query(sql_query, engine, params={"codBarras": f"{codBarras}%"})
        
        resultados = df.to_dict(orient="records")

        return [StockSchema(**result) for result in resultados]