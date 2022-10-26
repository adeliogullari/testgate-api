def test_verify_valid_scrypt_password(scrypt):
    encoded_password = scrypt.encode(password='password')
    verified_password = scrypt.verify(password='password', encoded_password=encoded_password)
    assert verified_password is True


def test_verify_invalid_scrypt_password(scrypt):
    encoded_password = scrypt.encode(password='password')
    verified_password = scrypt.verify(password='invalid_password', encoded_password=encoded_password)
    assert verified_password is False
