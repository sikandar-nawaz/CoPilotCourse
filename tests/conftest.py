# Context: Agentic World Architecture Specification (general.instructions.md)
"""Shared test fixtures for local PySpark testing."""

import pytest

from config.spark_config import AI_VERSION_get_local_spark_session


@pytest.fixture(scope="session")
def AI_VERSION_spark_session():
    """Provide one Spark session for all tests."""
    spark = AI_VERSION_get_local_spark_session(app_name="AgenticPipelineTests")
    yield spark
    spark.stop()
