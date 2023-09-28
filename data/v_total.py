# %% 
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# %% 
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')

# %% 
sql = """
    SELECT [FECHA], [TOTALNETO]
    FROM [LA_DORADA].[dbo].[FACTURASVENTA]
"""

# %% 
df_ventas = pd.read_sql(sql, engine)

# %% 
df_ventas['FECHA'] = pd.to_datetime(df_ventas['FECHA'])

# %% 
ventas_por_mes = df_ventas.groupby(df_ventas['FECHA'].dt.to_period("M"))['TOTALNETO'].sum()

# %% 
plt.figure(figsize=(12, 6))
ventas_por_mes.plot(kind='line', xlabel='Fecha', ylabel='Ventas', title='Tendencias de Ventas a lo largo del Tiempo')
plt.grid(True)
plt.show()

# %%
