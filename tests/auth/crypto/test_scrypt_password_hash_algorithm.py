from src.testgate.auth.crypto.password.scrypt import Scrypt


def test_verify(scrypt: Scrypt) -> None:
    encoded_password = scrypt.encode(password="password")
    is_password_verified = scrypt.verify(
        password="password", encoded_password=encoded_password
    )
    assert is_password_verified is True


def test_verify_with_invalid_password(scrypt: Scrypt) -> None:
    encoded_password = scrypt.encode(password="password")
    is_password_verified = scrypt.verify(
        password="invalid_password", encoded_password=encoded_password
    )
    assert is_password_verified is False


def test_verify_with_invalid_encoded_password(scrypt: Scrypt) -> None:
    encoded_password = scrypt.encode(password="invalid_password")
    is_password_verified = scrypt.verify(
        password="password", encoded_password=encoded_password
    )
    assert is_password_verified is False
