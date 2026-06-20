import struct

import pytest

from acp.cflbinary import CFLBinaryPListComposer
from acp.exception import ACPPropertyError
from acp.property import ACPProperty


def test_supported_includes_syAP():
	assert "syAP" in ACPProperty.get_supported_property_names()


def test_null_property_roundtrip():
	p = ACPProperty()
	assert p.name is None
	assert p.value is None
	raw = ACPProperty.compose_raw_element(0, p)
	back = ACPProperty.parse_raw_element(raw)
	assert back.name is None
	assert back.value is None


def test_invalid_name_raises():
	with pytest.raises(ACPPropertyError):
		ACPProperty("nope", 1)


def test_dec_int_and_packed():
	assert ACPProperty("syAP", 5).value == 5
	assert str(ACPProperty("syAP", 5)) == "5"
	assert ACPProperty("syAP", struct.pack("!I", 42)).value == 42


def test_hex_int_and_packed():
	assert ACPProperty("syFl", 0x10).value == 0x10
	assert ACPProperty("syFl", struct.pack("!I", 0xAB)).value == 0xAB


def test_mac_str_and_bytes():
	p = ACPProperty("raMA", "aa:bb:cc:dd:ee:ff")
	assert p.value == bytes.fromhex("aabbccddeeff")
	assert str(p) == "aa:bb:cc:dd:ee:ff"
	p2 = ACPProperty("raMA", b"\xaa\xbb\xcc\xdd\xee\xff")
	assert str(p2) == "aa:bb:cc:dd:ee:ff"


def test_mac_bad_raises():
	with pytest.raises(ACPPropertyError):
		ACPProperty("raMA", "not-a-mac")


def test_bin_format():
	assert str(ACPProperty("diag", b"\x01\x02\x0a")) == "01020a"


def test_str_decode():
	p = ACPProperty("syNm", "My Router")
	assert p.value == b"My Router"
	assert str(p) == "My Router"
	assert ACPProperty("syNm", b"raw").value == b"raw"


def test_compose_raw_element_roundtrip():
	raw = ACPProperty.compose_raw_element(0, ACPProperty("syAP", 7))
	back = ACPProperty.parse_raw_element(raw)
	assert back.name == "syAP"
	assert back.value == 7


def test_log_format():
	val = b"line one\x00line two\x00"
	s = str(ACPProperty("logm", val))
	assert "line one" in s
	assert "line two" in s


def test_cfb_format():
	blob = CFLBinaryPListComposer.compose({"k": b"v", "n": 3})
	s = str(ACPProperty("DynS", blob))
	assert "'k'" in s
