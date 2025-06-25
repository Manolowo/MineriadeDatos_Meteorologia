import pickle
import pandas as pd
import numpy as np
from flask import render_template, redirect, url_for, request, session
from pathlib import Path
from commonwealth.src.commonwealth.pipelines.predict_week.utils import predecir_semana_completa

def register_routes(app):

    def convert_numpy_types(obj):
        if isinstance(obj, dict):
            return {k: convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_numpy_types(i) for i in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        else:
            return obj

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/prediction_form")
    def prediction_form():
        return render_template("prediction_form.html")

    @app.route("/predict", methods=["POST"])
    def predict():
        if request.method == "POST":
            # Recoger los datos del formulario
            features_dia = {
                "Temp_avg": float(request.form["Temp_avg"]),
                "WindSpeed_max": float(request.form["WindSpeed_max"]),
                "RainToday": int(request.form["RainToday"]),
                "Rainfall": float(request.form["Rainfall"]),
                "RISK_MM": float(request.form["RISK_MM"]),
                "Humidity_avg": float(request.form["Humidity_avg"]),
            }
            location_id = int(request.form["Location_encoded"])

            # Definir base del proyecto con ruta absoluta
            base_dir = Path(__file__).resolve().parent.parent.parent / "mineriadedatos_meteorologia"

            # Cargar modelo entrenado y CSV con rutas absolutas
            modelos_path = base_dir / "commonwealth" / "data" / "06_models" / "modelos_entrenados.pkl"
            with open(modelos_path, "rb") as f:
                modelos_entrenados = pickle.load(f)

            df_path = base_dir / "commonwealth" / "data" / "03_primary" / "weatherAUS_primary.csv"
            df = pd.read_csv(df_path)

            predicciones = predecir_semana_completa(features_dia, location_id, df, modelos_entrenados)

            # Convertir numpy types a tipos nativos para poder guardarlo en session
            predicciones = convert_numpy_types(predicciones)

            session["predicciones"] = predicciones
            return redirect(url_for("prediction_results"))

    @app.route("/prediction_results")
    def prediction_results():
        predicciones = session.get("predicciones")
        if not predicciones:
            return redirect(url_for("prediction_form"))
        return render_template("prediction_results.html", predicciones=predicciones)
