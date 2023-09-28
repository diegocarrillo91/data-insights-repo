#%%
from sqlalchemy import create_engine, text
import pandas as pd

# %%
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')

# %%
codBarras = "2852023801403"

# Consulta SQL
sql_query = text("""
    SELECT
        Articulos.REFPROVEEDOR AS REFERENCIA,
        Articulos.DESCRIPCION AS DESCRIPCION,
        Stocks.COLOR AS COLOR,
        Stocks.TALLA AS TALLA,
        Stocks.STOCK AS STOCK,
        CASE
            WHEN GETDATE() BETWEEN desde2 AND HASTA2 THEN PNETO2
            ELSE PNETO
        END AS VALOR
    FROM
        STOCKS
    INNER JOIN
        ARTICULOS ON ARTICULOS.CODARTICULO = STOCKS.CODARTICULO
    INNER JOIN
        ARTICULOSLIN ON ARTICULOSLIN.CODARTICULO = ARTICULOS.CODARTICULO
            AND ARTICULOSLIN.TALLA = STOCKS.TALLA
            AND ARTICULOSLIN.COLOR = STOCKS.COLOR
    INNER JOIN
        PRECIOSVENTA ON PRECIOSVENTA.CODARTICULO = ARTICULOSLIN.CODARTICULO
            AND PRECIOSVENTA.TALLA = ARTICULOSLIN.TALLA
            AND PRECIOSVENTA.COLOR = ARTICULOSLIN.COLOR
    WHERE
        STOCKS.STOCK <> 0
        AND CODBARRAS LIKE :codBarras
""")

# %%

df = pd.read_sql_query(sql_query, engine, params={"codBarras": f"{codBarras}%"})

# %%
print(df)
# %%
