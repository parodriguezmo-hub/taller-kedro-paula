import pandas as pd


# ---------- Funciones auxiliares (limpian una columna) ----------

def _is_true(x: pd.Series) -> pd.Series:
    """Convierte 't'/'f' en True/False."""
    return x == "t"


def _parse_percentage(x: pd.Series) -> pd.Series:
    """Convierte '90%' en 0.9."""
    x = x.str.replace("%", "")
    x = x.astype(float) / 100
    return x


def _parse_money(x: pd.Series) -> pd.Series:
    """Convierte '$1,325.00' en 1325.0."""
    x = x.str.replace("$", "").str.replace(",", "")
    x = x.astype(float)
    return x


# ---------- Nodos (los que va a usar el pipeline) ----------

def preprocess_companies(companies: pd.DataFrame) -> pd.DataFrame:
    """Limpia los datos crudos de companies.csv."""
    companies["iata_approved"] = _is_true(companies["iata_approved"])
    companies["company_rating"] = _parse_percentage(companies["company_rating"])
    return companies


def preprocess_shuttles(shuttles: pd.DataFrame) -> pd.DataFrame:
    """Limpia los datos crudos de shuttles.xlsx."""
    shuttles["d_check_complete"] = _is_true(shuttles["d_check_complete"])
    shuttles["moon_clearance_complete"] = _is_true(shuttles["moon_clearance_complete"])
    shuttles["price"] = _parse_money(shuttles["price"])
    return shuttles


def create_model_input_table(
    shuttles: pd.DataFrame, companies: pd.DataFrame, reviews: pd.DataFrame
) -> pd.DataFrame:
    """Combina shuttles, companies y reviews en la tabla que alimenta al modelo."""
    rated_shuttles = shuttles.merge(reviews, left_on="id", right_on="shuttle_id")
    rated_shuttles = rated_shuttles.drop("id", axis=1)
    model_input_table = rated_shuttles.merge(
        companies, left_on="company_id", right_on="id"
    )
    model_input_table = model_input_table.dropna()
    model_input_table["price_per_passenger"] = (
        model_input_table["price"] / model_input_table["passenger_capacity"]
    )
    return model_input_table