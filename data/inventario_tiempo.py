#%%
from sqlalchemy import create_engine, text
import pandas as pd

# %%
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')

# %%

sql_query_inventario = text("""
    SELECT
        Articulos.CODARTICULO AS CODIGO,
        Articulos.REFPROVEEDOR AS REFERENCIA,
        Articulos.DESCRIPCION AS DESCRIPCION,
        Stocks.COLOR AS COLOR,
        Stocks.TALLA AS TALLA,
        Stocks.STOCK AS STOCK
    FROM
        STOCKS
    INNER JOIN
        ARTICULOS ON ARTICULOS.CODARTICULO = STOCKS.CODARTICULO
""")

# %%
df_inventario = pd.read_sql_query(sql_query_inventario, engine)

# %%
print(df_inventario)

# %%
