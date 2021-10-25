import re


class REGISTER:
    reg: str

    def __init__(self, reg: str):
        self.reg = reg

    def isValidRegName(self):
        regList = ("A", "B", "IN", "OUT")
        if self.reg in regList:
            return True
        if self.isGPR():
            return True
        return False

    def isGPR(self):
        if self.reg[0:3] == "GPR":
            match1 = re.search("GPR\[[0-9]\]", self.reg, re.I)
            match2 = re.search("GPR\[1[0-5]\]", self.reg, re.I)
            if match1 or match2:
                return True
        return False


class IMM:
    imm: int

    def __init__(self, imm: int):
        self.imm = imm

    def isValidImm(self):
        return 0 <= self.imm < 16
