from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    clickhouse_host: str = "localhost"
    clickhouse_port: int = 8127
    clickhouse_db: str = "marketing"
    clickhouse_user: str = "default"
    clickhouse_password: str = ""

    dataset_path: str = "dataset/dataset.csv"
    output_dir: str = "output"
    generated_file: str = "output/ads_data_100k.csv"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()