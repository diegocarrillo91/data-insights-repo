# %%
from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
# %%
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')
# %%
def consultar_clientes_importe_total():
    query = text("""
        SELECT CLIENTES.NIF20 AS Cedula,
               CLIENTES.NOMBRECLIENTE AS Nombre,
               SUM(
                   CASE
                       WHEN DTO <> 0 THEN ROUND(ALBVENTALIN.UNID1 * (PRECIOIVA - (PRECIOIVA * DTO / 100)), 0)
                       ELSE ROUND(ALBVENTALIN.UNID1 * (PRECIOIVA * DTO / 100), 0)
                   END
               ) AS ImporteTotal,
               MAX(ALBVENTACAB.FECHA) AS UltimaCompra
        FROM ALBVENTALIN
        INNER JOIN ALBVENTACAB ON ALBVENTALIN.NUMSERIE = ALBVENTACAB.NUMSERIE AND ALBVENTALIN.NUMALBARAN = ALBVENTACAB.NUMALBARAN
        INNER JOIN CLIENTES ON CLIENTES.CODCLIENTE = ALBVENTACAB.CODCLIENTE
        WHERE CLIENTES.DESCATALOGADO <> 'T'
        GROUP BY CLIENTES.NIF20, CLIENTES.NOMBRECLIENTE
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    return df

# %%
clientes_importe_df = consultar_clientes_importe_total()

# %%
clientes_importe_df = clientes_importe_df.sort_values(by='ImporteTotal', ascending=False)

# %%
pdf_filename = 'informe_clientes.pdf'
doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))

# %%
data = [clientes_importe_df.columns.tolist()] + clientes_importe_df.values.tolist()
# %%
table = Table(data)
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), (0.9, 0.9, 0.9)),
    ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), (0.95, 0.95, 0.95)),
    ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
])

table.setStyle(style)

# %%
elements = []
elements.append(table)

doc.build(elements)

print(f'Informe exportado a {pdf_filename}')
# %%
