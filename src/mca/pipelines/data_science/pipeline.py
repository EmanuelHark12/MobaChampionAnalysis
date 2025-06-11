from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model, split_data, train_model,values_counts_damage_type,values_counts_modifier_name,values_counts_attribute_name,values_counts_champion


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
        node(
                func=values_counts_damage_type,
                inputs="HeroInfo_data",
                outputs="damageTypeCount",
                name="values_counts_damage_type",
        ),
        node(
                func=values_counts_modifier_name,
                inputs="HeroInfo_data",
                outputs="modifierNameCount",
                name="values_counts_modifier_name",
        ),
        node(
                func=values_counts_attribute_name,
                inputs="HeroInfo_data",
                outputs="attributeNameCount",
                name="values_counts_attribute_name",
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

