from __future__ import annotations
from pathlib import Path
from typing import Any
import pandas as pd


class CSVLoader:
    def __init__(self, path: str | Path, encoding: str | None = None, sep: str = ",", **kwargs: Any) -> None:
        self.path = Path(path)
        self.encoding = encoding
        self.sep = sep
        self.kwargs = kwargs

    def load(self) -> pd.DataFrame:
        raise NotImplementedError("CSVLoader.load() — implement in Phase 1.")


class JSONLoader:
    def __init__(self, path: str | Path, orient: str | None = None) -> None:
        self.path = Path(path)
        self.orient = orient

    def load(self) -> pd.DataFrame:
        raise NotImplementedError("JSONLoader.load() — implement in Phase 1.")


class ExcelLoader:
    def __init__(self, path: str | Path, sheet_name: int | str = 0, header: int = 0) -> None:
        self.path = Path(path)
        self.sheet_name = sheet_name
        self.header = header

    def load(self) -> pd.DataFrame:
        raise NotImplementedError("ExcelLoader.load() — implement in Phase 1.")


class DatabaseLoader:
    def __init__(self, connection_string: str, query: str) -> None:
        self.connection_string = connection_string
        self.query = query

    def load(self) -> pd.DataFrame:
        raise NotImplementedError("DatabaseLoader.load() — implement in Phase 1.")


class DataProfiler:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def profile(self) -> dict[str, Any]:
        raise NotImplementedError("DataProfiler.profile() — implement in Phase 1.")
