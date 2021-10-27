from lccompiler.oparator import OPERATOR
from lccompiler.multiplication import MULT
from lccompiler.errors import IMM_CONSTRUCT_ERROR


class LSHIFT(OPERATOR):
    def __init__(self, reg1: str = None, val1: int = None, regOut: str = None):
        """
        左シフト演算: regOUT = reg1 << val1(shamt)
        :param reg1: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param val1(shamt): (int) 0 ~ 15 Value
        :param regOut: (str) "A" | "B" | "GPR[0] ~ GPR[15]" Register
        """
        if val1 is None or val1 > 3:
            raise IMM_CONSTRUCT_ERROR("Val1(shamt) must be less than 4.")
        super().__init__(reg1=reg1, val1=val1, regOut=regOut)

    def print(self):
        return MULT(reg1=self.reg1.reg, val1=int(pow(2, self.val1.imm)), regOut=self.regOut.reg).print()

    def __repr__(self):
        return self.print()


# print(LSHIFT("A", 3, "B"))
# print(LSHIFT("GPR[2]", 3, "GPR[1]"))
# print(RSHIFT())
