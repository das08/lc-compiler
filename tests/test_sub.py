import pytest
from lccompiler.oparator import SUB
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR


def test_valid_subtraction_reg_reg():
    assert SUB(reg1="A", reg2="A", regOut="A").print() == "MOV A, 0"


def test_invalid_subtraction_construction():
    with pytest.raises(REG_CONSTRUCT_ERROR):
        SUB(reg1="C", reg2="B", regOut="GPR[0]")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        SUB(reg1="A", reg2="C", regOut="GPR[0]")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        SUB(reg1="A", reg2="GPR[1]", regOut="GPR[16]")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        SUB(reg1="A", reg2="GPR[2]", regOut="C")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        SUB(reg1="A", reg2="C")


def test_invalid_subtraction_declaration():
    with pytest.raises(REG_DECLARATION_ERROR):
        SUB(reg1="IN", reg2="B", regOut="GPR[0]")
    with pytest.raises(REG_DECLARATION_ERROR):
        SUB(reg1="A", reg2="IN", regOut="GPR[0]")
    with pytest.raises(REG_DECLARATION_ERROR):
        SUB(reg1="A", reg2="B", regOut="IN")
    with pytest.raises(REG_DECLARATION_ERROR):
        SUB(reg1="GPR[15]", reg2="B", regOut="GPR[0]")
    with pytest.raises(REG_DECLARATION_ERROR):
        SUB(reg1="A", reg2="GPR[15]", regOut="GPR[0]")
    with pytest.raises(REG_DECLARATION_ERROR):
        SUB(reg1="A", reg2="GPR[0]", regOut="IN")
    with pytest.raises(REG_DECLARATION_ERROR):
        SUB(reg1="A", reg2="GPR[15]", regOut="GPR[15]")
    with pytest.raises(REG_DECLARATION_ERROR):
        SUB(reg1="OUT", reg2="GPR[0]", regOut="A")

