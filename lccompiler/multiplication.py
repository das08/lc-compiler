from lccompiler.oparator import OPERATOR
from lccompiler.declare_var import LET
from lccompiler.substitute import PUT


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
