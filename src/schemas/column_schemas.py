# Context: Agentic World Architecture Specification (general.instructions.md)
"""Explicit schema definitions for all pipeline datasets."""

from pyspark.sql.types import IntegerType, StringType, StructField, StructType


def AI_VERSION_get_customer_schema() -> StructType:
    """Return schema for source/customer.csv."""
    return StructType(
        [
            StructField("customer_id", IntegerType(), False),
            StructField("client_id", IntegerType(), False),
            StructField("customer_name", StringType(), False),
            StructField("signup_date", StringType(), False),
        ]
    )


def AI_VERSION_get_client_schema() -> StructType:
    """Return schema for source/client.csv."""
    return StructType(
        [
            StructField("client_id", IntegerType(), False),
            StructField("client_name", StringType(), False),
            StructField("tier", StringType(), False),
            StructField("region", StringType(), False),
        ]
    )
