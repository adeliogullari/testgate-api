from src.testgate.auth.crypto.password.strategy import (
    Pbkdf2PasswordHashStrategy,
    ScryptPasswordHashStrategy,
    PasswordHashStrategy,
)


class PasswordHashStrategyFactory:
    @staticmethod
    def create(algorithm: str) -> PasswordHashStrategy:
        strategies = {
            "pbkdf2": Pbkdf2PasswordHashStrategy(),
            "scrypt": ScryptPasswordHashStrategy(),
        }
        return strategies.get(algorithm, strategies["scrypt"])
