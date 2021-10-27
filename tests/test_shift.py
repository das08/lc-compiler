import pytest
from lccompiler.shift import LSHIFT
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR, OPERATOR_CONSTRUCT_ERROR


def test_valid_lshift():
    assert LSHIFT("A", 0, "B").print() == "MOV B, 1\nMULT A, B\n"
    assert LSHIFT("A", 1, "B").print() == "MOV B, 2\nMULT A, B\n"
    assert LSHIFT("A", 2, "B").print() == "MOV B, 4\nMULT A, B\n"
    assert LSHIFT("A", 3, "B").print() == "MOV B, 8\nMULT A, B\n"
    assert LSHIFT("B", 3, "GPR[1]").print() == "MOV A, B\nMOV B, 8\nMULT A, B\nMOV GPR[1], B"
    assert LSHIFT("GPR[2]", 3, "GPR[1]").print() == "MOV B, GPR[2]\nMOV A, B\nMOV B, 8\nMULT A, B\nMOV GPR[1], B"


def test_invalid_lshift_construction():
    with pytest.raises(REG_CONSTRUCT_ERROR):
        LSHIFT(reg1="C", val1=0, regOut="GPR[0]")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        LSHIFT(reg1="A", val1=0, regOut="GPR[16]")
    with pytest.raises(IMM_CONSTRUCT_ERROR):
        LSHIFT(reg1="A", val1=4, regOut="GPR[0]")
    with pytest.raises(OPERATOR_CONSTRUCT_ERROR):
        LSHIFT(reg1="A", val1=1)
    with pytest.raises(IMM_CONSTRUCT_ERROR):
        LSHIFT()
    with pytest.raises(IMM_CONSTRUCT_ERROR):
        LSHIFT(regOut="B")
    with pytest.raises(IMM_CONSTRUCT_ERROR):
        LSHIFT(reg1="A", regOut="B")
