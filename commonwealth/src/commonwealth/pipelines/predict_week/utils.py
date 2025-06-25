from datetime import datetime, timedelta
import pandas as pd

def predecir_semana_completa(features_dia, location_id, df, results):
    # Asegurar columnas auxiliares
    if 'Day' not in df.columns:
        df['Day'] = pd.to_datetime(df['Date']).dt.day
    if 'Month' not in df.columns:
        df['Month'] = pd.to_datetime(df['Date']).dt.month

    predicciones = {}
    hoy = datetime.today().date()
    mes_actual = hoy.month
    dia_actual = hoy.day

    features = list(features_dia.keys()) + ['Month', 'Location_encoded']

    # === Día actual ===
    x_hoy = features_dia.copy()
    x_hoy['Month'] = mes_actual
    x_hoy['Location_encoded'] = location_id
    x_hoy_df = pd.DataFrame([x_hoy])

    pred_hoy = {}
    for actividad, res in results.items():
        modelo = res['model']
        pred_hoy[actividad] = modelo.predict(x_hoy_df)[0]
    
    predicciones[hoy.strftime("%Y-%m-%d")] = pred_hoy

    # === Próximos 6 días ===
    for offset in range(1, 7):
        fecha = hoy + timedelta(days=offset)
        mes = fecha.month
        dia = fecha.day

        df_filtro = df[
            (df['Location_encoded'] == location_id) &
            (df['Month'] == mes) &
            (df['Day'].between(dia - 1, dia + 1))
        ]

        # Si no hay datos específicos, relajar filtro
        if df_filtro.empty:
            df_filtro = df[
                (df['Location_encoded'] == location_id) &
                (df['Month'] == mes)
            ]

        if df_filtro.empty:
            df_filtro = df[df['Location_encoded'] == location_id]

        if df_filtro.empty:
            predicciones[fecha.strftime("%Y-%m-%d")] = {act: 0 for act in results.keys()}
            continue

        # Calcular promedios de los features para ese día
        x_hist = {}
        for f in features:
            if f == 'Month':
                x_hist[f] = mes
            elif f == 'Location_encoded':
                x_hist[f] = location_id
            else:
                x_hist[f] = df_filtro[f].mean()

        x_hist_df = pd.DataFrame([x_hist])

        pred_hist = {}
        for actividad, res in results.items():
            modelo = res['model']
            pred_hist[actividad] = modelo.predict(x_hist_df)[0]
        
        predicciones[fecha.strftime("%Y-%m-%d")] = pred_hist

    return predicciones