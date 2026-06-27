# GitHub Copilot Project Instructions: Local PySpark & Modular Architecture

This file defines the strict coding standards, architectural patterns, and project rules for this repository. Adhere to these guidelines for every task, code generation, and refactoring effort.

---

## 1. Tech Stack & Environment Settings
- **Language:** Python 3.10+ (type-hinted, PEP 8 compliant)
- **Framework:** Apache Spark (PySpark) 3.x+
- **Execution Mode:** Local mode (`local[*]`)
- **Testing:** pytest with reusable SparkSession fixtures

---

## 2. Directory & Folder Structure
Keep the project highly modular. Separate capabilities, logic, and layers into explicit Python files instead of monolithic scripts.

```text
├── .github/                  # CI/CD workflows
├── config/
│   └── spark_config.py       # Centralized SparkSession builder
├── src/
│   ├── __init__.py
│   ├── schemas/
│   │   └── column_schemas.py # Explicit StructTypes for DataFrames
│   ├── extract/
│   │   └── readers.py        # Local file readers (CSV, Parquet, JSON)
│   ├── transforms/
│   │   ├── cleaning.py       # Deduplication, null handling, casting
│   │   └── business_logic.py # Domain-specific transformations
│   ├── load/
│   │   └── writers.py        # Local file writers & formats
│   └── utils/
│       └── helpers.py        # Shared non-spark helpers, logging
├── tests/
│   ├── conftest.py          # Shared PySpark local session fixture
│   └── test_transforms.py    # Unit tests for transformations
├── copilot-instructions.md   # This rules file
├── requirements.txt          # Python dependencies
└── main.py                   # Orchestration entry point
```

---

## 3. PySpark Coding Style & Best Practices

### 3.1 SparkSession Management
- Never hardcode `.master("local[*]")` inside functional modules.
- Initialize the `SparkSession` once inside `config/spark_config.py`.
- Configure local performance tuning parameters explicitly (e.g., driver memory, shuffle partitions for local compute).

### 3.2 Code Style & Syntax
- **No Loops:** Never use Python loops (`for`, `while`) to iterate over DataFrame rows. Use built-in `pyspark.sql.functions` instead.
- **Explicit Functions over SQL expressions:** Prefer native API methods (e.g., `df.select()`, `df.filter()`) over raw SQL strings (`spark.sql(...)`) unless handling highly complex legacy queries.
- **Column Referencing:** Use the `F.col("column_name")` syntax. Avoid `df.column_name` or `"column_name"` strings to ensure refactoring safety.
- **Alias All Aggregations:** Always provide an explicit `.alias()` when creating or transforming columns.

### 3.3 Memory & Performance Optimization
- **Shuffle Partitions:** Since this runs locally, always scale down shuffle partitions to match local cores. Set `spark.sql.shuffle.partitions` to a low number (e.g., `4` or `8`) to avoid massive overhead.
- **UDF Avoidance:** Avoid Python User Defined Functions (UDFs) at all costs because they serialize data back and forth to the JVM. Use native `pyspark.sql.functions` (aliased as `F`). If a UDF is unavoidable, use **Vectorized/Pandas UDFs** with type hints.
- **Explain Plan:** When executing heavy transformations, use `.explain(True)` during debugging to verify the execution graph.

### 3.4 Data Integrity & Schemas
- Never rely on `inferSchema=True` for production data reads.
- Define data structures explicitly using `StructType` and `StructField` inside `src/schemas/column_schemas.py`.

---

## 4. Modular Implementation Blueprints

When writing or generating new capabilities, mimic the following code structures exactly:

### Centralized Spark Session (`config/spark_config.py`)
```python
from pyspark.sql import SparkSession
import os

def get_local_spark_session(app_name: str = "LocalPySparkApp") -> SparkSession:
    """Builds a performance-optimized local SparkSession."""
    return (SparkSession.builder
            .appName(app_name)
            .master("local[*]")
            .config("spark.driver.memory", "4g")
            .config("spark.sql.shuffle.partitions", os.cpu_count() or "4")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate())
```

### Pure Transformation Function (`src/transforms/business_logic.py`)
```python
from pyspark.sql import DataFrame
import pyspark.sql.functions as F

def calculate_high_value_customer_metrics(df: DataFrame, threshold: float) -> DataFrame:
    """
    Accepts a DataFrame, applies pure PySpark functional changes, and returns a DataFrame.
    Does NOT contain side effects (no read/write operations).
    """
    return (df
            .filter(F.col("total_spend") > threshold)
            .withColumn("is_premium", F.lit(True))
            .groupBy("country")
            .agg(F.sum("total_spend").alias("total_country_revenue"))
            )
```

---

## 5. Development & Verification Rules
- **Type Hinting:** Every function signature must include type hints for parameters and return types (e.g., `def transform(df: DataFrame) -> DataFrame:`).
- **Documentation:** Every module must contain a clean docstring detailing the transformation logic, inputs, and outputs.
- **Testing:** Ensure logic inside `src/transforms/` can be easily isolated and tested by passing mocked DataFrames using small local sets of data.
