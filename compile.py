import re

from lccompiler.declare_var import LET
from lccompiler.substitute import PUT
from lccompiler.addition import ADD
from lccompiler.subtraction import SUB
from lccompiler.multiplication import MULT
from lccompiler.errors import OPERATOR_CONSTRUCT_ERROR

code = """
LET GPR[0] 0
LET GPR[2] 0
PUT A GPR[2]
ADD 2 4 GPR[0]
ADD A 4 GPR[0]
ADD A GPR[2] GPR[0]
SUB 2 4 GPR[0]
SUB A 4 GPR[0]
SUB A GPR[2] GPR[0]
MULT 2 4 GPR[0]
MULT A 4 GPR[0]
MULT A GPR[2] GPR[0]
"""


def loadOp(fileName: str):
    codes = []
    file = open(fileName)
    for f in file:
        codes.append(f.rstrip('\n'))
    return codes


def compileFromFile(codes: list, readable=False):
    res = []
    for c in codes:
        if c == "": continue
        op = c.split(" ")
        if op[0] == "LET":
            if len(op) != 3: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            res.append(LET(reg=op[1], imm=int(op[2])).print())
        elif op[0] == "PUT":
            if len(op) != 3: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            res.append(PUT(reg1=op[1], reg2=op[2]).print())
        elif op[0] == "ADD":
            if len(op) != 4: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            if op[1].isdecimal() and op[2].isdecimal():
                res.append(ADD(val1=int(op[1]), val2=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and op[2].isdecimal():
                res.append(ADD(reg1=op[1], val1=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and not op[2].isdecimal():
                res.append(ADD(reg1=op[1], reg2=op[2], regOut=op[3]).print())
        elif op[0] == "SUB":
            if len(op) != 4: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            if op[1].isdecimal() and op[2].isdecimal():
                res.append(SUB(val1=int(op[1]), val2=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and op[2].isdecimal():
                res.append(SUB(reg1=op[1], val1=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and not op[2].isdecimal():
                res.append(SUB(reg1=op[1], reg2=op[2], regOut=op[3]).print())
            else:
                raise OPERATOR_CONSTRUCT_ERROR("Invalid assignment of argument(s)")
        elif op[0] == "MULT":
            if len(op) != 4: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            if op[1].isdecimal() and op[2].isdecimal():
                res.append(MULT(val1=int(op[1]), val2=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and op[2].isdecimal():
                res.append(MULT(reg1=op[1], val1=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and not op[2].isdecimal():
                res.append(MULT(reg1=op[1], reg2=op[2], regOut=op[3]).print())
            else:
                raise OPERATOR_CONSTRUCT_ERROR("Invalid assignment of argument(s)")
        else:
            raise OPERATOR_CONSTRUCT_ERROR("Invalid operand.")


    # 細分化する
    opList = []
    for r in res:
        if readable:print(r)
        opList.extend(r.splitlines())

    if not readable:
        for i, r in enumerate(opList):
            # print("{:03d}: ".format(i), end='')
            # 0000
            if re.match("MOV A, (?:[023456789]|1[012345]?)", r):
                print('{:01x}{:01x}'.format(0x0, int(r.split(" ")[2])))
            # 0001
            if re.match("ADD A, (?:[023456789]|1[012345]?)", r):
                print('{:01x}{:01x}'.format(0x1, int(r.split(" ")[2])))
            # 0010
            if re.match("MOV A, B", r):
                print('{:01x}{:01x}'.format(0x2, 0x0))
            # 0011
            if re.match("MOV A, IN", r):
                print('{:01x}{:01x}'.format(0x3, 0x0))
            # 0100
            if re.match("MOV B, (?:[023456789]|1[012345]?)", r):
                print('{:01x}{:01x}'.format(0x4, int(r.split(" ")[2])))
            # 0101
            if re.match("ADD B, (?:[023456789]|1[012345]?)", r):
                print('{:01x}{:01x}'.format(0x5, int(r.split(" ")[2])))
            # 0110
            if re.match("MOV B, A", r):
                print('{:01x}{:01x}'.format(0x6, 0x0))
            # 0111
            if re.match("MOV B, IN", r):
                print('{:01x}{:01x}'.format(0x7, 0x0))
            # 1000
            if re.match("MOV OUT, (?:[023456789]|1[012345]?)", r):
                print('{:01x}{:01x}'.format(0x8, int(r.split(" ")[2])))
            # 1001
            if re.match("MOV OUT, B", r):
                print('{:01x}{:01x}'.format(0x9, 0x0))
            # 1010
            if re.match("MOV B, GPR\[(?:[023456789]|1[012345]?)\]", r):
                print('{:01x}{:01x}'.format(0xa, int(re.match("GPR\[([0-9]+)\]", r.split(" ")[2]).group(1))))
            # 1011
            if re.match("MOV GPR\[(?:[023456789]|1[012345]?)\], B", r):
                print('{:01x}{:01x}'.format(0xb, int(re.match("GPR\[([0-9]+)\]", r.split(" ")[1]).group(1))))
            # 1100
            if re.match("SUB A, B", r):
                print('{:01x}{:01x}'.format(0xc, 0x0))
            # 1101
            if re.match("MULT A, B", r):
                print('{:01x}{:01x}'.format(0xd, 0x0))
            # 1110
            if re.match("JNC (?:[023456789]|1[012345]?)", r):
                print('{:01x}{:01x}'.format(0xe, int(r.split(" ")[1])))
            # 1111
            if re.match("JMP (?:[023456789]|1[012345]?)", r):
                print('{:01x}{:01x}'.format(0xf, int(r.split(" ")[1])))


compileFromFile(loadOp("./example/sample.das"), True)
