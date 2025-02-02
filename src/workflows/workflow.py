import mlrun
from kfp import dsl


@dsl.pipeline(
    name="Fraud Detection Pipeline",
    description="Detecting fraud from a transactions dataset",
)
def kfpipeline():
    project = mlrun.get_current_project()

    # Train
    train_run = project.run_function(
        function="train",
        name="train",
        handler="train",
        params={},
        outputs=["model_path", "test_data"],
    )

    # Evaluate
    evaluate_run = project.run_function(
        function="evaluate",
        name="evaluate",
        handler="evaluate",
        inputs={"test_set": train_run.outputs["test_data"]},
        params={
            "model_path": train_run.outputs["model_path"],
            "model_name": "xgboost-model",
            # "test_set": train_run.outputs['test_data'],
            "label_column": "transaction_category",
        },
        returns=["classification_report: dataset"],
    )


#     serving_function = project.get_function("serving")

#     with dsl.Condition(serving_function.spec.graph is None) as build_graph:
#     # if serving_function.spec.graph is None:
#         # Set the topology and get the graph object:
#         graph = serving_function.set_topology("flow", engine="async")

#         # Add the steps:
#         graph.to("XGBModelServer",
#                  name="xgboost-model",
#                  model_path=train_run.outputs['model_path'])\
#         .to(handler="postprocess", name="postprocess").respond()

#     # Deploy the serving function:
#     project.deploy_function(serving_function).after(train_run)
