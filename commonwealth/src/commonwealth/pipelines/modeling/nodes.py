import pandas as pd
import pickle
from typing import Dict, Any
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def train_models(df: pd.DataFrame) -> Dict[str, Any]:
    features = [
        'Temp_avg', 'WindSpeed_max', 'RainToday', 
        'Rainfall', 'RISK_MM', 'Humidity_avg',
        'Month', 'Location_encoded'
    ]

    activities = [
        'activity_Surf', 'activity_Senderismo', 'activity_Buceo',
        'activity_Kayak', 'activity_Ciclismo', 'activity_Camping'
    ]

    available_features = [f for f in features if f in df.columns]
    available_activities = [a for a in activities if a in df.columns]

    if not available_features or not available_activities:
        raise ValueError("Features o actividades no disponibles en el DataFrame.")

    X = df[available_features]
    results = {}

    for activity in available_activities:
        y = df[activity]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)

        results[activity] = {
            "model": model,
            "accuracy": accuracy,
            "classification_report": report
        }

    return results

def save_models(models: Dict[str, Any], output_path: str):
    with open(output_path, "wb") as f:
        pickle.dump(models, f)