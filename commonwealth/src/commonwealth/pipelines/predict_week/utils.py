from datetime import datetime, timedelta
import pandas as pd

def predecir_semana_completa(features_dia, location_id, df, results):
    # Agregar columnas auxiliares si no existen
    if 'Day' not in df.columns:
        df['Day'] = pd.to_datetime(df['Date']).dt.day
    if 'Month' not in df.columns:
        df['Month'] = pd.to_datetime(df['Date']).dt.month

    predicciones = {}
    hoy = datetime.today().date()
    month_actual = hoy.month

    # Construir input para hoy
    x_hoy = features_dia.copy()
    x_hoy['Month'] = month_actual
    x_hoy['Location_encoded'] = location_id
    x_hoy_df = pd.DataFrame([x_hoy])

    # Predecir hoy
    pred_actividades_hoy = {}
    for actividad, res in results.items():
        modelo = res['model']
        pred = modelo.predict(x_hoy_df)[0]
        pred_actividades_hoy[actividad] = pred
    predicciones[hoy] = pred_actividades_hoy

    # Simular los próximos 6 días con el mismo input de hoy
    for offset in range(1, 7):
        fecha = hoy + timedelta(days=offset)
        predicciones[fecha] = pred_actividades_hoy 

    return predicciones