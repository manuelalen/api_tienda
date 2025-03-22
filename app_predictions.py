#scikit-learn pandas matplotlib seaborn

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from datetime import timedelta
import os
from dotenv import load_dotenv

# Cargar variables del entorno
load_dotenv()

# Conexión a MySQL
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")

url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(url)

# Consulta SQL de ingresos por día
query = """
SELECT 
    YEAR(c.fecha_pedido) AS anio,
    DAY(c.fecha_pedido) AS dia,
    SUM(dc.precio * dc.cantidad) AS ingresos
FROM compras c
JOIN detalles_compras dc ON c.id_pedido = dc.id_pedido
GROUP BY anio, dia
ORDER BY anio, dia;
"""

df = pd.read_sql(query, engine)

# Crear columna de fecha real
df["fecha"] = pd.to_datetime(df["anio"].astype(str) + "-01-" + df["dia"].astype(str), errors="coerce")
df = df.dropna(subset=["fecha"]).reset_index(drop=True)
df = df.sort_values("fecha")

# Añadir variable "periodo" como predictor
df["periodo"] = range(len(df))
X = df[["periodo"]]
y = df["ingresos"]

if len(df) < 2:
    print("No hay suficientes datos para entrenar un modelo.")
else:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Modelo
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predicciones para próximos 7 días
    last_period = df["periodo"].max()
    last_date = df["fecha"].max()

    forecast_periods = list(range(last_period + 1, last_period + 8))
    forecast_dates = [last_date + timedelta(days=i) for i in range(1, 8)]
    forecast_preds = model.predict(np.array(forecast_periods).reshape(-1, 1))

    forecast_df = pd.DataFrame({
        "fecha": forecast_dates,
        "periodo": forecast_periods,
        "prediccion_ingresos": forecast_preds
    })

    # Crear carpeta forecast si no existe
    os.makedirs("forecast", exist_ok=True)

    # Guardar CSV
    forecast_df.to_csv("forecast/forecasting.csv", index=False)
    print("✅ Predicciones guardadas en 'forecast/forecasting.csv'")
