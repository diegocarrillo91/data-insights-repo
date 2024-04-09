# %%
# Importar librerías necesarias
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime

# %%
# Crear conexión a la base de datos
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')

# %%
# Solicitar fechas de inicio y fin al usuario
start_date = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
end_date = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

# %%
# Consultar datos de la base de datos
sql = f"""
    SELECT [FECHA], [TOTALNETO]
    FROM [LA_DORADA].[dbo].[FACTURASVENTA]
    WHERE [FECHA] BETWEEN '{start_date}' AND '{end_date}'
"""
df_ventas = pd.read_sql(sql, engine)

# %%
# Convertir la columna de fecha a tipo datetime
df_ventas['FECHA'] = pd.to_datetime(df_ventas['FECHA'])

# %%
# Agrupar ventas por mes
ventas_por_mes = df_ventas.groupby(df_ventas['FECHA'].dt.to_period("M"))['TOTALNETO'].sum()

# %%
# Visualizar tendencia de ventas
plt.figure(figsize=(12, 6))
ventas_por_mes.plot(kind='line', xlabel='Fecha', ylabel='Ventas', title='Tendencias de Ventas a lo largo del Tiempo')
plt.grid(True)
plt.show()

# %%
# Solicitar al usuario ingresar periodos a pronosticar
periodos_a_consultar = int(input("Ingrese el número de periodos a pronosticar: "))

# %%
# Ajustar el modelo SARIMA
order = (1, 1, 1)  # Parámetros ARIMA
seasonal_order = (1, 1, 1, 12)  # Parámetros estacionales
model = SARIMAX(ventas_por_mes, order=order, seasonal_order=seasonal_order)
results = model.fit()

# %%
# Realizar pronóstico
fecha_inicio_prediccion = ventas_por_mes.index[-1].to_timestamp() + pd.DateOffset(months=1)
fecha_fin_prediccion = fecha_inicio_prediccion + pd.DateOffset(months=periodos_a_consultar-1)
rango_fechas_prediccion = pd.date_range(fecha_inicio_prediccion, fecha_fin_prediccion, freq='M')

#%%
# Obtener las predicciones y graficarlas
predicciones = results.get_forecast(steps=periodos_a_consultar).predicted_mean

#%%
# Convertir períodos a enteros para el eje x
x_historico = range(len(ventas_por_mes.index))
x_prediccion = range(len(ventas_por_mes.index), len(ventas_por_mes.index) + periodos_a_consultar)

#%%
# Visualizar pronóstico junto con datos históricos
plt.figure(figsize=(12, 6))
plt.plot(x_historico, ventas_por_mes.values, label='Ventas Históricas')
plt.plot(x_prediccion, predicciones, label='Pronóstico de Ventas')
plt.xlabel('Fecha')
plt.ylabel('Ventas')
plt.title('Pronóstico de Ventas con SARIMA')
plt.legend()
plt.grid(True)


# %%
# Mostrar pronóstico
print("Pronóstico de Ventas:")
print(predicciones)

# %%
