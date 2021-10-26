from lccompiler.oparator import OPERATOR
from lccompiler.declare_var import LET
from lccompiler.substitute import PUT
from lccompiler.multiplication import MULT


class ADD(OPERATOR):
    def __init__(self, reg1: str = None, reg2: str = None, val1: int = None, val2: int = None, regOut: str = None):
        """
        足し算: regOUT[0:4] = reg1 + reg2
        :param reg1: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param reg2: (str) "A" | "B" | "GPR[0] ~ GPR[14]" Register
        :param val1: (int) 0 ~ 15 Value
        :param val2: (int) 0 ~ 15 Value
        :param regOut: (str) "A" | "B" | "GPR[0] ~ GPR[15]" Register
        """
        super().__init__(reg1, reg2, val1, val2, regOut)

    def print(self):
        # レジスタ同士の足し算
        if self.isRegReg():
            if self.reg1.reg == "A":
                if self.reg2.reg == "A":
                    return MULT(reg1="A", val1=2, regOut=self.regOut.reg).print()
                if self.reg2.reg == "B":
                    return PUT("GPR[15]", "B").print() + "\n" + PUT("GPR[14]", "A").print() + "\nMOV B, GPR[15]\nMOV A, 15\nMULT A, B\nMOV GPR[15], B\n" + PUT("A", "GPR[14]").print() + "\nMOV B, GPR[15]\nSUB A, B\n" + PUT(self.regOut.reg, "A").print()
                if self.reg2.isGPR():
                    return PUT("GPR[15]", "A").print() + "\n" + PUT("GPR[14]", self.reg2.reg).print() + "\nMOV B, GPR[15]\nMOV A, 15\nMULT A, B\nMOV GPR[15], B\n" + PUT("A", "GPR[14]").print() + "\nMOV B, GPR[15]\nSUB A, B\n" + PUT(self.regOut.reg, "A").print()
            if self.reg1.reg == "B":
                if self.reg2.reg == "A":
                    return PUT("GPR[15]", "B").print() + "\n" + PUT("GPR[14]", "A").print() + "\nMOV B, GPR[15]\nMOV A, 15\nMULT A, B\nMOV GPR[15], B\n" + PUT("A", "GPR[14]").print() + "\nMOV B, GPR[15]\nSUB A, B\n" + PUT(self.regOut.reg, "A").print()
                if self.reg2.reg == "B":
                    return MULT(reg1="B", val1=2, regOut=self.regOut.reg).print()
                if self.reg2.isGPR():
                    return "MOV A, B\n" + PUT("GPR[15]", "A").print() + "\n" + PUT("GPR[14]", self.reg2.reg).print() + "\nMOV B, GPR[15]\nMOV A, 15\nMULT A, B\nMOV GPR[15], B\n" + PUT("A", "GPR[14]").print() + "\nMOV B, GPR[15]\nSUB A, B\n" + PUT(self.regOut.reg, "A").print()
            if self.reg1.isGPR():
                if self.reg2.reg == "A":
                    return PUT("GPR[15]", self.reg1.reg).print() + "\n" + PUT("GPR[14]", "A").print() + "\nMOV B, GPR[15]\nMOV A, 15\nMULT A, B\nMOV GPR[15], B\n" + PUT("A", "GPR[14]").print() + "\nMOV B, GPR[15]\nSUB A, B\n" + PUT(self.regOut.reg, "A").print()
                if self.reg2.reg == "B":
                    return PUT("GPR[15]", "B").print() + "\n" + PUT("GPR[14]", self.reg1.reg).print() + "\nMOV B, GPR[15]\nMOV A, 15\nMULT A, B\nMOV GPR[15], B\n" + PUT("A", "GPR[14]").print() + "\nMOV B, GPR[15]\nSUB A, B\n" + PUT(self.regOut.reg, "A").print()
                if self.reg2.isGPR():
                    return PUT("GPR[15]", self.reg1.reg).print() + "\n" + PUT("GPR[14]", self.reg2.reg).print() + "\nMOV B, GPR[15]\nMOV A, 15\nMULT A, B\nMOV GPR[15], B\n" + PUT("A", "GPR[14]").print() + "\nMOV B, GPR[15]\nSUB A, B\n" + PUT(self.regOut.reg, "A").print()
        if self.isImmImm():
            return "MOV A, {0}\nMOV B, 15\nMULT A, B\nMOV A, {1}\nSUB A, B\n".format(self.val2.imm, self.val2.imm) + PUT(self.regOut.reg, "A").print()
        if self.isRegImm():
            if self.reg1.reg == "A":
                return "ADD A, {0}\n".format(self.val1.imm) + PUT(self.regOut.reg, "A").print()
            if self.reg1.reg == "B":
                return "ADD B, {0}\n".format(self.val1.imm) + PUT(self.regOut.reg, "A").print()
            if self.reg1.isGPR():
                return "MOV B, {0}\nADD B, {1}\n".format(self.reg1.reg, self.val1.imm) + PUT(self.regOut.reg, "A").print()

    def __repr__(self):
        return self.print()


# print(ADD(val1=5, val2=3, regOut="GPR[0]"))
# print(ADD(reg1="A", val1=3, regOut="GPR[0]"))
# print(ADD(reg1="GPR[2]", val1=3, regOut="GPR[0]"))
# print(ADD(reg1="A", reg2="A", regOut="GPR[0]"))
# print(ADD(reg1="A", reg2="GPR[1]", regOut="GPR[0]"))
# print(ADD(reg1="GPR[1]", reg2="A", regOut="GPR[0]"))
# print("==== ADD GPR[1], GPR[2] -> GPR[0] ====")
# print(ADD(reg1="GPR[1]", reg2="GPR[2]", regOut="GPR[0]"))
