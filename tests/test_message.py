import pytest

from acp.exception import ACPMessageError
from acp.keystream import generate_acp_keystream
from acp.message import ACPMessage, _generate_acp_header_key


def test_header_magic_is_bytes():
	assert ACPMessage._header_magic == b"acpp"


def test_header_key_length():
	assert len(_generate_acp_header_key("secret")) == 32


def test_empty_password_header_key_is_keystream():
	assert _generate_acp_header_key("") == generate_acp_keystream(32)


def test_echo_roundtrip():
	raw = ACPMessage.compose_echo_command(0, "secret", b"hi")
	m = ACPMessage.parse_raw(raw)
	assert m.command == 1
	assert m.body == b"hi"
	assert m.body_size == 2


def test_feat_stream_header():
	raw = ACPMessage.compose_feat_command(0)
	m = ACPMessage.parse_raw(raw)
	assert m.command == 0x1b
	assert m.body_size == -1
	assert m.body_checksum == 1
	assert m.body is None


def test_bad_magic_raises():
	raw = bytearray(ACPMessage.compose_echo_command(0, "x", b"y"))
	raw[0:4] = b"XXXX"
	with pytest.raises(ACPMessageError):
		ACPMessage.parse_raw(bytes(raw))


def test_corrupt_header_checksum_raises():
	raw = bytearray(ACPMessage.compose_echo_command(0, "x", b"y"))
	raw[28] ^= 0xFF
	with pytest.raises(ACPMessageError):
		ACPMessage.parse_raw(bytes(raw))
