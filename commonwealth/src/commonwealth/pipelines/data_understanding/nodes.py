import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
from typing import Dict

def convertir_fecha(df: pd.DataFrame) -> pd.DataFrame:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    return df

def grafico_registros_ubicacion(df: pd.DataFrame) -> plt.Figure:
    plt.figure(figsize=(12, 5))
    df['Location'].value_counts().nlargest(30).plot(kind='bar')
    plt.title("Número de registros por ubicación")
    plt.xlabel("Ubicación")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)
    return plt.gcf()

def grafico_outliers(df: pd.DataFrame) -> plt.Figure:
    variables_numericas = ['Sunshine', 'Evaporation', 'Pressure9am', 'Pressure3pm', 
                           'WindGustSpeed', 'Humidity3pm', 'Temp3pm', 'WindSpeed3pm', 
                           'Humidity9am', 'Rainfall', 'WindSpeed9am', 'Temp9am', 'MinTemp', 'MaxTemp']
    
    plt.figure(figsize=(15, 10))
    for i, columna in enumerate(variables_numericas):
        plt.subplot(3, 5, i + 1)
        sns.boxplot(y=df[columna])
        plt.title(columna)
    plt.tight_layout()
    return plt.gcf()

def grafico_correlaciones(df: pd.DataFrame) -> plt.Figure:
    plt.figure(figsize=(12, 8))
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, cmap="BrBG", annot=True)
    plt.title("Matriz de Correlación")
    return plt.gcf()

def grafico_clima_mensual(df: pd.DataFrame) -> plt.Figure:
    clima_mensual = df.groupby('Month_Name')[['MaxTemp', 'MinTemp', 'Rainfall', 'Humidity3pm', 'WindGustSpeed']].mean().round(2)
    orden_meses = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    clima_mensual = clima_mensual.reindex(orden_meses)

    plt.figure(figsize=(14, 8))
    sns.heatmap(clima_mensual, annot=True, cmap="YlGnBu", fmt=".1f", annot_kws={"size": 12}, linewidths=0.5)
    plt.title("Promedio Climático por Mes")
    plt.ylabel("Mes")
    plt.xlabel("Variable Climática")
    return plt.gcf()

def grafico_actividades_zona(df: pd.DataFrame) -> plt.Figure:
    condiciones = {
        'Surf': (df['WindGustSpeed'] < 35) & (df['RainToday'] == 0) & (df['RISK_MM'].between(0.5, 2.5)),
        'Senderismo': (df['RainToday'] == 0) & (df['WindGustSpeed'] < 45) & (df['MaxTemp'] < 36),
        'Buceo': (df['MaxTemp'].between(21, 31)) & (df['RainToday'] == 'No'),
        'Kayak': (df['WindGustSpeed'] < 30) & (df['Rainfall'] < 6),
        'Ciclismo': (df['RainToday'] == 0) & (df['WindGustSpeed'] < 35),
        'Camping': (df['WindGustSpeed'] < 25) & (df['MaxTemp'].between(12, 28)) & (df['Rainfall'] < 3),
    }

    registros = []
    for actividad, condicion in condiciones.items():
        df_act = df.loc[condicion].copy()
        df_act['Mes'] = df_act['Date'].dt.strftime('%B')
        df_act['Actividad'] = actividad
        registros.append(df_act[['Mes', 'Actividad']])

    conteo = (pd.concat(registros)
              .assign(Mes=lambda d: d['Mes'].astype(pd.CategoricalDtype(categories=[ 
                  'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December'
              ], ordered=True)))
              .groupby(['Actividad', 'Mes'])
              .size()
              .reset_index(name='Dias_Ideales'))

    plt.figure(figsize=(14, 8))
    sns.barplot(data=conteo, x='Mes', y='Dias_Ideales', hue='Actividad')
    plt.title("Días ideales por Actividad y Mes (Registros Históricos)")
    plt.ylabel("Cantidad de días ideales")
    plt.xlabel("Mes")
    plt.xticks(rotation=45)
    plt.legend(title="Actividad", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return plt.gcf()

def generar_todos_los_graficos(df: pd.DataFrame) -> Dict:
    """Genera y guarda todos los gráficos en la carpeta especificada"""

    # Asegúrate de convertir la columna 'Date' antes de crear los gráficos
    df = convertir_fecha(df)

    output_path = "data/08_reporting"
    os.makedirs(output_path, exist_ok=True)

    graficos = {
        "registros_ubicacion": grafico_registros_ubicacion(df),
        "outliers": grafico_outliers(df),
        "correlaciones": grafico_correlaciones(df),
        "clima_mensual": grafico_clima_mensual(df),
        "actividades_zona": grafico_actividades_zona(df),
    }

    for nombre, grafico in graficos.items():
        if isinstance(grafico, plt.Figure):
            grafico.savefig(os.path.join(output_path, f"{nombre}.png"))
        elif isinstance(grafico, plt.Axes):
            grafico.get_figure().savefig(os.path.join(output_path, f"{nombre}.png"))
        else:
            print(f"Warning: {nombre} is not a valid matplotlib object.")
            continue
        plt.close(grafico)

    # Guardar los gráficos como un pickle
    with open(os.path.join(output_path, "data_understanding_report.pkl"), "wb") as f:
        pickle.dump(graficos, f)

    print(f"Gráficos guardados en {output_path}")

    return {"graficos": graficos}
