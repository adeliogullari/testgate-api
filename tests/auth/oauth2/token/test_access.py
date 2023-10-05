from datetime import datetime, timedelta

from src.testgate.auth.crypto.digest.strategy import Blake2bMessageDigestStrategy
from src.testgate.auth.oauth2.token.claims import RegisteredClaims
from src.testgate.auth.oauth2.token.access import AccessToken


def test_registered_claims_verification_with_default_attributes():
    registered_claims = RegisteredClaims()
    assert registered_claims.verify() is True


def test_registered_claims_verification_with_custom_attributes():
    now = datetime.utcnow()
    exp = (now + timedelta(seconds=7200)).timestamp()
    nbf = (now - timedelta(seconds=60)).timestamp()
    iat = (now - timedelta(seconds=60)).timestamp()

    registered_claims = RegisteredClaims(**{'iss': 'issuer',
                                            'sub': 'subject',
                                            'aud': 'audience',
                                            'exp': exp,
                                            'nbf': nbf,
                                            'iat': iat})
    assert registered_claims.verify(iss='issuer', sub='subject', aud='audience') is True


def test_registered_claims_verification_with_exceed_expiration():
    now = datetime.utcnow()
    exp = (now + timedelta(seconds=0)).timestamp()
    nbf = (now - timedelta(seconds=0)).timestamp()
    iat = (now - timedelta(seconds=0)).timestamp()

    registered_claims = RegisteredClaims(**{'iss': 'issuer',
                                            'sub': 'subject',
                                            'aud': 'audience',
                                            'exp': exp,
                                            'nbf': nbf,
                                            'iat': iat})
    assert registered_claims.verify(iss='issuer', sub='subject', aud='audience') is False


def test_access_token_encode():
    access_token = AccessToken(Blake2bMessageDigestStrategy())
    token = access_token.encode(payload={'email': 'username@testgate.com'}, key='secret', headers={'alg': 'blake2b'})
    assert token is not None


def test_access_token_decode():
    access_token = AccessToken(Blake2bMessageDigestStrategy())
    token = access_token.encode(payload={}, key='secret', headers={})
    info = access_token.decode(token=token)
    assert info is not None


def test_access_verify_token():
    access_token = AccessToken(Blake2bMessageDigestStrategy())
    token = access_token.encode(payload={'email': 'username@testgate.com'}, key='secret', headers={'alg': 'blake2b'})
    is_verified = access_token.verify(key='secret', token=token)
    assert is_verified is True


def test_access_verify_token_with_invalid_key():
    access_token = AccessToken(Blake2bMessageDigestStrategy())
    token = access_token.encode(payload={'email': 'username@testgate.com'}, key='secret', headers={'alg': 'blake2b'})
    is_verified = access_token.verify(key='invalid_key', token=token)
    assert is_verified is False
