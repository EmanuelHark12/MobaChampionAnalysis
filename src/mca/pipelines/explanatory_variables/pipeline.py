from kedro.pipeline import Pipeline, node, pipeline

from .nodes import values_counts_champion,damage_counts_champion, gold_counts_champion, minion_counts_champion, kda_counts_champion, versus_matchus
def load_data(data):
    """Load data from the catalog and return it as a dictionary."""
    return data

load_data_node = node(
    func=load_data,
    inputs="lol_historic_years",  # Kedro automatically injects the catalog
    outputs="loaded_data",
    name="load_data_node"
)

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
        load_data_node,
        node(
                func=values_counts_champion,
                #inputs="lol_historic_years",
                inputs="loaded_data",
                outputs="championCount",
                name="values_counts_champion",
        ),
        node(
                func=damage_counts_champion,
                #inputs="lol_historic_years",
                inputs="loaded_data",
                outputs="championDamageCount",
                name="damage_counts_champion",
        ),
        node(
                func=gold_counts_champion,
                #inputs="lol_historic_years",
                inputs="loaded_data",
                outputs="championGoldCount",
                name="gold_counts_champion",
        ),
        node(
                func=minion_counts_champion,
                #inputs="lol_historic_years",
                inputs="loaded_data",
                outputs="championMinionCount",
                name="minion_counts_champion",
        ),
        node(
                func=kda_counts_champion,
                #inputs="lol_historic_years",
                inputs="loaded_data",
                outputs="championKdaCount",
                name="kda_counts_champion",
        ),
        node(
            func=versus_matchus,
            inputs="loaded_data",
            outputs="versusScenarios",
            name="versus_scenarios"
        )
        #    node(
        #        func=train_model,
        #        inputs=["X_train", "y_train"],
        #        outputs="regressor",
        #        name="train_model_node",
        #    ),
        #    node(
        #        func=evaluate_model,
        #        inputs=["regressor", "X_test", "y_test"],
        #        outputs=None,
        #        name="evaluate_model_node",
        #    ),
        ]
)

