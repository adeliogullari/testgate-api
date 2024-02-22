from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    testgate_uvicorn_host: str
    testgate_uvicorn_port: int
    testgate_uvicorn_log_level: str
    testgate_uvicorn_reload: bool
    testgate_uvicorn_workers: int
    testgate_jwt_access_token_exp_minutes: int
    testgate_jwt_access_token_key: str
    testgate_jwt_access_token_alg: str
    testgate_jwt_refresh_token_exp_days: int
    testgate_jwt_refresh_token_key: str
    testgate_jwt_refresh_token_alg: str
    testgate_postgresql_schema: str
    testgate_postgresql_user: str
    testgate_postgresql_password: str
    testgate_postgresql_host: str
    testgate_postgresql_port: str
    testgate_postgresql_database: str
    testgate_smtp_email_verification: bool
    testgate_smtp_email_address: str
    testgate_smtp_email_username: str
    testgate_smtp_email_password: str
    testgate_kafka_enabled: str
    testgate_kafka_bootstrap_servers: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings():
    return Settings()
