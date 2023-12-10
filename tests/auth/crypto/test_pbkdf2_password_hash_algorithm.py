def test_verify_with_valid_password(pbkdf2):
    encoded_password = pbkdf2.encode(password="password")
    is_password_verified = pbkdf2.verify(
        password="password", encoded_password=encoded_password
    )
    assert is_password_verified is True


def test_verify_with_invalid_password(pbkdf2):
    encoded_password = pbkdf2.encode(password="password")
    is_password_verified = pbkdf2.verify(
        password="invalid_password", encoded_password=encoded_password
    )
    assert is_password_verified is False
