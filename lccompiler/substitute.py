from lccompiler.models import REGISTER, IMM
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR


class PUT:
    reg1: REGISTER
    reg2: REGISTER

    def __init__(self, reg1: str, reg2: str):
        """
        代入操作: PUT reg2 into reg1
        :param reg1: (str) "A" | "B" | "OUT" | "GPR[0] ~ GPR[15]" Register
        :param reg2: (str) "A" | "B" | "IN" | "GPR[0] ~ GPR[15]" Register
        """
        # レジスタ同士の引き算
        _reg1 = REGISTER(reg1)
        _reg2 = REGISTER(reg2)
        if not _reg1.isValidRegName():
            raise REG_CONSTRUCT_ERROR("Invalid Register1 Name.")
        if not _reg2.isValidRegName():
            raise REG_CONSTRUCT_ERROR("Invalid Register2 Name.")
        validReg = ("A", "B")
        if not (_reg1.reg in validReg or _reg1.isGPR() or _reg1.reg == "OUT"):
            raise REG_DECLARATION_ERROR("Cannot use {0} reg for subtraction.".format(reg1))
        if not (_reg2.reg in validReg or _reg2.isGPR() or _reg2.reg == "IN"):
            raise REG_DECLARATION_ERROR("Cannot use {0} reg for subtraction.".format(reg2))

        self.reg1 = _reg1
        self.reg2 = _reg2

    def print(self):
        if self.reg1.reg == "A":
            if self.reg2.reg == "A":
                return ""
            if self.reg2.reg == "B":
                return "MOV A, B"
            if self.reg2.reg == "IN":
                return "MOV A, IN"
            if self.reg2.isGPR():
                return "MOV B, {0}\nMOV A, B".format(self.reg2.reg)
        if self.reg1.reg == "B":
            if self.reg2.reg == "A":
                return "MOV B, A"
            if self.reg2.reg == "B":
                return ""
            if self.reg2.reg == "IN":
                return "MOV B, IN"
            if self.reg2.isGPR():
                return "MOV B, {0}".format(self.reg2.reg)
        if self.reg1.reg == "OUT":
            if self.reg2.reg == "A":
                return "MOV B, A\nMOV OUT, B"
            if self.reg2.reg == "B":
                return "MOV OUT, B"
            if self.reg2.reg == "IN":
                return "MOV B, IN\nMOV OUT, B"
            if self.reg2.isGPR():
                return "MOV B, {0}\nMOV OUT, B".format(self.reg2.reg)
        if self.reg1.isGPR():
            if self.reg2.reg == "A":
                return "MOV B, A\nMOV {0}, B".format(self.reg1.reg)
            if self.reg2.reg == "B":
                return "MOV {0}, B".format(self.reg1.reg)
            if self.reg2.reg == "IN":
                return "MOV B, IN\nMOV {0}, B".format(self.reg1.reg)
            if self.reg2.isGPR():
                return "MOV B, {0}\nMOV {1}, B".format(self.reg2.reg, self.reg1.reg)

    def __repr__(self):
        return self.print()
