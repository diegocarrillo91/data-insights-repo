from typing import List
from datetime import datetime
from sqlalchemy import text
from app.db import engine

import pandas as pd
import numpy as np

from app.schemas.cliente_schema import ClienteSchema

class ClienteService:
    
    @classmethod
    def get_cliente(cls, cedula, start_date: str, end_date: str) -> List[ClienteSchema]:
        query = text("""
            SELECT CONVERT(VARCHAR(10), ALBVENTACAB.FECHA, 103) FECHA,
                ALBVENTACAB.NUMSERIE SERIE,
                ALBVENTACAB.NUMALBARAN FACTURA,
                ALBVENTALIN.REFERENCIA REFERENCIA,
                ALBVENTALIN.DESCRIPCION DESCRIPCION,
                ALBVENTALIN.COLOR COLOR,
                ALBVENTALIN.TALLA TALLA,
                ALBVENTALIN.UNIDADESTOTAL UNIDADES,
                CASE
                    WHEN DTO <> 0 THEN ROUND(ALBVENTALIN.UNID1 * (PRECIOIVA - (PRECIOIVA * DTO / 100)), 0)
                    ELSE ROUND(ALBVENTALIN.UNID1 * (PRECIOIVA * DTO / 100), 0)
                END IMPORTE,
                datediff(day, fecha, GETDATE()) DIAS
            FROM ALBVENTALIN
            INNER JOIN ALBVENTACAB ON ALBVENTALIN.NUMSERIE = ALBVENTACAB.NUMSERIE AND ALBVENTALIN.NUMALBARAN = ALBVENTACAB.NUMALBARAN
            INNER JOIN CLIENTES ON CLIENTES.CODCLIENTE = ALBVENTACAB.CODCLIENTE
            WHERE ALBVENTACAB.FECHA BETWEEN :fecha_desde AND :fecha_hasta
                AND CLIENTES.NIF20 = :Cedula
            ORDER BY FECHA, NUMLIN
        """)
        
        with engine.connect() as connection:
            result = connection.execute(query, {"fecha_desde": start_date, "fecha_hasta": end_date, "Cedula": cedula})
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            
        total_gastado = df['IMPORTE'].sum()
        numero_compras = df['FACTURA'].nunique()
        promedio_gasto = total_gastado / numero_compras

        if total_gastado >= 1000000:
            grupo = "Clientes de gasto alto"
        elif total_gastado >= 500000:
            grupo = "Clientes de gasto medio"
        else:
            grupo = "Clientes de gasto bajo"

        cliente_data = [
            ClienteSchema(
                cliente=cedula,
                total_gastado=total_gastado,
                numero_compras=numero_compras,
                promedio_gasto=promedio_gasto,
                grupo=grupo
            )
        ]

        return cliente_data