from acp.keystream import generate_acp_keystream, ACP_STATIC_KEY


def test_empty():
	assert generate_acp_keystream(0) == b""


def test_length():
	assert len(generate_acp_keystream(100)) == 100
	assert len(generate_acp_keystream(300)) == 300


def test_first_byte():
	ks = generate_acp_keystream(16)
	assert ks[0] == 0x0e


def test_formula():
	ks = generate_acp_keystream(512)
	n = len(ACP_STATIC_KEY)
	for i in range(512):
		expected = ((i + 0x55) & 0xFF) ^ ACP_STATIC_KEY[i % n]
		assert ks[i] == expected


def test_repeats_every_256():
	ks = generate_acp_keystream(512)
	assert ks[:256] == ks[256:512]
