from datetime import datetime, timedelta

from src.testgate.auth.oauth2.token.claims import RegisteredClaims


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
