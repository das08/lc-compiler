import pytest
from lccompiler.declare_var import LET
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR


def test_valid_declaration():
    assert LET("A", 10).print() == "MOV A, 10"
    assert LET("B", 0).print() == "MOV B, 0"
    assert LET("OUT", 0xf).print() == "MOV OUT, 15"
    assert LET("GPR[12]", 1).print() == "MOV B, 1\nMOV GPR[12], B"
    assert LET("GPR[15]", 0x5).print() == "MOV B, 5\nMOV GPR[15], B"


def test_invalid_reg_declaration():
    with pytest.raises(REG_CONSTRUCT_ERROR):
        LET("a", 10)
    with pytest.raises(REG_CONSTRUCT_ERROR):
        LET("C", 10)
    with pytest.raises(REG_CONSTRUCT_ERROR):
        LET("GPR[16]", 10)


def test_invalid_reg_declaration_in():
    with pytest.raises(REG_DECLARATION_ERROR):
        LET("IN", 10)


def test_invalid_imm_declaration():
    with pytest.raises(IMM_CONSTRUCT_ERROR):
        LET("A", 100)
    with pytest.raises(IMM_CONSTRUCT_ERROR):
        LET("A", -1)
    with pytest.raises(IMM_CONSTRUCT_ERROR):
        LET("GPR[0]", 16)
