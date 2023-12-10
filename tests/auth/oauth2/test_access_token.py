import pytest
from datetime import datetime
from src.testgate.auth.crypto.digest.strategy import Blake2bMessageDigestStrategy


@pytest.mark.parametrize(
    "access_token", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_encode_with_valid_payload_and_key(access_token):
    token = access_token.encode(
        payload={"email": "username@testgate.com"},
        key="key",
        headers={"alg": "blake2b", "typ": "JWT"},
    )
    assert token is not None


@pytest.mark.parametrize(
    "access_token", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_decode_with_valid_payload_and_key(access_token):
    token = access_token.encode(
        payload={"email": "username@testgate.com"},
        key="key",
        headers={"alg": "blake2b", "typ": "JWT"},
    )

    payload, headers, signature = access_token.decode(token=token)

    assert payload["email"] == "username@testgate.com"
    assert headers["alg"] == "blake2b"
    assert signature is not None


@pytest.mark.parametrize(
    "access_token", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_verify_with_valid_token_and_key(access_token):
    token = access_token.encode(
        payload={"email": "username@testgate.com"},
        key="key",
        headers={"alg": "blake2b"},
    )

    is_token_verified = access_token.verify(key="key", token=token)

    assert is_token_verified is True


@pytest.mark.parametrize(
    "access_token", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_verify_with_invalid_key(access_token):
    token = access_token.encode(
        payload={"email": "username@testgate.com"},
        key="key",
        headers={"alg": "blake2b"},
    )

    is_token_verified = access_token.verify(key="invalid_key", token=token)

    assert is_token_verified is False


@pytest.mark.parametrize(
    "access_token", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_verify_with_exceed_expiration(access_token):
    exp = datetime.utcnow().timestamp()
    token = access_token.encode(
        payload={"exp": exp, "email": "username@testgate.com"},
        key="key",
        headers={"alg": "blake2b"},
    )

    is_token_verified = access_token.verify(key="key", token=token)

    assert is_token_verified is False


@pytest.mark.parametrize(
    "access_token", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_verify_and_decode_with_valid_token_and_key(access_token):
    token = access_token.encode(
        payload={"email": "username@testgate.com"},
        key="key",
        headers={"alg": "blake2b"},
    )

    verified, payload, headers, signature = access_token.verify_and_decode(
        key="key", token=token
    )

    assert verified is True
    assert payload["email"] == "username@testgate.com"
    assert headers["alg"] == "blake2b"
    assert signature is not None


@pytest.mark.parametrize(
    "access_token", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_verify_and_decode_with_invalid_key(access_token):
    token = access_token.encode(
        payload={"email": "username@testgate.com"},
        key="key",
        headers={"alg": "blake2b"},
    )

    verified, payload, headers, signature = access_token.verify_and_decode(
        key="invalid_key", token=token
    )

    assert verified is False


@pytest.mark.parametrize(
    "access_token", [Blake2bMessageDigestStrategy()], indirect=True
)
def test_verify_and_decode_with_exceed_expiration(access_token):
    exp = datetime.utcnow().timestamp()
    token = access_token.encode(
        payload={"exp": exp, "email": "username@testgate.com"},
        key="key",
        headers={"alg": "blake2b"},
    )

    verified, payload, headers, signature = access_token.verify_and_decode(
        key="key", token=token
    )

    assert verified is False
