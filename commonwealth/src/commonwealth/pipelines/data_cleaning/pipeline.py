from kedro.pipeline import Pipeline, node
from .nodes import transformar_datos, imputar_datos

def data_cleaning():
    return Pipeline(
        [
            node(
                func=transformar_datos, 
                inputs="weatherAUS",
                outputs="datos_transformados",
                name="transformar_datos_node"
            ),
            node(
                func=imputar_datos, 
                inputs="datos_transformados",
                outputs="weatherAUS_Cleaned",
                name="imputar_datos_node"
            )
        ]
    )

