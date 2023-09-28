#%%
from sqlalchemy import create_engine, text
import pandas as pd

# %%
engine = create_engine('mssql+pyodbc://DESKTOP-BSJPEV6\\SQLEXPRESS/LA_DORADA?driver=ODBC+Driver+17+for+SQL+Server')

# %%
cedula = '52205234'

# %%
sql_query = f"SELECT NOMBRECLIENTE FROM clientes WHERE nif20 = '{cedula}' AND DESCATALOGADO <> 'T'"

# %%
df = pd.read_sql_query(sql_query, engine)

print(df)
# %%
