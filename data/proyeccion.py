# %%
# Importar librerías necesarias
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime

# %%
# Conexión a la base de datos
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')

#%%
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
# Solicitar al usuario ingresar periodos a consultar
periodos_a_consultar = int(input("Ingrese el número de periodos a pronosticar: "))

# %%
# Crear dataframe para pronóstico
ultimo_mes = ventas_por_mes.index[-1].to_timestamp()
fechas_a_pronosticar = pd.date_range(ultimo_mes + pd.DateOffset(months=1), periods=periodos_a_consultar, freq='M')
df_pronostico = pd.DataFrame({'FECHA': fechas_a_pronosticar})

# %%
# Dividir datos en conjunto de entrenamiento y prueba
X = np.array(range(len(ventas_por_mes))).reshape(-1, 1)
y = ventas_por_mes.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# %%
# Entrenar modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# %%
# Realizar pronóstico
df_pronostico['Pronostico'] = model.predict(np.array(range(len(ventas_por_mes), len(ventas_por_mes) + periodos_a_consultar)).reshape(-1, 1))

# %%
# Convertir índices a formato datetime
df_pronostico['FECHA'] = pd.to_datetime(df_pronostico['FECHA'])

# Visualizar pronóstico junto con datos históricos
plt.figure(figsize=(12, 6))
plt.plot(ventas_por_mes.index, ventas_por_mes.values, label='Ventas Históricas')
plt.plot(df_pronostico['FECHA'], df_pronostico['Pronostico'], label='Pronóstico de Ventas')
plt.xlabel('Fecha')
plt.ylabel('Ventas')
plt.title('Pronóstico de Ventas')
plt.legend()
plt.grid(True)
plt.show()


# %%
# Mostrar pronóstico
print("Pronóstico de Ventas:")
print(df_pronostico)
