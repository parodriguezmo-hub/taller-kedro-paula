"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.7.0
"""
from kedro.pipeline import Pipeline, node, pipeline 
from .nodes import create_model_input_table, preprocess_companies, preprocess_shuttles 
  
def create_pipeline(**kwargs) -> Pipeline: 
    return pipeline([ 
        node(preprocess_companies, "companies", "preprocessed_companies", 
             name="preprocess_companies_node"), 
        node(preprocess_shuttles, "shuttles", "preprocessed_shuttles", 
             name="preprocess_shuttles_node"), 
        node(create_model_input_table, 
             ["preprocessed_shuttles", "preprocessed_companies", "reviews"], 
             "model_input_table", name="create_model_input_table_node"), 
    ]) 