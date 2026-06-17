import pytest
from src.analytics.queries import load_query


class TestCohortQueries:
    def test_create_cohorts_is_insert(self):
        sql = load_query("cohort/01_create_cohorts.sql").strip().upper()
        assert "INSERT" in sql, "Cohort creation must contain INSERT"

    def test_retention_active_has_select(self):
        sql = load_query("cohort/02_retention_active.sql").strip().upper()
        assert sql.startswith("SELECT")

    def test_retention_function_has_with(self):
        sql = load_query("cohort/03_retention_function.sql").strip().upper()
        assert sql.startswith("WITH") or sql.startswith("SELECT"), \
            "Retention function must start with WITH or SELECT"

    def test_keyword_retention_has_select(self):
        sql = load_query("cohort/04_keyword_retention.sql").strip().upper()
        assert sql.startswith("WITH") or sql.startswith("SELECT"), \
            "Keyword retention must start with WITH or SELECT"