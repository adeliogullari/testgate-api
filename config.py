from typing import Optional
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    testgate_jwt_access_token_exp_minutes: Optional[int]
    testgate_jwt_access_token_key: Optional[str]
    testgate_jwt_access_token_alg: Optional[str]
    testgate_jwt_refresh_token_exp_days: Optional[int]
    testgate_jwt_refresh_token_key: Optional[str]
    testgate_jwt_refresh_token_alg: Optional[str]
    testgate_postgresql_schema: Optional[str]
    testgate_postgresql_user: Optional[str]
    testgate_postgresql_password: Optional[str]
    testgate_postgresql_host: Optional[str]
    testgate_postgresql_port: Optional[str]
    testgate_postgresql_database: Optional[str]
    testgate_smtp_email_address: Optional[str]
    testgate_smtp_email_app_password: Optional[str]

    class Config:
        env_file = ".env"


@lru_cache()
def settings():
    return Settings()


@lru_cache()
def get_settings():
    return Settings()
