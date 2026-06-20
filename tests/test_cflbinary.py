from collections import OrderedDict

import pytest

from acp.cflbinary import (
	CFLBinaryPListComposer as Composer,
	CFLBinaryPListParser as Parser,
	CFLBinaryPListParseError,
)


@pytest.mark.parametrize("value", [
	None,
	True,
	False,
	0,
	1,
	255,
	256,
	65535,
	65536,
	70000,
	0x100000000,
	1.5,
	b"",
	b"hello",
	b"\x00\x01\x02",
	"hello",
	"héllo",
	[],
	[1, 2, 3],
	[b"a", "b", 1.5, 42],
	OrderedDict(),
	OrderedDict([("a", 1), ("b", b"x")]),
])
def test_roundtrip(value):
	assert Parser.parse(Composer.compose(value)) == value


def test_bool_distinct_from_int():
	assert Parser.parse(Composer.compose(True)) is True
	assert Parser.parse(Composer.compose(False)) is False
	assert Parser.parse(Composer.compose(1)) == 1
	assert Parser.parse(Composer.compose(0)) == 0


def test_bad_header_magic():
	with pytest.raises(CFLBinaryPListParseError):
		Parser.parse(b"XXXX" + b"\x00" + b"END!")


def test_short_data():
	with pytest.raises(CFLBinaryPListParseError):
		Parser.parse(b"CF")


def test_bad_footer():
	with pytest.raises(CFLBinaryPListParseError):
		Parser.parse(b"CFB0" + b"\x00" + b"NOPE")


def test_none_inside_container_is_format_limitation():
	# This hacky format reuses the 0x00 null marker as the array/dict
	# terminator (see _unpack_object: `if element == None: break`), so a
	# None element cannot be stored inside a container. This locks in that
	# legacy behavior: composing a list with None truncates on parse, the
	# leftover bytes then trip the "extra data" check and parse raises.
	raw = Composer.compose([b"a", None, b"b"])
	with pytest.raises(CFLBinaryPListParseError):
		Parser.parse(raw)

