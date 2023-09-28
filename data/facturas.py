#%%
from sqlalchemy import create_engine, text
import pandas as pd

# %%
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')
# %%
def consulta_facturas(Cedula, fecha_desde, fecha_hasta):
    query = text("""
        SELECT CONVERT(VARCHAR(10), ALBVENTACAB.FECHA, 103) FECHA,
               ALBVENTACAB.NUMSERIE SERIE,
               ALBVENTACAB.NUMALBARAN FACTURA,
               ALBVENTALIN.REFERENCIA REFERENCIA,
               ALBVENTALIN.DESCRIPCION DESCRIPCION,
               ALBVENTALIN.COLOR COLOR,
               ALBVENTALIN.TALLA TALLA,
               ALBVENTALIN.UNIDADESTOTAL UNIDADES,
               CASE
                   WHEN DTO <> 0 THEN ROUND(ALBVENTALIN.UNID1 * (PRECIOIVA - (PRECIOIVA * DTO / 100)), 0)
                   ELSE ROUND(ALBVENTALIN.UNID1 * (PRECIOIVA * DTO / 100), 0)
               END IMPORTE,
               datediff(day, fecha, GETDATE()) DIAS
        FROM ALBVENTALIN
        INNER JOIN ALBVENTACAB ON ALBVENTALIN.NUMSERIE = ALBVENTACAB.NUMSERIE AND ALBVENTALIN.NUMALBARAN = ALBVENTACAB.NUMALBARAN
        INNER JOIN CLIENTES ON CLIENTES.CODCLIENTE = ALBVENTACAB.CODCLIENTE
        WHERE ALBVENTACAB.FECHA BETWEEN :fecha_desde AND :fecha_hasta
              AND CLIENTES.NIF20 = :Cedula
        ORDER BY FECHA, NUMLIN
    """)

    with engine.connect() as connection:
        result = connection.execute(query, {"fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta, "Cedula": Cedula})
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    return df

# %%
Cedula = '52205234'
fecha_desde = '2020-11-27'
fecha_hasta = '2020-12-18'

facturas_df = consulta_facturas(Cedula, fecha_desde, fecha_hasta)
print(facturas_df)
# %%
