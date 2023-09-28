from typing import List
from datetime import date

from app.db import engine

import pandas as pd
import numpy as np

from app.schemas.ventas_schema import VentasSchema

class VentasService:

    @classmethod
    def get_venta_by_goal(cls, start_date: str, end_date: str, goal: int) -> List[VentasSchema]:
        sql = """
            SELECT [NUMSERIE]
            ,[NUMFACTURA]
            ,[N]
            ,[CODCLIENTE]
            ,[FECHA]
            ,[HORA]
            ,[ENVIOPOR]
            ,[PORTESPAG]
            ,[DTOCOMERCIAL]
            ,[TOTDTOCOMERCIAL]
            ,[DTOPP]
            ,[TOTDTOPP]
            ,[TOTALBRUTO]
            ,[TOTALIMPUESTOS]
            ,[TOTALNETO]
            ,[TOTALCOSTE]
            ,[CODMONEDA]
            ,[FACTORMONEDA]
            ,[IVAINCLUIDO]
            ,[TRASPASADA]
            ,[FECHATRASPASO]
            ,[ENLACE_EJERCICIO]
            ,[ENLACE_EMPRESA]
            ,[ENLACE_USUARIO]
            ,[ENLACE_ASIENTO]
            ,[CODVENDEDOR]
            ,[VIENEDEFO]
            ,[FECHAENTRADA]
            ,[TIPODOC]
            ,[IDESTADO]
            ,[FECHAMODIFICADO]
            ,[Z]
            ,[CAJA]
            ,[TOTALCOSTEIVA]
            ,[ENTREGADO]
            ,[CAMBIO]
            ,[PROPINA]
            ,[CODENVIO]
            ,[TRANSPORTE]
            ,[TOTALCARGOSDTOS]
            ,[NUMROLLO]
            ,[VENDEDORMODIFICADO]
            ,[TOTALRETENCION]
            ,[SUFACTURA]
            ,[ESINVERSION]
            ,[FECHACREACION]
            ,[IDMOTIVODTO]
            ,[NUMIMPRESIONES]
            ,[CLEANCASHCONTROLCODE1]
            ,[CLEANCASHCONTROLCODE2]
            ,[AGRUPACION]
            ,[ESENTREGAACUENTA]
            ,[REGIMFACT]
            ,[MMFIJADO]
            ,[ENVIADOSII]
            ,[ESSERVICIO]
            ,[MODIFIEDTOTALES]
            ,[CAMBIO2]
            ,[FECHAREGISTRO]
            ,[FECHADEVENGO]
            ,[ABONODE_SERIEFISCAL1]
            ,[ABONODE_SERIEFISCAL2]
            ,[ABONODE_NUMEROFISCAL]
            ,[ABONODE_CLEANCASHCONTROLCODE1]
            ,[ABONODE_CLEANCASHCONTROLCODE2]
            ,[TIQUETCONTABILIZADO]
            ,[MOTIVODTOOBSERVACIONES]
            ,[CODVENDEDORXML]
        FROM [LA_DORADA].[dbo].[FACTURASVENTA]
        """

        # Consulta para obtener los datos de vendedores
        sql_vendedores = """
            SELECT [CODVENDEDOR]
            ,[NOMVENDEDOR]
        FROM [LA_DORADA].[dbo].[VENDEDORES]
        """

        df_ventas = pd.read_sql(sql, engine)
        df_vendedores = pd.read_sql(sql_vendedores, engine)

        # Convertir a datetime
        df_ventas['FECHA'] = pd.to_datetime(df_ventas['FECHA'])


        # Filtrar por periodo

        df_filtrado = df_ventas[(df_ventas['FECHA'] >= start_date) & (df_ventas['FECHA'] <= end_date)]
        ventas_por_vendedor = df_filtrado.groupby('CODVENDEDOR')['TOTALNETO'].sum()

        nombres_vendedores = df_vendedores.set_index('CODVENDEDOR').loc[ventas_por_vendedor.index, 'NOMVENDEDOR']
        df_resultado = pd.DataFrame({'NOMBRE_VENDEDOR': nombres_vendedores, 'VENTAS': ventas_por_vendedor, 'CODVENDEDOR': ventas_por_vendedor.index})

        resultados = []
        for index, row in df_resultado.iterrows():
            resultados.append(VentasSchema(
                codvendedor=row['CODVENDEDOR'],
                nombre_vendedor=row['NOMBRE_VENDEDOR'],
                ventas=row['VENTAS']
            ))

        return resultados