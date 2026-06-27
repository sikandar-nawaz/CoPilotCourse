# Agentic Data Pipeline (PySpark)

This project builds an end-to-end local data pipeline with:
- Source bootstrap (create source files only if missing)
- Join logic between customer and client data
- Business transformations
- Curated data load into target locations

## Pipeline Flow

1. Ensure source data exists in `source/`
2. Read source CSVs with explicit schemas
3. Clean and standardize source datasets
4. Join and apply business transformations
5. Write curated outputs to `target/curated/`

## Project Structure

- `main.py`: orchestration entry point
- `config/spark_config.py`: local Spark session setup
- `src/schemas/column_schemas.py`: explicit source schemas
- `src/extract/readers.py`: source generation and readers
- `src/transforms/cleaning.py`: cleaning transformations
- `src/transforms/business_logic.py`: join + business transformations
- `src/load/writers.py`: output writers
- `src/utils/helpers.py`: summary helpers
- `tests/`: pipeline transformation tests

## Setup

From repository root:

```bash
python3 -m venv COPILOTCOURSE_VE_27JUN
source COPILOTCOURSE_VE_27JUN/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

If Java is not installed (required by Spark), install and configure OpenJDK 17.

## Run Pipeline

```bash
python3 main.py
```

Expected behavior:
- If `source/customer.csv` or `source/client.csv` is missing, it will be auto-created.
- Curated outputs will be written to:
  - `target/curated/parquet/` (partitioned by region)
  - `target/curated/csv/` (single coalesced CSV folder)

## Run Tests

```bash
pytest -q
```

## Notes

- Source files are never overwritten once present.
- All pipeline functions follow `AI_VERSION_` prefix naming.
- Schemas are explicit (no inferSchema) for consistent behavior.
