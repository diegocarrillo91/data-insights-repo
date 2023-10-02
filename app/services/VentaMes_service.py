from typing import List
from datetime import datetime
from app.db import engine

import pandas as pd
import numpy as np

from app.schemas.VentaMes_schema import VentaPorMesSchema

class VentaPorMesService:
    
    @classmethod
    def get_ventas_por_mes(cls, start_date: str, end_date: str) -> List[VentaPorMesSchema]:
        sql = f"""
            SELECT [FECHA], [TOTALNETO]
            FROM [LA_DORADA].[dbo].[FACTURASVENTA]
            WHERE [FECHA] BETWEEN '{start_date}' AND '{end_date}'
        """
        
        df_ventas = pd.read_sql(sql, engine)
        
        df_ventas['FECHA'] = pd.to_datetime(df_ventas['FECHA'])
        
        ventas_por_mes = df_ventas.groupby(df_ventas['FECHA'].dt.to_period("M"))['TOTALNETO'].sum()
        
        resultados = []
        
        for index, row in ventas_por_mes.iterrows():
            resultados.append(VentaPorMesSchema(
                fecha=str(row['FECHA']),
                total_neto=float(row['TOTALNETO'])
            ))
            
        return resultados