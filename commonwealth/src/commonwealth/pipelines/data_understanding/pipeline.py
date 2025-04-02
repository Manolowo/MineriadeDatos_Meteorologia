from kedro.pipeline import Pipeline, node
from .nodes import (
    grafico_registros_ubicacion,
    grafico_outliers,
    grafico_correlaciones,
    grafico_clima_mensual,
    grafico_actividades_zona,
    guardar_graficos,
)

def data_understanding():
    return Pipeline([
        node(
            func=grafico_registros_ubicacion,
            inputs=["weatherAUS_Cleaned"],
            outputs="registros_ubicacion_grafico",
            name="grafico_registros_ubicacion_node"
        ),
        node(
            func=grafico_outliers,
            inputs=["weatherAUS_Cleaned"],
            outputs="outliers_grafico",
            name="grafico_outliers_node"
        ),
        node(
            func=grafico_correlaciones,
            inputs=["weatherAUS_Cleaned"],
            outputs="correlaciones_grafico",
            name="grafico_correlaciones_node"
        ),
        node(
            func=grafico_clima_mensual,
            inputs=["weatherAUS_Cleaned"],
            outputs="clima_mensual_grafico",
            name="grafico_clima_mensual_node"
        ),
        node(
            func=grafico_actividades_zona,
            inputs=["weatherAUS_Cleaned"],
            outputs="actividades_zona_grafico",
            name="grafico_actividades_zona_node"
        ),
        node(
            func=guardar_graficos,
            inputs=["weatherAUS_Cleaned"],
            outputs="graficos_guardados",
            name="guardar_graficos_node"
        ),
    ])