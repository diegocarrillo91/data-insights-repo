# %%
# Importar librerías necesarias
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from skforecast.datasets import fetch_dataset
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from skforecast.ForecasterAutoregDirect import ForecasterAutoregDirect

#%%
# Configuración de gráficos
plt.style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['font.size'] = 10

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
# Crear el modelo de forecasting
def train_forecaster(ventas, steps):
    forecaster = ForecasterAutoregDirect(
        regressor=RandomForestRegressor(),  # Puedes cambiar el regresor según tus necesidades
        lags=6,  # Número de lags a considerar en el modelo
        steps=steps  # Número de pasos a predecir en el futuro
    )
    
    # Entrenar el modelo
    forecaster.fit(y=ventas)
    
    return forecaster
# %%
# Pedir al usuario el número de meses a predecir
horizon = int(input("Ingrese el número de meses a predecir (3, 6, o 12): "))

# %%
# Obtener los datos de entrenamiento
train_size = len(ventas_por_mes) - horizon
train_data = ventas_por_mes[:train_size]

#%%
# Entrenar el modelo
forecaster = train_forecaster(train_data, horizon)

#%%
# Realizar predicción
periodos_a_consultar = ventas_por_mes.index[-horizon:]
last_window_series = pd.Series(index=periodos_a_consultar, data=0)  # Convertir a Serie de Pandas
predictions = forecaster.predict(steps=horizon, last_window=last_window_series)

#%%
# Crear DataFrame con datos pronosticados
df_predicciones = pd.DataFrame({
    'Fecha': predictions.index.astype(str),
    'Ventas_Predichas': predictions.values
})

# %%
# Visualizar resultados
plt.figure(figsize=(12, 6))
plt.plot(ventas_por_mes.index.astype(str), ventas_por_mes.values, label='Ventas reales', color='blue')
plt.plot(predictions.index.astype(str), predictions, label='Predicciones', color='red')
plt.xlabel('Fecha')
plt.ylabel('Ventas')
plt.title(f'Predicción de Ventas para los próximos {horizon} meses')
plt.legend()
plt.grid(True)
plt.show()

#%%
# Visualizar tabla con datos pronosticados
print("Datos Pronosticados:")
print(df_predicciones)

# %%
# Evaluar el desempeño del modelo
test_data = ventas_por_mes[train_size:]
mse = mean_squared_error(test_data, predictions)
mae = mean_absolute_error(test_data, predictions)

print(f'Mean Squared Error (MSE): {mse}')
print(f'Mean Absolute Error (MAE): {mae}')

# %%
