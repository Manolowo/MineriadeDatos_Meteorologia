from kedro.pipeline import Pipeline, node, pipeline
from .nodes import nodo_predecir_semana

def predict_week(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=nodo_predecir_semana,
            inputs=["features_dia", "location_id", "modelos_entrenados", "weatherAUS_primary"],
            outputs="predicciones_dict",
            name="nodo_predecir_semana"
        )
    ])
