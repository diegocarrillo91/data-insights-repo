from typing import List
from datetime import datetime
from app.db import engine

import pandas as pd
import numpy as np

from app.schemas.articulos_schema import ArticulosSchema

class ArticulosService:
    
    @classmethod
    def get_articulo(cls, start_date: str, end_date: str) -> List[ArticulosSchema]:
        
        # Ingresar fechas
        start_date = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
        end_date = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
        
        start_date = start_date.replace("-", "")[:6]
        end_date = end_date.replace("-", "")[:6]
        
        query = f"""
            SELECT CODARTICULO, SUM(UNIDADES) as TOTAL_UNIDADES
            FROM VENTASACUMULADAS
            WHERE ANYOMES >= '{start_date}' AND ANYOMES <= '{end_date}'
            GROUP BY CODARTICULO
            ORDER BY TOTAL_UNIDADES DESC
        """
        
        df_ventas = pd.read_sql(query, engine)
        
        query_articulos = """
                        SELECT CODARTICULO, DESCRIPCION
                        FROM ARTICULOS
                    """
        df_articulos = pd.read_sql(query_articulos, engine)
        
        df_ventas = df_ventas.merge(df_articulos, on='CODARTICULO', how='left')
        
        num_articulos_a_mostrar = 10
        
        top_articulos = df_ventas.head(num_articulos_a_mostrar)
        print(top_articulos)
        
        resultados = []
        for index, row in top_articulos.iterrows():
            resultados.append(ArticulosSchema(
                codarticulo = row['CODARTICULO'],
                total_unidades = row['TOTAL_UNIDADES'],
                descripcion = row['DESCRIPCION']
            ))
            
        return resultados