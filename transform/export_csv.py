import pandas as pd
from pathlib import Path


def export_csv(df: pd.DataFrame, output_path: Path):
    """
    Export DataFrame to CSV.
    """

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Saved: {output_path.name} ({len(df)} rows)")