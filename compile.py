import re


class REGISTER:
    reg: str

    def __init__(self, reg: str):
        self.reg = reg

    def isValidRegName(self):
        regList = ("A", "B", "IN", "OUT")
        if self.reg in regList:
            return True
        if self.reg[0:3] == "GPR":
            match1 = re.search("GPR\[[0-9]\]", self.reg, re.I)
            match2 = re.search("GPR\[1[0-5]\]", self.reg, re.I)
            if match1 or match2:
                return True
        return False


def LET(reg, imm):
    pass

