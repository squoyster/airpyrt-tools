from acp.encryption import ACPEncryption


def _new():
	return ACPEncryption(b"k" * 16, b"C" * 16, b"S" * 16)


def test_client_roundtrip():
	enc = _new()
	dec = _new()
	data = b"A" * 48
	assert dec.client_decrypt(enc.client_encrypt(data)) == data


def test_server_roundtrip():
	enc = _new()
	dec = _new()
	data = b"B" * 48
	assert dec.server_decrypt(enc.server_encrypt(data)) == data


def test_client_and_server_keys_differ():
	e = _new()
	data = b"X" * 32
	assert e.client_encrypt(data) != e.server_encrypt(data)


def test_deterministic():
	a = _new()
	b = _new()
	assert a.client_encrypt(b"Z" * 16) == b.client_encrypt(b"Z" * 16)
