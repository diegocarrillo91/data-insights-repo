# %% 
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# %%
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')

# %%
fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

# %%
fecha_inicio = fecha_inicio.replace("-", "")[:6]
fecha_fin = fecha_fin.replace("-", "")[:6]

# %%
query = f"""
SELECT CODARTICULO, SUM(UNIDADES) as TOTAL_UNIDADES
FROM VENTASACUMULADAS
WHERE ANYOMES >= '{fecha_inicio}' AND ANYOMES <= '{fecha_fin}'
GROUP BY CODARTICULO
ORDER BY TOTAL_UNIDADES DESC
"""
# %%
df_ventas = pd.read_sql(query, engine)

#%%
query_articulos = """
SELECT CODARTICULO, DESCRIPCION
FROM ARTICULOS
"""
df_articulos = pd.read_sql(query_articulos, engine)

# %%
df_ventas = df_ventas.merge(df_articulos, on='CODARTICULO', how='left')

# %%
num_articulos_a_mostrar = 10

# %%
top_articulos = df_ventas.head(num_articulos_a_mostrar)
print(top_articulos)

#%%
plt.figure(figsize=(15, 8))

bar_width = 0.6
plt.bar(np.arange(len(top_articulos['DESCRIPCION'])), top_articulos['TOTAL_UNIDADES'], width=bar_width, color='skyblue')

plt.xlabel('Nombre del Artículo', fontsize=12)
plt.ylabel('Total de Unidades Vendidas', fontsize=12)
plt.title('Top {} Artículos Vendidos en el Período'.format(num_articulos_a_mostrar), fontsize=16)
plt.xticks(np.arange(len(top_articulos['DESCRIPCION'])), top_articulos['DESCRIPCION'], rotation=90, fontsize=10)
plt.yticks(fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, value in enumerate(top_articulos['TOTAL_UNIDADES']):
    plt.text(i, value, str(value), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()

# %%
engine.dispose()