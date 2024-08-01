from datetime import datetime, timedelta
from src.testgate.auth.oauth2.token.claims import Payload


def test_verify_with_default_attributes(payload: Payload) -> None:
    assert payload.verify() is True


def test_verify_with_custom_attributes(payload: Payload) -> None:
    now = datetime.utcnow()
    exp = (now + timedelta(seconds=7200)).timestamp()
    nbf = (now - timedelta(seconds=60)).timestamp()
    iat = (now - timedelta(seconds=60)).timestamp()

    payload.exp = exp
    payload.nbf = nbf
    payload.iat = iat

    assert payload.verify(iss=payload.iss, sub=payload.sub, aud=payload.aud) is True


def test_verify_with_exceed_expiration(payload: Payload) -> None:
    now = datetime.utcnow()
    exp = (now - timedelta(seconds=7200)).timestamp()
    nbf = (now + timedelta(seconds=60)).timestamp()
    iat = (now + timedelta(seconds=60)).timestamp()

    payload.exp = exp
    payload.nbf = nbf
    payload.iat = iat

    assert payload.verify(iss=payload.iss, sub=payload.sub, aud=payload.aud) is False
