import pickle
import pandas as pd
import numpy as np
from flask import render_template, redirect, url_for, request, session
from pathlib import Path
import sqlite3
from commonwealth.src.commonwealth.pipelines.predict_week.utils import predecir_semana_completa

LOCATION_MAP = {
    0: "Adelaide", 1: "Albany", 2: "Albury", 3: "AliceSprings", 4: "BadgerysCreek", 5: "Ballarat",
    6: "Bendigo", 7: "Brisbane", 8: "Cairns", 9: "Canberra", 10: "Cobar", 11: "CoffsHarbour",
    12: "Dartmoor", 13: "Darwin", 14: "GoldCoast", 15: "Hobart", 16: "Katherine", 17: "Launceston",
    18: "Melbourne", 19: "MelbourneAirport", 20: "Mildura", 21: "Moree", 22: "MountGambier",
    23: "MountGinini", 24: "Newcastle", 25: "Nhil", 26: "NorahHead", 27: "NorfolkIsland",
    28: "Nuriootpa", 29: "PearceRAAF", 30: "Penrith", 31: "Perth", 32: "PerthAirport",
    33: "Portland", 34: "Richmond", 35: "Sale", 36: "SalmonGums", 37: "Sydney", 38: "SydneyAirport",
    39: "Townsville", 40: "Tuggeranong", 41: "Uluru", 42: "WaggaWagga", 43: "Walpole",
    44: "Watsonia", 45: "Williamtown", 46: "Witchcliffe", 47: "Wollongong", 48: "Woomera"
}

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
    
    @app.route("/prediction_table")
    def prediction_table():
        base_dir = Path(__file__).resolve().parent.parent.parent / "mineriadedatos_meteorologia"
        db_path = base_dir / "commonwealth" / "data" / "03_primary" / "weatherAUS.sqlite"

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Obtener nombres de tablas que empiezan con "pred_"
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'pred_%';")
        tables = [row[0] for row in cursor.fetchall()]

        all_predictions = {}

        for table_name in tables:
            # Extraer location_name del nombre de la tabla
            location_name = table_name[5:]  # porque "pred_" tiene 5 caracteres

            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            predicciones = {}
            for row in rows:
                fecha = row[0]
                predicciones[fecha] = {
                    "activity_Buceo": bool(row[3]),
                    "activity_Camping": bool(row[4]),
                    "activity_Ciclismo": bool(row[5]),
                    "activity_Kayak": bool(row[6]),
                    "activity_Senderismo": bool(row[7]),
                    "activity_Surf": bool(row[8])
                }
            all_predictions[location_name] = predicciones

        conn.close()

        return render_template("prediction_table.html", all_predictions=all_predictions)

    @app.route("/predict", methods=["POST"])
    def predict():
        if request.method == "POST":
            features_dia = {
                "Temp_avg": float(request.form["Temp_avg"]),
                "WindSpeed_max": float(request.form["WindSpeed_max"]),
                "RainToday": int(request.form["RainToday"]),
                "Rainfall": float(request.form["Rainfall"]),
                "RISK_MM": float(request.form["RISK_MM"]),
                "Humidity_avg": float(request.form["Humidity_avg"]),
            }
            location_id = int(request.form["Location_encoded"])
            
            location_name = LOCATION_MAP.get(location_id, "Desconocido")
            session["location_name"] = location_name
            session["location_id"] = location_id  # ✅ Agrega esta línea

            base_dir = Path(__file__).resolve().parent.parent.parent / "mineriadedatos_meteorologia"

            modelos_path = base_dir / "commonwealth" / "data" / "06_models" / "modelos_entrenados.pkl"
            with open(modelos_path, "rb") as f:
                modelos_entrenados = pickle.load(f)

            df_path = base_dir / "commonwealth" / "data" / "03_primary" / "weatherAUS_primary.csv"
            df = pd.read_csv(df_path)

            predicciones = predecir_semana_completa(features_dia, location_id, df, modelos_entrenados)
            predicciones = convert_numpy_types(predicciones)
            session["predicciones"] = predicciones
            return redirect(url_for("prediction_results"))


    @app.route("/prediction_results")
    def prediction_results():
        location_name = session.get("location_name", "Localidad desconocida")
        predicciones = session.get("predicciones")
        if not predicciones:
            return redirect(url_for("prediction_form"))
        return render_template("prediction_results.html", predicciones=predicciones, location_name=location_name)

    @app.route("/guardar_prediccion", methods=["POST"])
    def guardar_prediccion():
        predicciones = session.get("predicciones")
        location_id = session.get("location_id")
        location_name = session.get("location_name")
        
        print("DEBUG >> session keys:", session.keys())
        print("DEBUG >> predicciones:", predicciones)
        print("DEBUG >> location_id:", location_id)
        print("DEBUG >> location_name:", location_name)

        if not predicciones or location_id is None or not location_name:
            print("No se guardo correctamente")
            return redirect(url_for("prediction_results"))

        table_name = f"pred_{location_name.replace(' ', '').replace('-', '').replace('.', '')}"

        base_dir = Path(__file__).resolve().parent.parent.parent / "mineriadedatos_meteorologia"
        db_path = base_dir / "commonwealth" / "data" / "03_primary" / "weatherAUS.sqlite"

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                fecha TEXT PRIMARY KEY,
                location_id INTEGER,
                location_name TEXT,
                activity_Buceo INTEGER,
                activity_Camping INTEGER,
                activity_Ciclismo INTEGER,
                activity_Kayak INTEGER,
                activity_Senderismo INTEGER,
                activity_Surf INTEGER
            )
        """)

        for fecha, actividades in predicciones.items():
            cursor.execute(f"""
                INSERT OR REPLACE INTO {table_name} (
                    fecha, location_id, location_name, activity_Buceo, activity_Camping,
                    activity_Ciclismo, activity_Kayak, activity_Senderismo, activity_Surf
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fecha,
                location_id,
                location_name,
                actividades.get("activity_Buceo", 0),
                actividades.get("activity_Camping", 0),
                actividades.get("activity_Ciclismo", 0),
                actividades.get("activity_Kayak", 0),
                actividades.get("activity_Senderismo", 0),
                actividades.get("activity_Surf", 0)
            ))

        conn.commit()
        conn.close()
        print("Se llamó a guardar_prediccion")
        return redirect(url_for("prediction_table"))