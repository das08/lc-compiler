import pytest
from lccompiler.oparator import SUB
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR, OPERATOR_CONSTRUCT_ERROR


def test_valid_subtraction_reg_reg():
    # A A
    assert SUB(reg1="A", reg2="A", regOut="A").print() == "MOV A, 0"
    assert SUB(reg1="A", reg2="A", regOut="B").print() == "MOV B, 0"
    assert SUB(reg1="A", reg2="A", regOut="GPR[2]").print() == "MOV B, 0\nMOV GPR[2], B"
    # A B
    assert SUB(reg1="A", reg2="B", regOut="A").print() == "SUB A, B\n"
    assert SUB(reg1="A", reg2="B", regOut="B").print() == "SUB A, B\nMOV B, A"
    assert SUB(reg1="A", reg2="B", regOut="GPR[2]").print() == "SUB A, B\nMOV B, A\nMOV GPR[2], B"
    # A GPR[0]
    assert SUB(reg1="A", reg2="GPR[0]", regOut="A").print() == "MOV B, GPR[0]\nSUB A, B\n"
    assert SUB(reg1="A", reg2="GPR[0]", regOut="B").print() == "MOV B, GPR[0]\nSUB A, B\nMOV B, A"
    assert SUB(reg1="A", reg2="GPR[0]", regOut="GPR[2]").print() == "MOV B, GPR[0]\nSUB A, B\nMOV B, A\nMOV GPR[2], B"
    # B A
    # assert SUB(reg1="B", reg2="A", regOut="A").print() == "MOV A, 0"
    # assert SUB(reg1="B", reg2="A", regOut="B").print() == "MOV B, 0"
    # assert SUB(reg1="B", reg2="A", regOut="GPR[2]").print() == "MOV B, 0\nMOV GPR[2], B"


def test_valid_subtraction_imm_imm():
    assert SUB(val1=10, val2=2, regOut="A").print() == "MOV A, 10\nMOV B, 2\nSUB A, B\n"
    assert SUB(val1=10, val2=2, regOut="B").print() == "MOV A, 10\nMOV B, 2\nSUB A, B\nMOV B, A"
    assert SUB(val1=10, val2=2, regOut="GPR[1]").print() == "MOV A, 10\nMOV B, 2\nSUB A, B\nMOV B, A\nMOV GPR[1], B"


def test_valid_subtraction_reg_imm():
    assert SUB(reg1="A", val1=2, regOut="GPR[1]").print() == "MOV B, 2\nSUB A, B\nMOV B, A\nMOV GPR[1], B"
    assert SUB(reg1="B", val1=2, regOut="GPR[1]").print() == "MOV A, B\nMOV B, 2\nSUB A, B\nMOV B, A\nMOV GPR[1], B"
    assert SUB(reg1="GPR[2]", val1=2,
               regOut="GPR[1]").print() == "MOV B, GPR[2]\nMOV A, B\nMOV B, 2\nSUB A, B\nMOV B, A\nMOV GPR[1], B"


def test_invalid_subtraction_construction():
    with pytest.raises(REG_CONSTRUCT_ERROR):
        SUB(reg1="C", reg2="B", regOut="GPR[0]")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        SUB(reg1="A", reg2="C", regOut="GPR[0]")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        SUB(reg1="A", reg2="GPR[1]", regOut="GPR[16]")
    with pytest.raises(REG_CONSTRUCT_ERROR):
        SUB(reg1="A", reg2="GPR[2]", regOut="C")
    with pytest.raises(OPERATOR_CONSTRUCT_ERROR):
        SUB(reg1="A", reg2="B")
    with pytest.raises(OPERATOR_CONSTRUCT_ERROR):
        SUB()
    with pytest.raises(OPERATOR_CONSTRUCT_ERROR):
        SUB(regOut="B")
        SUB()
    with pytest.raises(OPERATOR_CONSTRUCT_ERROR):
        SUB(reg1="A", regOut="B")


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
    with pytest.raises(REG_DECLARATION_ERROR):
        SUB(val1=10, val2=2, regOut="IN")
    with pytest.raises(IMM_CONSTRUCT_ERROR):
        SUB(val1=16, val2=2, regOut="GPR[0]")
    with pytest.raises(IMM_CONSTRUCT_ERROR):
        SUB(val1=10, val2=16, regOut="GPR[0]")
