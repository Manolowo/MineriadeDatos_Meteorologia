from kedro.pipeline import Pipeline, node, pipeline
from .nodes import train_models, save_models

def modeling(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=train_models,
            inputs="weatherAUS_primary",
            outputs="trained_models",
            name="train_models_node"
        ),
        node(
            func=save_models,
            inputs=["trained_models", "params:model_output_path"],
            outputs=None,
            name="save_models_node"
        )
    ])