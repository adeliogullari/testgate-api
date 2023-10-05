def test_verify_with_valid_password(scrypt):
    encoded_password = scrypt.encode(password='password')
    is_password_verified = scrypt.verify(password='password', encoded_password=encoded_password)
    assert is_password_verified is True


def test_verify_with_invalid_password(scrypt):
    encoded_password = scrypt.encode(password='password')
    is_password_verified = scrypt.verify(password='invalid_password', encoded_password=encoded_password)
    assert is_password_verified is False
