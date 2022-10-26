from src.testgate.auth.crypto.password.scrypt import Scrypt


def test_verify_password():
    scrypt_password_hasher = Scrypt()
    encoded = scrypt_password_hasher.encode(bytes('147258DsA&', 'UTF-8'))
    checked = scrypt_password_hasher.verify(bytes('147258DsA&', 'UTF-8'), hashed_password=encoded)
    assert checked is True


def test_verify_false_password():
    scrypt_password_hasher = Scrypt()
    encoded = scrypt_password_hasher.encode(bytes('147258DsA&', 'UTF-8'))
    checked = scrypt_password_hasher.verify(bytes('19961996DsA&', 'UTF-8'), hashed_password=encoded)
    assert checked is False
