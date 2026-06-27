# Context: Agentic World Architecture Specification (general.instructions.md)
"""Source bootstrap and data-reading utilities."""

import csv
import os

from pyspark.sql import DataFrame, SparkSession

from src.schemas.column_schemas import AI_VERSION_get_client_schema, AI_VERSION_get_customer_schema


def AI_VERSION_ensure_source_data_exists(source_dir: str = "source") -> None:
    """Create required source CSVs only when missing."""
    os.makedirs(source_dir, exist_ok=True)

    customer_path = os.path.join(source_dir, "customer.csv")
    client_path = os.path.join(source_dir, "client.csv")

    if not os.path.exists(customer_path):
        with open(customer_path, mode="w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["customer_id", "client_id", "customer_name", "signup_date"])
            writer.writerows(
                [
                    [1001, 501, "Alice Smith", "2026-01-15"],
                    [1002, 501, "Bob Jones", "2026-02-20"],
                    [1003, 502, "Charlie Brown", "2026-03-05"],
                    [1004, 503, "Diana Prince", "2026-04-12"],
                ]
            )

    if not os.path.exists(client_path):
        with open(client_path, mode="w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["client_id", "client_name", "tier", "region"])
            writer.writerows(
                [
                    [501, "Acme Corp", "Enterprise", "EMEA"],
                    [502, "Stark Industries", "Premium", "AMER"],
                    [503, "Wayne Enterprises", "Standard", "APAC"],
                ]
            )


def AI_VERSION_read_customer_data(spark: SparkSession, source_dir: str = "source") -> DataFrame:
    """Read customer source CSV with explicit schema."""
    customer_path = os.path.join(source_dir, "customer.csv")
    return (
        spark.read.option("header", "true")
        .schema(AI_VERSION_get_customer_schema())
        .csv(customer_path)
    )


def AI_VERSION_read_client_data(spark: SparkSession, source_dir: str = "source") -> DataFrame:
    """Read client source CSV with explicit schema."""
    client_path = os.path.join(source_dir, "client.csv")
    return (
        spark.read.option("header", "true")
        .schema(AI_VERSION_get_client_schema())
        .csv(client_path)
    )
