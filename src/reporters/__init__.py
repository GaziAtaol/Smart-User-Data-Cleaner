from __future__ import annotations
from pathlib import Path
from typing import Any
import pandas as pd


class ReportGenerator:
    def __init__(self, df_before: pd.DataFrame, df_after: pd.DataFrame,
                 change_logs: list[list[dict[str, Any]]],
                 template_dir: str | Path = "src/reporters/templates/") -> None:
        self.df_before = df_before
        self.df_after = df_after
        self.change_logs = change_logs
        self.template_dir = Path(template_dir)

    def to_html(self, output_path: str | Path) -> Path:
        raise NotImplementedError("ReportGenerator.to_html() — implement in Phase 4.")

    def to_pdf(self, output_path: str | Path) -> Path:
        raise NotImplementedError("ReportGenerator.to_pdf() — implement in Phase 4.")


class DataExporter:
    def __init__(self, df: pd.DataFrame, add_timestamp: bool = True) -> None:
        self.df = df
        self.add_timestamp = add_timestamp

    def to_csv(self, path: str | Path) -> Path:
        raise NotImplementedError("DataExporter.to_csv() — implement in Phase 4.")

    def to_db(self, connection_string: str, table_name: str, if_exists: str = "replace") -> None:
        raise NotImplementedError("DataExporter.to_db() — implement in Phase 4.")
