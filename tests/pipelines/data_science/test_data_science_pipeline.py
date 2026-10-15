import logging

import pandas as pd
import pytest
from kedro.io import DataCatalog, MemoryDataset
from kedro.runner import SequentialRunner

from spaceflights.pipelines.data_science.nodes import split_data
from spaceflights.pipelines.data_science.pipeline import base_data_science


# ---------- Datos de prueba (fixtures) ----------

@pytest.fixture
def dummy_data():
    """Una tabla pequeña hecha a mano, con 12 filas."""
    return pd.DataFrame(
        {
            "engines": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
            "crew": [4, 5, 6, 4, 5, 6, 4, 5, 6, 4, 5, 6],
            "passenger_capacity": [5, 6, 7, 5, 6, 7, 5, 6, 7, 5, 6, 7],
            "price": [120, 290, 30, 150, 300, 45, 110, 280, 35, 140, 310, 40],
        }
    )


@pytest.fixture
def dummy_parameters():
    """Parámetros de prueba: 25 % para test → 12 filas = 9 train + 3 test."""
    return {
        "test_size": 0.25,
        "random_state": 3,
        "features": ["engines", "passenger_capacity", "crew"],
    }


# ---------- Tests del 3.2 (un nodo) ----------

def test_split_data(dummy_data, dummy_parameters):
    X_train, X_test, y_train, y_test = split_data(dummy_data, dummy_parameters)
    assert len(X_train) == 9
    assert len(X_test) == 3
    assert len(y_train) == 9
    assert len(y_test) == 3


def test_split_data_missing_price(dummy_data, dummy_parameters):
    dummy_data_missing_price = dummy_data.drop(columns="price")
    with pytest.raises(KeyError) as e_info:
        split_data(dummy_data_missing_price, dummy_parameters)
    assert "price" in str(e_info.value)


# ---------- Test del 3.3 (pipeline completo) ----------

def test_data_science_pipeline(caplog, dummy_data, dummy_parameters):
    caplog.set_level(logging.INFO, logger="kedro")

    pipeline = base_data_science
    catalog = DataCatalog(
        datasets={
            "model_input_table": MemoryDataset(data=dummy_data),
            "params:model_options": MemoryDataset(data=dummy_parameters),
        }
    )

    SequentialRunner().run(pipeline, catalog)

    assert "Pipeline execution completed successfully" in caplog.text