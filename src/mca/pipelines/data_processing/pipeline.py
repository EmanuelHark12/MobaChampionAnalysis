from kedro.pipeline import Pipeline, node, pipeline

from .nodes import create_model_input_table, preprocess_companies, preprocess_shuttles, preprocess_heroport_api


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_heroport_api,
                inputs="metadataChampion",
                outputs="HeroInfo_data",
                name="preprocess_heroport_api"
            )
            #node(
            #    func=preprocess_companies,
            #    inputs="companies",
            #    outputs="preprocessed_companies",
            #    name="preprocess_companies_node",
            #),
            #node(
            #    func=preprocess_shuttles,
            #    inputs="shuttles",
            #    outputs="preprocessed_shuttles",
            #    name="preprocess_shuttles_node",
            #),
            #node(
            #    func=create_model_input_table,
            #    inputs=["preprocessed_shuttles", "preprocessed_companies", "reviews"],
            #    outputs="model_input_table",
            #    name="create_model_input_table_node",
            #),
        ]
    )
