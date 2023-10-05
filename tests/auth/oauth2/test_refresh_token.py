import pytest
from src.testgate.auth.crypto import Blake2bMessageDigestStrategy


@pytest.mark.parametrize("refresh_token", [Blake2bMessageDigestStrategy()], indirect=True)
def test_encode_with_valid_payload_and_key(refresh_token):
    token = refresh_token.encode(payload={'email': 'username@testgate.com'},
                                 key='key',
                                 headers={'alg': 'blake2b'})
    assert token is not None


@pytest.mark.parametrize("refresh_token", [Blake2bMessageDigestStrategy()], indirect=True)
def test_decode_with_valid_payload_and_key(refresh_token):
    token = refresh_token.encode(payload={'email': 'username@testgate.com'},
                                 key='key',
                                 headers={'alg': 'blake2b'})

    payload, headers, signature = refresh_token.decode(token=token)

    assert payload['email'] == "username@testgate.com"
    assert headers['alg'] == "blake2b"
    assert signature is not None


@pytest.mark.parametrize("refresh_token", [Blake2bMessageDigestStrategy()], indirect=True)
def test_verify_with_valid_token_and_key(refresh_token):
    token = refresh_token.encode(payload={'email': 'username@testgate.com'},
                                 key='key',
                                 headers={'alg': 'blake2b', "typ": "JWT"})

    is_token_verified = refresh_token.verify(key='key', token=token)

    assert is_token_verified is True


@pytest.mark.parametrize("refresh_token", [Blake2bMessageDigestStrategy()], indirect=True)
def test_verify_with_invalid_key(refresh_token):
    token = refresh_token.encode(payload={'email': 'username@testgate.com'},
                                 key='key',
                                 headers={'alg': 'blake2b'})

    is_token_verified = refresh_token.verify(key='invalid_key', token=token)

    assert is_token_verified is False


@pytest.mark.parametrize("refresh_token", [Blake2bMessageDigestStrategy()], indirect=True)
def test_verify_and_decode_with_valid_token_and_key(refresh_token):
    token = refresh_token.encode(payload={'email': 'username@testgate.com'},
                                 key='key',
                                 headers={'alg': 'blake2b'})

    verified, payload, headers, signature = refresh_token.verify_and_decode(key='key', token=token)

    assert verified is True
    assert payload['email'] == "username@testgate.com"
    assert headers['alg'] == "blake2b"
    assert signature is not None
