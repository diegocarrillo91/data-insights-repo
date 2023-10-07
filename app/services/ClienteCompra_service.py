from typing import List
from datetime import datetime
from app.db import engine
from sqlalchemy import create_engine, text

import pandas as pd
import numpy as np

from app.schemas.ClienteCompra_schema import ClienteCompraSchema

class ClienteCompraService:
    
    @classmethod
    def get_compras_cliente(cls):
        query = text("""
            SELECT CLIENTES.NIF20 AS Cedula,
                CLIENTES.NOMBRECLIENTE AS Nombre,
                SUM(
                    CASE
                        WHEN DTO <> 0 THEN ROUND(ALBVENTALIN.UNID1 * (PRECIOIVA - (PRECIOIVA * DTO / 100)), 0)
                        ELSE ROUND(ALBVENTALIN.UNID1 * (PRECIOIVA * DTO / 100), 0)
                    END
                ) AS ImporteTotal,
                MAX(ALBVENTACAB.FECHA) AS UltimaCompra
            FROM ALBVENTALIN
            INNER JOIN ALBVENTACAB ON ALBVENTALIN.NUMSERIE = ALBVENTACAB.NUMSERIE AND ALBVENTALIN.NUMALBARAN = ALBVENTACAB.NUMALBARAN
            INNER JOIN CLIENTES ON CLIENTES.CODCLIENTE = ALBVENTACAB.CODCLIENTE
            WHERE CLIENTES.DESCATALOGADO <> 'T'
            GROUP BY CLIENTES.NIF20, CLIENTES.NOMBRECLIENTE
        """)

        with engine.connect() as connection:
            result = connection.execute(query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            
        df = df.sort_values(by='ImporteTotal', ascending=False)
        return df