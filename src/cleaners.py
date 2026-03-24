from __future__ import annotations
from typing import Any
import pandas as pd

ChangeLog = list[dict[str, Any]]


class MissingValueCleaner:
    def __init__(self, strategy_map: dict[str, str], fill_values: dict[str, Any] | None = None) -> None:
        self.strategy_map = strategy_map
        self.fill_values = fill_values or {}

    def clean(self, df: pd.DataFrame) -> tuple[pd.DataFrame, ChangeLog]:
        raise NotImplementedError("MissingValueCleaner.clean() — implement in Phase 2.")


class DuplicateCleaner:
    def __init__(self, mode: str = "exact", fuzzy_columns: list[str] | None = None,
                 fuzzy_threshold: int = 90, keep: str = "first") -> None:
        self.mode = mode
        self.fuzzy_columns = fuzzy_columns or []
        self.fuzzy_threshold = fuzzy_threshold
        self.keep = keep

    def clean(self, df: pd.DataFrame) -> tuple[pd.DataFrame, ChangeLog]:
        raise NotImplementedError("DuplicateCleaner.clean() — implement in Phase 2.")


class FormatStandardiser:
    def __init__(self, format_config: dict[str, dict[str, Any]]) -> None:
        self.format_config = format_config

    def clean(self, df: pd.DataFrame) -> tuple[pd.DataFrame, ChangeLog]:
        raise NotImplementedError("FormatStandardiser.clean() — implement in Phase 2.")
