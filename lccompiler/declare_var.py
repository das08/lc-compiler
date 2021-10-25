from lccompiler.models import REGISTER, IMM
from lccompiler.errors import REG_CONSTRUCT_ERROR, REG_DECLARATION_ERROR, IMM_CONSTRUCT_ERROR


class LET:
    reg: REGISTER
    imm: IMM

    def __init__(self, reg: str, imm: int):
        if not REGISTER(reg).isValidRegName():
            raise REG_CONSTRUCT_ERROR("Invalid Register Name.")
        if not IMM(imm).isValidImm():
            raise IMM_CONSTRUCT_ERROR("Invalid Immediate Value.")
        if REGISTER(reg).reg == REGISTER("IN").reg:
            raise REG_DECLARATION_ERROR("Cannot use IN reg for declaration.")
        self.reg = REGISTER(reg)
        self.imm = IMM(imm)

    def print(self):
        normalReg = ("A", "B", "OUT")
        if self.reg.reg in normalReg:
            return "MOV {0}, {1}".format(self.reg.reg, self.imm.imm)
        if self.reg.isGPR():
            return "MOV B, {0}\nMOV {1}, B".format(self.imm.imm, self.reg.reg)

    def __repr__(self):
        return self.print()
