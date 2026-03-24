from __future__ import annotations
import re
from typing import Any
import pandas as pd
from dateutil import parser as dateutil_parser

ChangeLog = list[dict[str, Any]]

_VALID_MISSING_STRATEGIES = {"drop_row", "fill_mean", "fill_median", "fill_mode", "fill_const"}


class MissingValueCleaner:
    def __init__(self, strategy_map: dict[str, str], fill_values: dict[str, Any] | None = None) -> None:
        self.strategy_map = strategy_map
        self.fill_values = fill_values or {}

    def clean(self, df: pd.DataFrame) -> tuple[pd.DataFrame, ChangeLog]:
        for col, strategy in self.strategy_map.items():
            if strategy not in _VALID_MISSING_STRATEGIES:
                raise ValueError(
                    f"Unknown strategy '{strategy}' for column '{col}'. "
                    f"Valid strategies: {sorted(_VALID_MISSING_STRATEGIES)}"
                )

        result = df.copy()
        log: ChangeLog = []

        for col, strategy in self.strategy_map.items():
            if col not in result.columns:
                raise KeyError(f"Column '{col}' not found in DataFrame.")

            null_mask = result[col].isna()
            null_count = int(null_mask.sum())
            if null_count == 0:
                continue

            if strategy == "drop_row":
                result = result[~null_mask].reset_index(drop=True)
                log.append({"column": col, "strategy": strategy, "affected_rows": null_count})
            elif strategy == "fill_mean":
                fill_val = result[col].mean()
                result[col] = result[col].fillna(fill_val)
                log.append({"column": col, "strategy": strategy, "fill_value": fill_val, "affected_rows": null_count})
            elif strategy == "fill_median":
                fill_val = result[col].median()
                result[col] = result[col].fillna(fill_val)
                log.append({"column": col, "strategy": strategy, "fill_value": fill_val, "affected_rows": null_count})
            elif strategy == "fill_mode":
                mode_series = result[col].mode()
                if mode_series.empty:
                    continue
                fill_val = mode_series.iloc[0]
                result[col] = result[col].fillna(fill_val)
                log.append({"column": col, "strategy": strategy, "fill_value": fill_val, "affected_rows": null_count})
            elif strategy == "fill_const":
                fill_val = self.fill_values.get(col)
                result[col] = result[col].fillna(fill_val)
                log.append({"column": col, "strategy": strategy, "fill_value": fill_val, "affected_rows": null_count})

        return result, log


_VALID_DUPLICATE_MODES = {"exact", "fuzzy"}


class DuplicateCleaner:
    def __init__(self, mode: str = "exact", fuzzy_columns: list[str] | None = None,
                 fuzzy_threshold: int = 90, keep: str = "first") -> None:
        self.mode = mode
        self.fuzzy_columns = fuzzy_columns or []
        self.fuzzy_threshold = fuzzy_threshold
        self.keep = keep

    def clean(self, df: pd.DataFrame) -> tuple[pd.DataFrame, ChangeLog]:
        if self.mode not in _VALID_DUPLICATE_MODES:
            raise ValueError(
                f"Unknown mode '{self.mode}'. Valid modes: {sorted(_VALID_DUPLICATE_MODES)}"
            )

        result = df.copy()
        log: ChangeLog = []

        if self.mode == "exact":
            before = len(result)
            result = result.drop_duplicates(keep=self.keep).reset_index(drop=True)
            removed = before - len(result)
            log.append({"mode": "exact", "removed_rows": removed})

        elif self.mode == "fuzzy":
            from thefuzz import fuzz  # type: ignore[import]

            indices_to_drop: set[int] = set()
            values = result[self.fuzzy_columns].reset_index(drop=True)

            for i in range(len(values)):
                if i in indices_to_drop:
                    continue
                for j in range(i + 1, len(values)):
                    if j in indices_to_drop:
                        continue
                    score = min(
                        fuzz.ratio(str(values.iloc[i][col]), str(values.iloc[j][col]))
                        for col in self.fuzzy_columns
                    )
                    if score >= self.fuzzy_threshold:
                        indices_to_drop.add(j)

            before = len(result)
            result = result.drop(index=list(indices_to_drop)).reset_index(drop=True)
            removed = before - len(result)
            log.append({"mode": "fuzzy", "removed_rows": removed, "threshold": self.fuzzy_threshold})

        return result, log


class FormatStandardiser:
    def __init__(self, format_config: dict[str, dict[str, Any]]) -> None:
        self.format_config = format_config

    def clean(self, df: pd.DataFrame) -> tuple[pd.DataFrame, ChangeLog]:
        result = df.copy()
        log: ChangeLog = []

        for col, rules in self.format_config.items():
            if col not in result.columns:
                raise KeyError(f"Column '{col}' not found in DataFrame.")

            if "regex_sub" in rules:
                pattern, replacement = rules["regex_sub"]
                result[col] = result[col].astype(str).apply(
                    lambda v: re.sub(pattern, replacement, v)
                )
                log.append({"column": col, "operation": "regex_sub", "pattern": pattern})

            if "cast_dtype" in rules:
                target_dtype = rules["cast_dtype"]
                is_numeric = "float" in str(target_dtype) or "int" in str(target_dtype)
                if is_numeric:
                    numeric_series = pd.to_numeric(result[col], errors="coerce")
                    result[col] = numeric_series.astype(target_dtype if target_dtype != "float64" else float)
                else:
                    result[col] = result[col].astype(target_dtype)
                log.append({"column": col, "operation": "cast_dtype", "target": target_dtype})

            if "parse_date" in rules and rules["parse_date"]:
                def _parse(v: Any) -> str:
                    try:
                        return dateutil_parser.parse(str(v)).strftime("%Y-%m-%d")
                    except (ValueError, OverflowError):
                        return v
                result[col] = result[col].apply(_parse)
                log.append({"column": col, "operation": "parse_date"})

        return result, log
