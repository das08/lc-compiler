from lccompiler.models import REGISTER, IMM
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR


class SUB:
    reg1: REGISTER
    reg2: REGISTER
    val1: IMM
    val2: IMM
    regOut: REGISTER

    def __init__(self, reg1: str = None, reg2: str = None, val1: int = None, val2: int = None, regOut: str = None):
        """
        引き算
        :param reg1: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param reg2: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param val1: (int) 0 ~ 15 Value
        :param val2: (int) 0 ~ 15 Value
        :param regOut: (str) "A" | "B" | "GPR[0] ~ GPR[15]" Register
        """
        # レジスタ同士の引き算
        if reg1 and reg2:
            if not REGISTER(reg1).isValidRegName():
                raise REG_CONSTRUCT_ERROR("Invalid Register1 Name.")
            if not REGISTER(reg2).isValidRegName():
                raise REG_CONSTRUCT_ERROR("Invalid Register2 Name.")
            if not REGISTER(regOut).isValidRegName():
                raise REG_CONSTRUCT_ERROR("Invalid Register2 Name.")
            validReg = ("A", "B")
            if not (REGISTER(reg1).reg in validReg or REGISTER(reg1).isGPR()):
                raise REG_DECLARATION_ERROR("Cannot use {0} reg for subtraction.".format(reg1))
            if not (REGISTER(reg2).reg in validReg or REGISTER(reg2).isGPR()):
                raise REG_DECLARATION_ERROR("Cannot use {0} reg for subtraction.".format(reg2))
            if not (REGISTER(regOut).reg in validReg or REGISTER(regOut).isGPR()):
                raise REG_DECLARATION_ERROR("Cannot use {0} reg for subtraction.".format(regOut))
            if REGISTER(reg1).isGPR() and REGISTER(reg1).reg == "GPR[15]":
                raise REG_DECLARATION_ERROR("Cannot use GPR[15]reg.")
            if REGISTER(reg2).isGPR() and REGISTER(reg2).reg == "GPR[15]":
                raise REG_DECLARATION_ERROR("Cannot use GPR[15]reg.")

            self.reg1 = REGISTER(reg1)
            self.reg2 = REGISTER(reg2)
            self.regOut = REGISTER(regOut)

    def isRegReg(self):
        return self.reg1 and self.reg2

    def print(self):
        # レジスタ同士の引き算
        if self.isRegReg():
            if self.reg1.reg == "A" and self.reg2.reg == "B": return "SUB A, B\nMOV B, A"
            if self.reg1.reg == "B" and self.reg2.reg == "B": return "MOV B, 0"
            if self.reg1.isGPR() and self.reg2.reg == "B": return "MOV B, {0}\nMOV A, B\n"

    def __repr__(self):
        return self.print()
