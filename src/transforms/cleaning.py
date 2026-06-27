# Context: Agentic World Architecture Specification (general.instructions.md)
"""Data cleaning transformations for source datasets."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def AI_VERSION_clean_customer_data(df: DataFrame) -> DataFrame:
    """Trim text fields, cast signup date, and remove duplicates."""
    return (
        df.select(
            F.col("customer_id").alias("customer_id"),
            F.col("client_id").alias("client_id"),
            F.trim(F.col("customer_name")).alias("customer_name"),
            F.to_date(F.col("signup_date"), "yyyy-MM-dd").alias("signup_date"),
        )
        .dropna(subset=["customer_id", "client_id", "customer_name", "signup_date"])
        .dropDuplicates(["customer_id"])
    )


def AI_VERSION_clean_client_data(df: DataFrame) -> DataFrame:
    """Normalize text fields and remove duplicate client keys."""
    return (
        df.select(
            F.col("client_id").alias("client_id"),
            F.trim(F.col("client_name")).alias("client_name"),
            F.initcap(F.trim(F.col("tier"))).alias("tier"),
            F.upper(F.trim(F.col("region"))).alias("region"),
        )
        .dropna(subset=["client_id", "client_name", "tier", "region"])
        .dropDuplicates(["client_id"])
    )
