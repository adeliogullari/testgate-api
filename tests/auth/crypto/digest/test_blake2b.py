def test_verify_valid_blake2b_data(blake2b):
    encoded_data = blake2b.encode(data='data', key='key')
    verified_data = blake2b.verify(data='data', key='key', encoded_data=encoded_data)
    assert verified_data is True


def test_verify_invalid_blake2b_data(blake2b):
    encoded_data = blake2b.encode(data='data', key='key')
    verified_data = blake2b.verify(data='invalid_data', key='key', encoded_data=encoded_data)
    assert verified_data is False
