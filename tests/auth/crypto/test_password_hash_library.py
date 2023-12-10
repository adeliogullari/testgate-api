import pytest
from src.testgate.auth.crypto.password.strategy import (
    Pbkdf2PasswordHashStrategy,
    ScryptPasswordHashStrategy,
)


@pytest.mark.parametrize(
    "password_hash_library",
    [Pbkdf2PasswordHashStrategy(), ScryptPasswordHashStrategy()],
    indirect=True,
)
def test_verify_with_valid_password(password_hash_library):
    encoded_password = password_hash_library.encode(password="password")
    is_password_verified = password_hash_library.verify(
        password="password", encoded_password=encoded_password
    )
    assert is_password_verified is True


@pytest.mark.parametrize(
    "password_hash_library",
    [Pbkdf2PasswordHashStrategy(), ScryptPasswordHashStrategy()],
    indirect=True,
)
def test_verify_with_invalid_password(password_hash_library):
    encoded_password = password_hash_library.encode(password="password")
    is_password_verified = password_hash_library.verify(
        password="invalid_password", encoded_password=encoded_password
    )
    assert is_password_verified is False
