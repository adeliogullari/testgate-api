from src.testgate.auth.crypto.digest.blake2b import Blake2b


def test_verify(blake2b: Blake2b) -> None:
    encoded_data = blake2b.encode(data="data", key="key")
    is_data_verified = blake2b.verify(data="data", key="key", encoded_data=encoded_data)
    assert is_data_verified is True


def test_verify_with_invalid_data(blake2b: Blake2b) -> None:
    encoded_data = blake2b.encode(data="data", key="key")
    is_data_verified = blake2b.verify(
        data="invalid_data", key="key", encoded_data=encoded_data
    )
    assert is_data_verified is False


def test_verify_with_invalid_key(blake2b: Blake2b) -> None:
    encoded_data = blake2b.encode(data="data", key="key")
    is_data_verified = blake2b.verify(
        data="data", key="invalid_key", encoded_data=encoded_data
    )
    assert is_data_verified is False
