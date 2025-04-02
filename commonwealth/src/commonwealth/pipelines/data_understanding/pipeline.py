from kedro.pipeline import Pipeline, node
from .nodes import generar_todos_los_graficos

def create_pipeline(pipeline_name="default_pipeline", **kwargs):
    return Pipeline([
        node(
            func=generar_todos_los_graficos,
            inputs=["weatherAUS_Imputado"],
            outputs=None,
            name="generar_graficos_node"
        )
    ])
