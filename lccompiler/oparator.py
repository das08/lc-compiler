from lccompiler.models import REGISTER, IMM
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR, OPERATOR_CONSTRUCT_ERROR
from lccompiler.declare_var import LET
from lccompiler.substitute import PUT


class OPERATOR:
    reg1: REGISTER = None
    reg2: REGISTER = None
    val1: IMM = None
    val2: IMM = None
    regOut: REGISTER = None

    def __init__(self, reg1: str = None, reg2: str = None, val1: int = None, val2: int = None, regOut: str = None):
        """
        :param reg1: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param reg2: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param val1: (int) 0 ~ 15 Value
        :param val2: (int) 0 ~ 15 Value
        :param regOut: (str) "A" | "B" | "GPR[0] ~ GPR[15]" Register
        """
        # レジスタ同士の演算
        if reg1 and reg2:
            self.__validateReg(reg1)
            self.__validateReg(reg2)
            self.__validateReg(regOut, True)

            self.reg1 = REGISTER(reg1)
            self.reg2 = REGISTER(reg2)
            self.regOut = REGISTER(regOut)
        # レジスタと数値の演算
        elif reg1 and val1:
            self.__validateReg(reg1)
            self.__validateImm(val1)
            self.__validateReg(regOut, True)

            self.reg1 = REGISTER(reg1)
            self.val1 = IMM(val1)
            self.regOut = REGISTER(regOut)
        # 数値同士の演算
        elif val1 and val2:
            self.__validateImm(val1)
            self.__validateImm(val2)
            self.__validateReg(regOut, True)

            self.val1 = IMM(val1)
            self.val2 = IMM(val2)
            self.regOut = REGISTER(regOut)
        else:
            raise OPERATOR_CONSTRUCT_ERROR("Invalid arguments.")

    @staticmethod
    def __validateReg(reg: str, isRegOut: bool = False):
        validReg = ("A", "B")
        if isRegOut:
            if reg is None:
                raise OPERATOR_CONSTRUCT_ERROR("You must specify RegisterOUT")
            if not REGISTER(reg).isValidRegName():
                raise REG_CONSTRUCT_ERROR("Invalid RegisterOUT Name.")
            if not (REGISTER(reg).reg in validReg or REGISTER(reg).isGPR()):
                raise REG_DECLARATION_ERROR("Cannot use {0} reg for subtraction.".format(reg))
        else:
            if not REGISTER(reg).isValidRegName():
                raise REG_CONSTRUCT_ERROR("Invalid Register1 or Register2 Name.")
            if not (REGISTER(reg).reg in validReg or REGISTER(reg).isGPR()):
                raise REG_DECLARATION_ERROR("Cannot use {0} reg for subtraction.".format(reg))
            if REGISTER(reg).isGPR() and REGISTER(reg).reg == "GPR[15]":
                raise REG_DECLARATION_ERROR("Cannot use GPR[15]reg.")

    @staticmethod
    def __validateImm(val: int):
        if not IMM(val).isValidImm():
            raise IMM_CONSTRUCT_ERROR("Invalid Immediate Value.")

    def isRegReg(self):
        return self.reg1 and self.reg2

    def isRegImm(self):
        return self.reg1 and self.val1

    def isImmImm(self):
        return self.val1 and self.val2


class SUB(OPERATOR):
    def __init__(self, reg1: str = None, reg2: str = None, val1: int = None, val2: int = None, regOut: str = None):
        """
        引き算: regOUT = reg2 - reg1
        :param reg1: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param reg2: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param val1: (int) 0 ~ 15 Value
        :param val2: (int) 0 ~ 15 Value
        :param regOut: (str) "A" | "B" | "GPR[0] ~ GPR[15]" Register
        """
        super().__init__(reg1, reg2, val1, val2, regOut)

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
                    return "MOV GPR[15], B\nMOV B, {0}\nMOV A, GPR[15]\nSUB A, B\n".format(self.reg2.reg) + PUT(
                        self.regOut.reg, "A").print()
            if self.reg1.isGPR():
                if self.reg2.reg == "A":
                    return "MOV B, A\nMOV GPR[15], B\nMOV B, {0}\nMOV A, B\nMOV B, GPR[15]\nSUB A, B\n".format(
                        self.reg1.reg) + PUT(self.regOut.reg, "A").print()
                if self.reg2.reg == "B":
                    return "MOV GPR[15], B\nMOV B, {0}\nMOV A, B\nMOV B, GPR[15]\nSUB A, B\n".format(
                        self.reg1.reg) + PUT(self.regOut.reg, "A").print()
                if self.reg2.isGPR():
                    return "MOV B, {0}\nMOV GPR[15], B\nMOV B, {1}\nMOV A, B\nMOV B, GPR[15]\nSUB A, B\n".format(
                        self.reg2.reg, self.reg1.reg) + PUT(self.regOut.reg, "A").print()

        if self.isImmImm():
            return "MOV A, {0}\nMOV B, {1}\nSUB A, B\n".format(self.val1.imm, self.val2.imm) + PUT(self.regOut.reg, "A").print()

    def __repr__(self):
        return self.print()


class MUL(OPERATOR):
    def __init__(self, reg1: str = None, reg2: str = None, val1: int = None, val2: int = None, regOut: str = None):
        """
        掛け算: regOUT = reg1 * reg2
        :param reg1: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param reg2: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param val1: (int) 0 ~ 15 Value
        :param val2: (int) 0 ~ 15 Value
        :param regOut: (str) "A" | "B" | "GPR[0] ~ GPR[15]" Register
        """
        super().__init__(reg1, reg2, val1, val2, regOut)


# print(SUB(reg1="A", reg2="A", regOut="GPR[1]"))
# print(SUB(reg1="A", reg2="B", regOut="GPR[1]"))
# print(SUB(reg1="A", reg2="GPR[2]", regOut="GPR[1]"))
# print(SUB(reg1="B", reg2="GPR[2]", regOut="GPR[1]"))
# print(SUB(reg1="GPR[3]", reg2="A", regOut="GPR[1]"))
# print(SUB(reg1="GPR[3]", reg2="B", regOut="GPR[1]"))
# print(SUB(reg1="GPR[3]", reg2="GPR[2]", regOut="GPR[1]"))
print(SUB(val1=10, val2=2, regOut="GPR[1]"))
