
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def save_data(df, filepath):
    """Save a DataFrame as a CSV file."""

    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    logger.debug(
        "Saved %d rows to %s",
        len(df),
        output_path
    )
    return output_path

def create_cleaning_report(before_df, after_df):
    """Compare a dataset before and after cleaning."""

    return {
        "rows_before": len(before_df),
        "rows_after": len(after_df),
        "rows_removed": len(before_df) - len(after_df),
        "columns_before": len(before_df.columns),
        "columns_after": len(after_df.columns),
        "columns_removed": len(before_df.columns) - len(after_df.columns)
    }