import pandas as pd
import pytest

from spaceflights.pipelines.data_processing.nodes import create_model_input_table


# ---------- Datos de prueba (fixtures) ----------

@pytest.fixture
def dummy_shuttles():
    """Dos naves con precios y capacidades fáciles de dividir."""
    return pd.DataFrame(
        {
            "id": [1, 2],
            "company_id": [10, 20],
            "price": [1000.0, 3000.0],
            "passenger_capacity": [4, 6],
        }
    )


@pytest.fixture
def dummy_reviews():
    """Una reseña para cada nave."""
    return pd.DataFrame(
        {
            "shuttle_id": [1, 2],
            "review_scores_rating": [90.0, 80.0],
        }
    )


@pytest.fixture
def dummy_companies():
    """Una compañía para cada nave."""
    return pd.DataFrame(
        {
            "id": [10, 20],
            "company_rating": [0.9, 0.8],
        }
    )


# ---------- Tests ----------

def test_price_per_passenger_existe(dummy_shuttles, dummy_companies, dummy_reviews):
    resultado = create_model_input_table(dummy_shuttles, dummy_companies, dummy_reviews)
    assert "price_per_passenger" in resultado.columns


def test_price_per_passenger_valor_correcto(dummy_shuttles, dummy_companies, dummy_reviews):
    resultado = create_model_input_table(dummy_shuttles, dummy_companies, dummy_reviews)

    # Nave 1: 1000 / 4 = 250
    nave_1 = resultado.loc[resultado["shuttle_id"] == 1, "price_per_passenger"].iloc[0]
    assert nave_1 == pytest.approx(250.0)

    # Nave 2: 3000 / 6 = 500
    nave_2 = resultado.loc[resultado["shuttle_id"] == 2, "price_per_passenger"].iloc[0]
    assert nave_2 == pytest.approx(500.0)


def test_no_se_pierden_filas(dummy_shuttles, dummy_companies, dummy_reviews):
    resultado = create_model_input_table(dummy_shuttles, dummy_companies, dummy_reviews)
    assert len(resultado) == 2