# Spaceflights — Taller Kedro de Paula

Proyecto Kedro construido en el Taller 2 (DANE Automatización), siguiendo el
tutorial oficial de spaceflights, para predecir el precio de viajes a la luna
a partir de datos de compañías, naves y reseñas de clientes.

## Requisitos

- Python 3.11+
- Un entorno virtual con las dependencias de `requirements.txt` / `pyproject.toml`

## Cómo correrlo

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
kedro run
```

## Estructura del proyecto

- `conf/` — configuración (Data Catalog, parámetros, credenciales locales)
- `data/` — datos por capas (01_raw a 08_reporting), no versionados en Git
- `src/spaceflights/pipelines/` — pipelines `data_processing` y `data_science`
- `tests/` — pruebas con pytest

## Pipelines

| Pipeline | Qué hace |
|---|---|
| `data_processing` | Limpia companies/shuttles y arma la tabla de entrada al modelo |
| `data_science` | Separa train/test, entrena una regresión lineal y evalúa el modelo |

## Visualización

```powershell
kedro viz run
```

## Tests

```powershell
pytest
```
