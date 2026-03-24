from __future__ import annotations
from pathlib import Path
from typing import Any, Type
import pandas as pd


class SchemaValidator:
    def __init__(self, model: Type[Any], strict: bool = False) -> None:
        self.model = model
        self.strict = strict

    def validate(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        raise NotImplementedError("SchemaValidator.validate() — implement in Phase 3.")


class RuleEngine:
    def __init__(self, rules_path: str | Path = "config/rules.json") -> None:
        self.rules_path = Path(rules_path)
        self._rules: list[dict[str, Any]] = []

    def load(self) -> "RuleEngine":
        raise NotImplementedError("RuleEngine.load() — implement in Phase 3.")

    def apply(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        raise NotImplementedError("RuleEngine.apply() — implement in Phase 3.")


class AnomalyDetector:
    def __init__(self, strategy: str = "iqr", iqr_multiplier: float = 1.5,
                 zscore_threshold: float = 3.0, contamination: float | str = "auto") -> None:
        self.strategy = strategy
        self.iqr_multiplier = iqr_multiplier
        self.zscore_threshold = zscore_threshold
        self.contamination = contamination

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("AnomalyDetector.detect() — implement in Phase 3.")
