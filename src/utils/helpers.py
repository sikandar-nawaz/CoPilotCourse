# Context: Agentic World Architecture Specification (general.instructions.md)
"""Shared helper utilities for orchestration and reporting."""

from datetime import datetime


def AI_VERSION_build_run_summary(record_count: int, output_paths: dict[str, str]) -> str:
    """Build a concise pipeline run summary message."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    return (
        f"Run completed at {timestamp}. "
        f"Curated rows: {record_count}. "
        f"Parquet: {output_paths['curated_parquet_path']}. "
        f"CSV: {output_paths['curated_csv_path']}."
    )
