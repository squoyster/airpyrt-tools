import gzip
import io
import struct
import zlib

import pytest

from acp.basebinary import Basebinary, BasebinaryError, _basebinary_keys, _derive_key


def test_known_key_length():
	assert len(_derive_key(107)) == 16


def test_derive_known_value():
	raw = bytes.fromhex(_basebinary_keys[107])
	expected = bytes(raw[i] ^ (i + 0x19) for i in range(16))
	assert _derive_key(107) == expected


def test_unknown_model_returns_none():
	assert _derive_key(999) is None


def _craft(model=107, flags=0, byte_0x0F=0, inner=b"payload-data"):
	magic = b"APPLE-FIRMWARE\x00"
	hdr = struct.pack(">15sB2I4BI", magic, byte_0x0F, model, 1, 0, 0, 0, flags, 0)
	cksum = zlib.adler32(hdr + inner) & 0xFFFFFFFF
	return hdr + inner + struct.pack(">I", cksum)


def test_parse_valid():
	assert Basebinary.parse(_craft()) == b"payload-data"


def test_bad_checksum():
	data = bytearray(_craft())
	data[-1] ^= 0xFF
	with pytest.raises(BasebinaryError):
		Basebinary.parse(bytes(data))


def test_bad_magic():
	data = b"NOT-APPLE-FW\x00\x00" + _craft()[15:]
	with pytest.raises(BasebinaryError):
		Basebinary.parse(data)


def test_short_data():
	with pytest.raises(BasebinaryError):
		Basebinary.parse(b"too short")


def test_encrypted_missing_key_raises():
	data = _craft(model=999, flags=2, inner=b"\x00" * 32)
	with pytest.raises(BasebinaryError):
		Basebinary.parse(data)


def test_extract_gzip():
	buf = io.BytesIO()
	with gzip.GzipFile(fileobj=buf, mode="wb") as g:
		g.write(b"hello-world")
	assert Basebinary.extract(b"prefix-junk" + buf.getvalue()) == b"hello-world"
