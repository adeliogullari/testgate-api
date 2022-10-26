from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    testgate_jwt_token_exp: str
    testgate_jwt_token_key: str
    testgate_jwt_token_algorithms: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
