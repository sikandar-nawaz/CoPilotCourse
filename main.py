# Context: Agentic World Architecture Specification (general.instructions.md)
"""Orchestration entry point for the end-to-end local data pipeline."""

from config.spark_config import AI_VERSION_get_local_spark_session
from src.extract.readers import (
    AI_VERSION_ensure_source_data_exists,
    AI_VERSION_read_client_data,
    AI_VERSION_read_customer_data,
)
from src.load.writers import AI_VERSION_write_curated_data
from src.transforms.business_logic import AI_VERSION_join_and_transform
from src.transforms.cleaning import AI_VERSION_clean_client_data, AI_VERSION_clean_customer_data
from src.utils.helpers import AI_VERSION_build_run_summary


def AI_VERSION_run_pipeline(source_dir: str = "source", target_dir: str = "target") -> str:
    """Run extract, transform, and load pipeline and return run summary."""
    AI_VERSION_ensure_source_data_exists(source_dir=source_dir)
    spark = AI_VERSION_get_local_spark_session(app_name="AgenticDataPipeline")

    try:
        customer_df = AI_VERSION_read_customer_data(spark=spark, source_dir=source_dir)
        client_df = AI_VERSION_read_client_data(spark=spark, source_dir=source_dir)

        cleaned_customer_df = AI_VERSION_clean_customer_data(customer_df)
        cleaned_client_df = AI_VERSION_clean_client_data(client_df)

        curated_df = AI_VERSION_join_and_transform(cleaned_customer_df, cleaned_client_df)
        output_paths = AI_VERSION_write_curated_data(curated_df, target_dir=target_dir)

        return AI_VERSION_build_run_summary(
            record_count=curated_df.count(),
            output_paths=output_paths,
        )
    finally:
        spark.stop()


if __name__ == "__main__":
    print(AI_VERSION_run_pipeline())
