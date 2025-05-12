from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from commonwealth.pipelines.data_cleaning import pipeline as data_cleaning
from commonwealth.pipelines.data_understanding import pipeline as data_understanding
from commonwealth.pipelines.data_preparation import pipeline as data_preparation

def register_pipelines() -> dict[str, Pipeline]:
    return {
        "__default__": Pipeline([]),
        "data_cleaning": data_cleaning.data_cleaning(),
        "data_understanding": data_understanding.data_understanding(),
        "2daFase_CRISP-DM": Pipeline(
                    data_cleaning.data_cleaning().nodes + data_understanding.data_understanding().nodes
                ),
        "data_preparation": data_preparation.data_preparation(),
    }