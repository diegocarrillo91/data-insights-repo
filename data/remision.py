# %%
from sqlalchemy import create_engine, text
import pandas as pd

# %%
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')

# %%
cedula = '52205234'
fecha_desde = '2020-11-27'
fecha_hasta = '2020-12-18'

# %%
consulta_sql = text("""
    SELECT CONVERT(VARCHAR(10), ALBVENTACAB.FECHA, 103) AS FECHA,
           ALBVENTACAB.NUMSERIE AS SERIE,
           ALBVENTACAB.NUMALBARAN AS NUMERO,
           ALBVENTALIN.REFERENCIA AS REFERENCIA,
           ALBVENTALIN.DESCRIPCION AS DESCRIPCION,
           ALBVENTALIN.COLOR AS COLOR,
           ALBVENTALIN.TALLA AS TALLA,
           ALBVENTALIN.UNIDADESTOTAL AS UNIDADES,
           CASE WHEN DTO <> 0 THEN ROUND(ALBVENTALIN.UNID1 * (PRECIOIVA - (PRECIOIVA * DTO / 100)), 0)
                ELSE ROUND(ALBVENTALIN.UNID1 * (PRECIOIVA * DTO / 100), 0) END AS IMPORTE,
           DATEDIFF(day, ALBVENTACAB.FECHA, GETDATE()) AS DIAS
    FROM ALBVENTALIN
    INNER JOIN ALBVENTACAB ON ALBVENTALIN.NUMSERIE = ALBVENTACAB.NUMSERIE
                            AND ALBVENTALIN.NUMALBARAN = ALBVENTACAB.NUMALBARAN
    INNER JOIN CLIENTES ON CLIENTES.CODCLIENTE = ALBVENTACAB.CODCLIENTE
                      AND CLIENTES.NIF20 = :cedula
    WHERE ALBVENTACAB.FECHA BETWEEN :fecha_desde AND :fecha_hasta
    ORDER BY FECHA, NUMLIN
""")

# %%
df = pd.read_sql_query(consulta_sql, engine, params={"cedula": cedula, "fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta})

# %%
print(df)
# %%
