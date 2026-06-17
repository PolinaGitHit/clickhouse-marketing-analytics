import clickhouse_connect
from src.config import settings

_client = None


def get_client():
    global _client
    if _client is None:
        _client = clickhouse_connect.get_client(
            host=settings.clickhouse_host,
            port=settings.clickhouse_port,
            username=settings.clickhouse_user,
            password=settings.clickhouse_password,
        )
        _client.command(f"CREATE DATABASE IF NOT EXISTS {settings.clickhouse_db}")
    return _client


def get_new_client():
    """Создаёт новый ClickHouse-клиент (не singleton).
    Нужен для Streamlit, который рендерит табы в параллельных потоках."""
    return clickhouse_connect.get_client(
        host=settings.clickhouse_host,
        port=settings.clickhouse_port,
        username=settings.clickhouse_user,
        password=settings.clickhouse_password,
    )