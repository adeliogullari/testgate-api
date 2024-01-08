import pytest
from src.testgate.auth.crypto.digest.strategy import Blake2bMessageDigestStrategy


@pytest.mark.parametrize(
    "message_digest_library", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_verify(message_digest_library):
    encoded_data = message_digest_library.encode(data="data", key="key")
    is_data_verified = message_digest_library.verify(
        data="data", key="key", encoded_data=encoded_data
    )
    assert is_data_verified is True


@pytest.mark.parametrize(
    "message_digest_library", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_verify_with_invalid_data(message_digest_library):
    encoded_data = message_digest_library.encode(data="data", key="key")
    is_data_verified = message_digest_library.verify(
        data="invalid_data", key="key", encoded_data=encoded_data
    )
    assert is_data_verified is False


@pytest.mark.parametrize(
    "message_digest_library", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_verify_with_invalid_key(message_digest_library):
    encoded_data = message_digest_library.encode(data="data", key="key")
    is_data_verified = message_digest_library.verify(
        data="data", key="invalid_key", encoded_data=encoded_data
    )
    assert is_data_verified is False
