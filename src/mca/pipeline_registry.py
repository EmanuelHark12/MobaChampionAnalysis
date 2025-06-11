"""Project pipelines."""

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from mca.pipelines.data_processing import create_pipeline
from mca.pipelines.data_processing import pipeline as dp_pipeline
from mca.pipelines.data_science import pipeline as ds_pipeline
from mca.pipelines.explanatory_variables import pipeline as ev_pipeline
#def register_pipelines() -> dict[str, Pipeline]:
#    """Register the project's pipelines.

#    Returns:
#        A mapping from pipeline names to ``Pipeline`` objects.
#    """
#    #return {
    #    "data_processing": create_pipeline(),
    #    # Outros pipelines...
    #}
#    pipelines = find_pipelines()
#    pipelines["__default__"] = sum(pipelines.values())
#    return pipelines
def register_pipelines() -> dict[str, Pipeline]:
    return {
        "__default__": dp_pipeline.create_pipeline(),
        "data_processing": dp_pipeline.create_pipeline(),
        "data_science": ds_pipeline.create_pipeline(),
        "explanatory_variables": ev_pipeline.create_pipeline()
    }