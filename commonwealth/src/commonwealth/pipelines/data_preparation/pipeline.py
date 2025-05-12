from kedro.pipeline import Pipeline, node, pipeline
from .nodes import clean_weather_data, save_to_sqlite

def data_preparation(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=clean_weather_data,
            inputs=["weatherAUS_Cleaned"],
            outputs="weatherAUS_primary",
            name="clean_weather_data_node"
        ),
        node(
            func=save_to_sqlite,
            inputs=dict(df="weatherAUS_primary", sqlite_path="params:sqlite_output_path"),
            outputs=None,
            name="save_to_sqlite_node"
        ),
    ])