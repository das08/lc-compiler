from lccompiler.models import REGISTER, IMM
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR
from lccompiler.declare_var import LET
from lccompiler.substitute import PUT


class SUB:
    reg1: REGISTER
    reg2: REGISTER
    val1: IMM
    val2: IMM
    regOut: REGISTER

    def __init__(self, reg1: str = None, reg2: str = None, val1: int = None, val2: int = None, regOut: str = None):
        """
        引き算: regOUT = reg2 - reg1
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
                raise REG_CONSTRUCT_ERROR("Invalid RegisterOUT Name.")
            if not regOut:
                raise REG_CONSTRUCT_ERROR("You must specify RegisterOUT")
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
            if self.reg1.reg == "A":
                if self.reg2.reg == "A":
                    return LET(self.regOut.reg, 0).print()
                if self.reg2.reg == "B":
                    return "SUB A, B\n" + PUT(self.regOut.reg, "A").print()
                if self.reg2.isGPR():
                    return "MOV B, {0}\nSUB A, B\n".format(self.reg2.reg) + PUT(self.regOut.reg, "A").print()
            if self.reg1.reg == "B":
                if self.reg2.reg == "A":
                    return "MOV GPR[15], B\nMOV B, A\nMOV A, GPR[15]\nSUB A, B\n" + PUT(self.regOut.reg, "A").print()
                if self.reg2.reg == "B":
                    return LET(self.regOut.reg, 0).print()
                if self.reg2.isGPR():
                    return "MOV GPR[15], B\nMOV B, {0}\nMOV A, GPR[15]\nSUB A, B\n".format(self.reg2.reg) + PUT(self.regOut.reg, "A").print()
            if self.reg1.isGPR():
                if self.reg2.reg == "A":
                    return "MOV B, A\nMOV GPR[15], B\nMOV B, {0}\nMOV A, B\nMOV B, GPR[15]\nSUB A, B\n".format(self.reg1.reg) + PUT(self.regOut.reg, "A").print()
                if self.reg2.reg == "B":
                    return "MOV GPR[15], B\nMOV B, {0}\nMOV A, B\nMOV B, GPR[15]\nSUB A, B\n".format(self.reg1.reg) + PUT(self.regOut.reg, "A").print()
                if self.reg2.isGPR():
                    return "MOV B, {0}\nMOV GPR[15], B\nMOV B, {1}\nMOV A, B\nMOV B, GPR[15]\nSUB A, B\n".format(self.reg2.reg, self.reg1.reg) + PUT(self.regOut.reg, "A").print()

    def __repr__(self):
        return self.print()
