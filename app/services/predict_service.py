import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from skforecast.ForecasterAutoregDirect import ForecasterAutoregDirect

# Conectar a la base de datos
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')

# Función para entrenar el modelo y hacer predicciones
def train_forecaster(ventas, steps):
    forecaster = ForecasterAutoregDirect(
        regressor=RandomForestRegressor(),  
        lags=6,  
        steps=steps 
    )
    forecaster.fit(y=ventas)
    return forecaster

def predict_sales(start_date: str, end_date: str, horizon: int):
    # Consultar datos de la base de datos
    sql = f"""
        SELECT [FECHA], [TOTALNETO]
        FROM [LA_DORADA].[dbo].[FACTURASVENTA]
        WHERE [FECHA] BETWEEN '{start_date}' AND '{end_date}'
    """
    df_ventas = pd.read_sql(sql, engine)
    
    # Preprocesar datos
    df_ventas['FECHA'] = pd.to_datetime(df_ventas['FECHA'])
    ventas_por_mes = df_ventas.groupby(df_ventas['FECHA'].dt.to_period("M"))['TOTALNETO'].sum()
    
    # Obtener los datos de entrenamiento
    train_size = len(ventas_por_mes) - horizon
    train_data = ventas_por_mes[:train_size]
    
    # Entrenar el modelo
    forecaster = train_forecaster(train_data, horizon)
    
    # Realizar predicciones
    periodos_a_consultar = ventas_por_mes.index[-horizon:]
    last_window_series = pd.Series(index=periodos_a_consultar, data=0)
    predictions = forecaster.predict(steps=horizon, last_window=last_window_series)
    
    # Evaluar el desempeño del modelo
    test_data = ventas_por_mes[train_size:]
    mse = mean_squared_error(test_data, predictions)
    mae = mean_absolute_error(test_data, predictions)
    
    return predictions.values.tolist(), mse, mae
