# Context: Agentic World Architecture Specification (general.instructions.md)
"""Join and business transformation layer for curated customer output."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def AI_VERSION_join_and_transform(customer_df: DataFrame, client_df: DataFrame) -> DataFrame:
    """Join customer and client data and produce curated business fields."""
    tier_rank = (
        F.when(F.col("tier") == F.lit("Enterprise"), F.lit(3))
        .when(F.col("tier") == F.lit("Premium"), F.lit(2))
        .otherwise(F.lit(1))
    )

    return (
        customer_df.join(client_df, on="client_id", how="left")
        .withColumn("tier_rank", tier_rank.alias("tier_rank"))
        .withColumn(
            "customer_tenure_days",
            F.datediff(F.current_date(), F.col("signup_date")).alias("customer_tenure_days"),
        )
        .withColumn(
            "signup_year_month",
            F.date_format(F.col("signup_date"), "yyyy-MM").alias("signup_year_month"),
        )
        .select(
            F.col("customer_id").alias("customer_id"),
            F.col("client_id").alias("client_id"),
            F.col("customer_name").alias("customer_name"),
            F.col("signup_date").alias("signup_date"),
            F.col("client_name").alias("client_name"),
            F.col("tier").alias("tier"),
            F.col("tier_rank").alias("tier_rank"),
            F.col("region").alias("region"),
            F.col("signup_year_month").alias("signup_year_month"),
            F.col("customer_tenure_days").alias("customer_tenure_days"),
        )
    )
