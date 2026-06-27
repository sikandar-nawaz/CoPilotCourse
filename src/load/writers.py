# Context: Agentic World Architecture Specification (general.instructions.md)
"""Load-layer writers for curated pipeline outputs."""

import os

from pyspark.sql import DataFrame


def AI_VERSION_write_curated_data(df: DataFrame, target_dir: str = "target") -> dict[str, str]:
    """Write curated data to partitioned Parquet and single-folder CSV outputs."""
    curated_parquet_path = os.path.join(target_dir, "curated", "parquet")
    curated_csv_path = os.path.join(target_dir, "curated", "csv")

    (
        df.repartition("region")
        .write.mode("overwrite")
        .partitionBy("region")
        .parquet(curated_parquet_path)
    )
    df.coalesce(1).write.mode("overwrite").option("header", "true").csv(curated_csv_path)

    return {
        "curated_parquet_path": curated_parquet_path,
        "curated_csv_path": curated_csv_path,
    }
