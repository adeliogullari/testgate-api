def test_verify_valid_pbkdf2_password(pbkdf2):
    encoded_password = pbkdf2.encode(password='password')
    verified_password = pbkdf2.verify(password='password', encoded_password=encoded_password)
    assert verified_password is True


def test_verify_invalid_pbkdf2_password(pbkdf2):
    encoded_password = pbkdf2.encode(password='password')
    verified_password = pbkdf2.verify(password='invalid_password', encoded_password=encoded_password)
    assert verified_password is False
