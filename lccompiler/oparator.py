from lccompiler.models import REGISTER, IMM
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR, OPERATOR_CONSTRUCT_ERROR


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
