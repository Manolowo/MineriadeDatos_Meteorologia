import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Función de transformación de datos
def transformar_datos(df):
    # 1. Transformación de variables categóricas a binarias
    def map_rain(value):
        if pd.isna(value):
            return 0
        elif value == 'Yes':
            return 1
        elif value == 'No':
            return 0
        else:
            return 0

    # Aplicar la función de transformación
    df['RainToday'] = df['RainToday'].apply(map_rain)
    df['RainTomorrow'] = df['RainTomorrow'].apply(map_rain)

    # 2. Convertir 'Date' a datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # 3. Separar la columna 'Date' en tres columnas: Año, Mes, Nombre del Mes
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Month_Name'] = df['Date'].dt.strftime('%B')

    # 4. Convertir localidades a formato numérico con LabelEncoder
    le = LabelEncoder()
    df['Location_encoded'] = le.fit_transform(df['Location'])

    # Retornar el dataframe después de las transformaciones
    return df

# Función de imputación de datos
def imputar_datos(df):
    # 1. Imputación de valores nulos usando interpolación para variables categóricas
    variables_a_imputar = ["Sunshine", "Evaporation", "Cloud3pm", "Cloud9am"]
    df[variables_a_imputar] = df[variables_a_imputar].interpolate(method='linear')

    # 2. Imputación de variables numéricas con la media
    variables_numericas = ['Sunshine', 'Evaporation', 'Pressure9am', 'Pressure3pm', 
                           'WindGustSpeed', 'Humidity3pm', 'Temp3pm', 'WindSpeed3pm', 
                           'Humidity9am', 'Rainfall', 'WindSpeed9am', 'Temp9am', 'MinTemp', 'MaxTemp']

    for columna in variables_numericas:
        media = df[columna].mean()
        df[columna].fillna(media, inplace=True)

    return df