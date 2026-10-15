from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model, split_data, train_model

base_data_science = pipeline([ 
    node(split_data, ["model_input_table", "params:model_options"], 
         ["X_train", "X_test", "y_train", "y_test"], name="split_data_node"), 
    node(train_model, ["X_train", "y_train"], "regressor", 
         name="train_model_node"), 
    node(evaluate_model, ["regressor", "X_test", "y_test"], None, 
         name="evaluate_model_node"), 
]) 
  
def create_pipeline(**kwargs) -> Pipeline: 
    activo = pipeline( 
        base_data_science, namespace="activo", 
        parameters={"params:model_options": "params:model_options_activo"}, 
        inputs={"model_input_table"}, 
    ) 
    candidato = pipeline( 
        base_data_science, namespace="candidato", 
        parameters={"params:model_options": "params:model_options_candidato"}, 
        inputs={"model_input_table"}, 
    ) 
    return activo + candidato 
