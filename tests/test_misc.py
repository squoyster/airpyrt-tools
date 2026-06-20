import pytest

from acp.misc import cast_u32


def test_zero():
	assert cast_u32(0) == 0


def test_max_positive_signed():
	assert cast_u32(0x7FFFFFFF) == 0x7FFFFFFF


def test_negative_one():
	assert cast_u32(-1) == 0xFFFFFFFF


def test_negative_two():
	assert cast_u32(-2) == 0xFFFFFFFE


def test_min_signed_in_range():
	assert cast_u32(-0x80000000) == 0x80000000


def test_above_range_raises():
	with pytest.raises(Exception):
		cast_u32(0x80000000)


def test_below_range_raises():
	with pytest.raises(Exception):
		cast_u32(-0x80000001)
