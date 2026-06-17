import pytest
from pathlib import Path
from src.analytics.queries import load_query, AVAILABLE_QUERIES, QUERIES_DIR


class TestQueries:
    def test_queries_dir_exists(self):
        assert QUERIES_DIR.exists(), f"Queries dir not found: {QUERIES_DIR}"

    def test_all_sql_files_exist(self):
        for name, filename in AVAILABLE_QUERIES.items():
            path = QUERIES_DIR / filename
            assert path.exists(), f"Missing SQL file: {filename}"

    def test_all_sql_files_non_empty(self):
        for name, filename in AVAILABLE_QUERIES.items():
            sql = load_query(filename)
            assert len(sql.strip()) > 0, f"Empty SQL file: {filename}"

    def test_all_sql_have_select_or_cte(self):
        for name, filename in AVAILABLE_QUERIES.items():
            sql = load_query(filename).strip().upper()
            assert sql.startswith(("SELECT", "WITH")), f"Query {filename} must start with SELECT or WITH (CTE)"

    def test_cohort_sql_files_exist(self):
        cohort_dir = QUERIES_DIR / "cohort"
        assert cohort_dir.exists()
        expected = [
            "01_create_cohorts.sql",
            "02_retention_active.sql",
            "03_retention_function.sql",
            "04_keyword_retention.sql",
        ]
        for fname in expected:
            assert (cohort_dir / fname).exists(), f"Missing cohort SQL: {fname}"