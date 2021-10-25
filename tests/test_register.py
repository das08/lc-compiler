import pytest
from lccompiler.models import REGISTER


def test_valid_reg_name():
    assert REGISTER("A").isValidRegName()
    assert REGISTER("B").isValidRegName()
    assert REGISTER("IN").isValidRegName()
    assert REGISTER("OUT").isValidRegName()
    assert REGISTER("GPR[0]").isValidRegName()
    assert REGISTER("GPR[9]").isValidRegName()
    assert REGISTER("GPR[10]").isValidRegName()
    assert REGISTER("GPR[15]").isValidRegName()


def test_invalid_reg_name():
    assert not REGISTER("a").isValidRegName()
    assert not REGISTER("C").isValidRegName()
    assert not REGISTER("AA").isValidRegName()
    assert not REGISTER("").isValidRegName()
    assert not REGISTER(" A").isValidRegName()
    assert not REGISTER(",A").isValidRegName()
    assert not REGISTER("GPR").isValidRegName()
    assert not REGISTER("GPR[]").isValidRegName()
    assert not REGISTER("GPR0]").isValidRegName()
    assert not REGISTER("GPR[0").isValidRegName()
    assert not REGISTER("GPr[0]").isValidRegName()
    assert not REGISTER("GPr[00]").isValidRegName()
    assert not REGISTER("GPr[16]").isValidRegName()
