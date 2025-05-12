import pandas as pd
import sqlite3

def clean_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    df_Cleaned = df.copy()

    # Imputación de WindGustDir
    df_Cleaned['WindGustDir'] = df_Cleaned['WindGustDir'].fillna(df_Cleaned['WindDir9am'])
    df_Cleaned['WindGustDir'] = df_Cleaned['WindGustDir'].fillna(df_Cleaned['WindDir3pm'])
    moda = df_Cleaned['WindGustDir'].mode()[0]
    df_Cleaned['WindGustDir'] = df_Cleaned['WindGustDir'].fillna(moda)

    # Renombrar variables
    df_Cleaned = df_Cleaned.rename(columns={
        'Location': 'Location_name',
        'WindGustDir': 'WindDir_avg',
        'WindGustSpeed': 'WindSpeed_max',
    })

    # Calcular promedios
    df_Cleaned['WindSpeed_avg'] = df_Cleaned[['WindSpeed9am', 'WindSpeed3pm']].mean(axis=1)
    df_Cleaned['Humidity_avg'] = df_Cleaned[['Humidity9am', 'Humidity3pm']].mean(axis=1)
    df_Cleaned['Pressure_avg'] = df_Cleaned[['Pressure9am', 'Pressure3pm']].mean(axis=1)
    df_Cleaned['Cloud_avg'] = df_Cleaned[['Cloud9am', 'Cloud3pm']].mean(axis=1)
    df_Cleaned['Temp_avg'] = df_Cleaned[['Temp9am', 'Temp3pm']].mean(axis=1)

    # Eliminar columnas originales
    df_Cleaned.drop(
        columns=[
            'WindDir9am', 'WindDir3pm',
            'WindSpeed9am','WindSpeed3pm',
            'Humidity9am', 'Humidity3pm',
            'Pressure9am', 'Pressure3pm',
            'Cloud9am', 'Cloud3pm',
            'Temp9am', 'Temp3pm',
        ],
        inplace=True
    )

    # Reordenar columnas
    nuevo_orden = [
        'Date', 'Year', 'Month', 'Month_Name',
        'Location_encoded','Location_name',
        'MinTemp', 'MaxTemp', 'Temp_avg',
        'Rainfall', 'Evaporation', 'Sunshine',
        'WindDir_avg', 'WindSpeed_max', 'WindSpeed_avg',
        'Humidity_avg', 'Pressure_avg', 'Cloud_avg',
        'RainToday', 'RISK_MM', 'RainTomorrow',
    ]
    df_Cleaned = df_Cleaned[nuevo_orden]

    return df_Cleaned

def save_to_sqlite(df: pd.DataFrame, sqlite_path: str) -> None:
    conn = sqlite3.connect(sqlite_path)
    df.to_sql('weather_data', conn, if_exists='replace', index=False)
    conn.close()