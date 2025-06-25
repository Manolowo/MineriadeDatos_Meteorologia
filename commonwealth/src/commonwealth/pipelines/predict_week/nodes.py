from .utils import predecir_semana_completa

def nodo_predecir_semana(features_dia: dict, location_id: int, modelos_entrenados: dict, df) -> dict:
    return {"predicciones": predecir_semana_completa(features_dia, location_id, df, modelos_entrenados)}