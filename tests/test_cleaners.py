from __future__ import annotations
import pandas as pd
import pytest
from src.cleaners import DuplicateCleaner, FormatStandardiser, MissingValueCleaner


@pytest.fixture
def df_missing() -> pd.DataFrame:
    return pd.DataFrame({
        "name": ["Alice", None, "Charlie", "Diana"],
        "age": [30, None, 25, 28],
        "city": ["London", "Paris", None, "Berlin"],
        "salary": [50000.0, 60000.0, None, 55000.0],
    })

@pytest.fixture
def df_dupes() -> pd.DataFrame:
    return pd.DataFrame({
        "name": ["Alice Smith", "Alice Smith", "Alce Smth", "Bob Jones"],
        "email": ["alice@example.com", "alice@example.com", "alice@example.com", "bob@example.com"],
        "age": [30, 30, 30, 45],
    })

@pytest.fixture
def df_dirty() -> pd.DataFrame:
    return pd.DataFrame({
        "phone": ["+1 (555) 123-4567", "555.987.6543", "5550001111"],
        "age": ["30", "not-a-number", "25"],
        "signup_date": ["01/15/2024", "2024-02-20", "March 3, 2024"],
    })


class TestMissingValueCleaner:
    def test_drop_row_removes_nulls(self, df_missing):
        cleaner = MissingValueCleaner(strategy_map={"name": "drop_row"})
        result, log = cleaner.clean(df_missing)
        assert result["name"].isna().sum() == 0
        assert len(result) == 3

    def test_fill_mean_replaces_null(self, df_missing):
        cleaner = MissingValueCleaner(strategy_map={"age": "fill_mean"})
        result, log = cleaner.clean(df_missing)
        assert result["age"].isna().sum() == 0
        assert result.loc[1, "age"] == pytest.approx(df_missing["age"].mean())

    def test_fill_const_replaces_null(self, df_missing):
        cleaner = MissingValueCleaner(strategy_map={"city": "fill_const"}, fill_values={"city": "Unknown"})
        result, log = cleaner.clean(df_missing)
        assert result.loc[2, "city"] == "Unknown"

    def test_unknown_strategy_raises(self, df_missing):
        with pytest.raises(ValueError):
            MissingValueCleaner(strategy_map={"age": "fill_magic"}).clean(df_missing)

    def test_unknown_column_raises(self, df_missing):
        with pytest.raises(KeyError):
            MissingValueCleaner(strategy_map={"nonexistent": "drop_row"}).clean(df_missing)


class TestDuplicateCleaner:
    def test_exact_dedup(self, df_dupes):
        result, log = DuplicateCleaner(mode="exact").clean(df_dupes)
        assert len(result) == 3

    def test_fuzzy_dedup(self, df_dupes):
        result, log = DuplicateCleaner(mode="fuzzy", fuzzy_columns=["name"], fuzzy_threshold=85).clean(df_dupes)
        assert len(result) == 2

    def test_invalid_mode_raises(self, df_dupes):
        with pytest.raises(ValueError):
            DuplicateCleaner(mode="magic").clean(df_dupes)


class TestFormatStandardiser:
    def test_regex_phone(self, df_dirty):
        result, _ = FormatStandardiser({"phone": {"regex_sub": ["[^0-9]", ""]}}).clean(df_dirty)
        assert result["phone"].str.match(r"^\d+$").all()

    def test_dtype_cast(self, df_dirty):
        result, _ = FormatStandardiser({"age": {"cast_dtype": "float64"}}).clean(df_dirty)
        assert result["age"].dtype == "float64"
        assert pd.isna(result.loc[1, "age"])

    def test_date_normalisation(self, df_dirty):
        result, _ = FormatStandardiser({"signup_date": {"parse_date": True}}).clean(df_dirty)
        assert result["signup_date"].tolist() == ["2024-01-15", "2024-02-20", "2024-03-03"]

    def test_missing_column_raises(self, df_dirty):
        with pytest.raises(KeyError):
            FormatStandardiser({"nonexistent": {"cast_dtype": "int64"}}).clean(df_dirty)
