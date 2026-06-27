# Context: Agentic World Architecture Specification (general.instructions.md)
"""Unit tests for transformation logic using tiny in-memory DataFrames."""

from datetime import date

from src.transforms.business_logic import AI_VERSION_join_and_transform
from src.transforms.cleaning import AI_VERSION_clean_client_data, AI_VERSION_clean_customer_data


def AI_VERSION_test_cleaning_and_join(AI_VERSION_spark_session):
    """Validate cleaning and join outputs for expected rows and fields."""
    raw_customers = [
        (1001, 501, " Alice Smith ", "2026-01-15"),
        (1002, 501, "Bob Jones", "2026-02-20"),
    ]
    raw_clients = [
        (501, "Acme Corp", "enterprise", "emea"),
    ]

    customer_df = AI_VERSION_spark_session.createDataFrame(
        raw_customers,
        ["customer_id", "client_id", "customer_name", "signup_date"],
    )
    client_df = AI_VERSION_spark_session.createDataFrame(
        raw_clients,
        ["client_id", "client_name", "tier", "region"],
    )

    cleaned_customer_df = AI_VERSION_clean_customer_data(customer_df)
    cleaned_client_df = AI_VERSION_clean_client_data(client_df)
    curated_df = AI_VERSION_join_and_transform(cleaned_customer_df, cleaned_client_df)

    assert cleaned_customer_df.count() == 2
    assert cleaned_client_df.count() == 1
    assert curated_df.count() == 2
    assert "tier_rank" in curated_df.columns
    assert "customer_tenure_days" in curated_df.columns

    first_row = curated_df.orderBy("customer_id").first()
    assert first_row.customer_name == "Alice Smith"
    assert first_row.region == "EMEA"
    assert first_row.signup_date == date(2026, 1, 15)
