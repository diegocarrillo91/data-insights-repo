# %% 
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# %%
# Create engine for ms sql server

engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')
# engine = create_engine('mssql+pyodbc://@./LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')

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

# %%
df_ventas = pd.read_sql(sql, engine)
df_vendedores = pd.read_sql(sql_vendedores, engine)

# %%
df_ventas['FECHA'] = pd.to_datetime(df_ventas['FECHA'])

# %%
meta = int(input('Ingrese el objetivo de ventas: '))
periodo_inicio = pd.to_datetime(input('Ingrese la fecha de inicio (YYYY-MM-DD): '))
periodo_fin = pd.to_datetime(input('Ingrese la fecha de fin (YYYY-MM-DD): '))

# %%
df_filtrado = df_ventas[(df_ventas['FECHA'] >= periodo_inicio) & (df_ventas['FECHA'] <= periodo_fin)]
ventas_por_vendedor = df_filtrado.groupby('CODVENDEDOR')['TOTALNETO'].sum()
# %%
nombres_vendedores = df_vendedores.set_index('CODVENDEDOR').loc[ventas_por_vendedor.index, 'NOMVENDEDOR']
# %%
df_resultado = pd.DataFrame({'NOMBRE_VENDEDOR': nombres_vendedores, 'VENTAS': ventas_por_vendedor})

df_resultado.head()

#%%
df_resultado.plot(kind='bar', x='NOMBRE_VENDEDOR', y='VENTAS', xlabel='Nombre del Vendedor', ylabel='Ventas', title='Ventas por Vendedor')
plt.axhline(meta, color='r', linestyle='--', label='Meta')

plt.show()
# %%
