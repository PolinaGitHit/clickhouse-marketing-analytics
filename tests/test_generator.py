import pytest
import pandas as pd
from src.data.generator import generate, COLUMNS


class TestGenerator:
    def test_generate_returns_dataframe(self):
        df = generate(n_rows=100, seed=42)
        assert isinstance(df, pd.DataFrame)

    def test_generate_correct_row_count(self):
        df = generate(n_rows=1000, seed=42)
        assert len(df) == 1000

    def test_generate_has_expected_columns(self):
        df = generate(n_rows=100, seed=42)
        for col in COLUMNS:
            assert col in df.columns, f"Missing column: {col}"

    def test_generate_reproducible_seed(self):
        df1 = generate(n_rows=500, seed=123)
        df2 = generate(n_rows=500, seed=123)
        assert df1.equals(df2)

    def test_generate_different_seed_produces_different_data(self):
        df1 = generate(n_rows=500, seed=1)
        df2 = generate(n_rows=500, seed=999)
        assert not df1.equals(df2)