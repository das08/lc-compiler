import pytest
from lccompiler.substitute import PUT
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR


def test_valid_substitution():
    assert PUT("A", "A").print() == ""
    assert PUT("A", "B").print() == "MOV A, B"
    assert PUT("A", "IN").print() == "MOV A, IN"
    assert PUT("A", "GPR[0]").print() == "MOV B, GPR[0]\nMOV A, B"

    assert PUT("B", "A").print() == "MOV B, A"
    assert PUT("B", "B").print() == ""
    assert PUT("B", "IN").print() == "MOV B, IN"
    assert PUT("B", "GPR[0]").print() == "MOV B, GPR[0]"

    assert PUT("OUT", "A").print() == "MOV B, A\nMOV OUT, B"
    assert PUT("OUT", "B").print() == "MOV OUT, B"
    assert PUT("OUT", "IN").print() == "MOV B, IN\nMOV OUT, B"
    assert PUT("OUT", "GPR[0]").print() == "MOV B, GPR[0]\nMOV OUT, B"

    assert PUT("GPR[15]", "A").print() == "MOV B, A\nMOV GPR[15], B"
    assert PUT("GPR[15]", "B").print() == "MOV GPR[15], B"
    assert PUT("GPR[15]", "IN").print() == "MOV B, IN\nMOV GPR[15], B"
    assert PUT("GPR[15]", "GPR[0]").print() == "MOV B, GPR[0]\nMOV GPR[15], B"


def test_invalid_substitution():
    with pytest.raises(REG_CONSTRUCT_ERROR):
        PUT("a", "B")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        PUT("A", "b")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        PUT("A", "C")
    with pytest.raises(REG_DECLARATION_ERROR):
        PUT("A", "OUT")
    with pytest.raises(REG_DECLARATION_ERROR):
        PUT("IN", "B")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        PUT("GPR[2]", "GPR[16]")
