import pandas as pd

# Leer todos los archivos parquet en el directorio
df = pd.read_parquet("detalles_compras_delta", engine="pyarrow")
print(df.head())

