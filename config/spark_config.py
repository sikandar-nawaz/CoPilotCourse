# Context: Agentic World Architecture Specification (general.instructions.md)
"""Spark session configuration for local pipeline execution."""

import os

from pyspark.sql import SparkSession


def AI_VERSION_get_local_spark_session(app_name: str = "AgenticDataPipeline") -> SparkSession:
    """Create a performance-tuned local Spark session."""
    shuffle_partitions = str(max(4, (os.cpu_count() or 4)))
    return (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.shuffle.partitions", shuffle_partitions)
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .getOrCreate()
    )
