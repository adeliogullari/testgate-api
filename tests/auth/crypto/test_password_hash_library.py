import pytest
from src.testgate.auth.crypto.password.library import PasswordHashLibrary


@pytest.mark.parametrize(
    "password_hash_library",
    ["pbkdf2", "scrypt"],
    indirect=True,
)
def test_verify(password_hash_library: PasswordHashLibrary) -> None:
    encoded_password = password_hash_library.encode(password="password")
    is_password_verified = password_hash_library.verify(
        password="password", encoded_password=encoded_password
    )
    assert is_password_verified is True


@pytest.mark.parametrize(
    "password_hash_library",
    ["pbkdf2", "scrypt"],
    indirect=True,
)
def test_verify_with_invalid_password(
    password_hash_library: PasswordHashLibrary,
) -> None:
    encoded_password = password_hash_library.encode(password="password")
    is_password_verified = password_hash_library.verify(
        password="invalid_password", encoded_password=encoded_password
    )
    assert is_password_verified is False


@pytest.mark.parametrize(
    "password_hash_library",
    ["pbkdf2", "scrypt"],
    indirect=True,
)
def test_verify_with_invalid_encoded_password(
    password_hash_library: PasswordHashLibrary,
) -> None:
    encoded_password = password_hash_library.encode(password="invalid_password")
    is_password_verified = password_hash_library.verify(
        password="password", encoded_password=encoded_password
    )
    assert is_password_verified is False
