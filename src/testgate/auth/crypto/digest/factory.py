from src.testgate.auth.crypto.digest.strategy import (
    Blake2bMessageDigestStrategy,
    MessageDigestStrategy,
)


class MessageDigestStrategyFactory:
    @staticmethod
    def create(algorithm: str) -> MessageDigestStrategy:
        strategies = {"blake2b": Blake2bMessageDigestStrategy()}
        return strategies.get(algorithm, strategies["blake2b"])
