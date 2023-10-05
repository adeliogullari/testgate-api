from datetime import datetime, timedelta

from src.testgate.auth.crypto.digest.strategy import Blake2bMessageDigestStrategy
from src.testgate.auth.oauth2.token.refresh import RefreshToken


def test_refresh_token_encode():
    refresh_token = RefreshToken(Blake2bMessageDigestStrategy())
    token = refresh_token.encode(payload={'email': 'username@testgate.com'}, key='secret', headers={'alg': 'blake2b'})
    assert token is not None


def test_refresh_token_decode():
    refresh_token = RefreshToken(Blake2bMessageDigestStrategy())
    token = refresh_token.encode(payload={}, key='secret', headers={})
    info = refresh_token.decode(token=token)
    assert info is not None


def test_refresh_verify_token():
    refresh_token = RefreshToken(Blake2bMessageDigestStrategy())
    token = refresh_token.encode(payload={'email': 'username@testgate.com'}, key='secret', headers={'alg': 'blake2b'})
    is_verified = refresh_token.verify(key='secret', token=token)
    assert is_verified is True


def test_refresh_verify_token_with_invalid_key():
    refresh_token = RefreshToken(Blake2bMessageDigestStrategy())
    token = refresh_token.encode(payload={'email': 'username@testgate.com'}, key='secret', headers={'alg': 'blake2b'})
    is_verified = refresh_token.verify(key='invalid_key', token=token)
    assert is_verified is False
