import pytest
from lccompiler.models import IMM


def test_valid_imm():
    assert IMM(0).isValidImm()
    assert IMM(2).isValidImm()
    assert IMM(10).isValidImm()
    assert IMM(15).isValidImm()
    assert IMM(0x0).isValidImm()
    assert IMM(0x5).isValidImm()
    assert IMM(0xf).isValidImm()


def test_invalid_imm():
    assert not IMM(-1).isValidImm()
    assert not IMM(16).isValidImm()
    assert not IMM(100).isValidImm()
    assert not IMM(0xff).isValidImm()
