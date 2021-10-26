from lccompiler.oparator import OPERATOR
from lccompiler.declare_var import LET
from lccompiler.substitute import PUT


class MULT(OPERATOR):
    def __init__(self, reg1: str = None, reg2: str = None, val1: int = None, val2: int = None, regOut: str = None):
        """
        掛け算: regOUT[0:4] = reg1 * reg2
        :param reg1: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param reg2: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param val1: (int) 0 ~ 15 Value
        :param val2: (int) 0 ~ 15 Value
        :param regOut: (str) "A" | "B" | "GPR[0] ~ GPR[15]" Register
        """
        super().__init__(reg1, reg2, val1, val2, regOut)

    def print(self):
        # レジスタ同士の掛け算
        if self.isRegReg():
            if self.reg1.reg == "A":
                if self.reg2.reg == "A":
                    return "MOV B, A\nMULT A, B\n" + PUT(self.regOut.reg, "B").print()
                if self.reg2.reg == "B":
                    return "MULT A, B\n" + PUT(self.regOut.reg, "B").print()
                if self.reg2.isGPR():
                    return "MOV B, {0}\nMULT A, B\n".format(self.reg2.reg) + PUT(self.regOut.reg, "B").print()
            if self.reg1.reg == "B":
                if self.reg2.reg == "A":
                    return "MOV GPR[15], B\nMOV B, A\nMOV A, GPR[15]\nMULT A, B\n" + PUT(self.regOut.reg, "B").print()
                if self.reg2.reg == "B":
                    return "MOV A, B\nMULT A, B\n" + PUT(self.regOut.reg, "B").print()
                if self.reg2.isGPR():
                    return "MOV GPR[15], B\nMOV B, {0}\nMOV A, GPR[15]\nMULT A, B\n".format(self.reg2.reg) + PUT(
                        self.regOut.reg, "B").print()
            if self.reg1.isGPR():
                if self.reg2.reg == "A":
                    return "MOV B, A\nMOV GPR[15], B\nMOV B, {0}\nMOV A, B\nMOV B, GPR[15]\nMULT A, B\n".format(
                        self.reg1.reg) + PUT(self.regOut.reg, "B").print()
                if self.reg2.reg == "B":
                    return "MOV GPR[15], B\nMOV B, {0}\nMOV A, B\nMOV B, GPR[15]\nMULT A, B\n".format(
                        self.reg1.reg) + PUT(self.regOut.reg, "B").print()
                if self.reg2.isGPR():
                    return "MOV B, {0}\nMOV GPR[15], B\nMOV B, {1}\nMOV A, B\nMOV B, GPR[15]\nMULT A, B\n".format(
                        self.reg2.reg, self.reg1.reg) + PUT(self.regOut.reg, "B").print()
        if self.isImmImm():
            return "MOV A, {0}\nMOV B, {1}\nMULT A, B\n".format(self.val1.imm, self.val2.imm) + PUT(self.regOut.reg, "B").print()
        if self.isRegImm():
            if self.reg1.reg == "A":
                return "MOV B, {0}\nMULT A, B\n".format(self.val1.imm) + PUT(self.regOut.reg, "B").print()
            if self.reg1.reg == "B":
                return "MOV A, B\nMOV B, {0}\nMULT A, B\n".format(self.val1.imm) + PUT(self.regOut.reg, "B").print()
            if self.reg1.isGPR():
                return "MOV B, {0}\nMOV A, B\nMOV B, {1}\nMULT A, B\n".format(self.reg1.reg, self.val1.imm) + PUT(
                    self.regOut.reg, "B").print()

    def __repr__(self):
        return self.print()


# print(MULT(val1=10, val2=5, regOut="B"))