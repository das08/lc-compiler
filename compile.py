import re
import argparse

from lccompiler.declare_var import LET
from lccompiler.substitute import PUT
from lccompiler.addition import ADD
from lccompiler.subtraction import SUB
from lccompiler.multiplication import MULT
from lccompiler.shift import LSHIFT
from lccompiler.errors import OPERATOR_CONSTRUCT_ERROR


def loadOp(fileName: str):
    codes = []
    file = open(fileName)
    for f in file:
        codes.append(f.rstrip('\n'))
    return codes


def saveOp(fileName: str, res: list):
    f = open(f"{fileName}.out", 'w')

    f.writelines("\n".join(res))

    f.close()


def compileFromFile(codes: list, ishex=False):
    res = []
    resHex = []
    isLoop = False
    loopCnt = 0
    loopStart = 0
    for c in codes:
        if c == "": continue
        op = c.split(" ")
        if op[0] == "LET" or op[0] == "@":
            if len(op) != 3: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            res.append(LET(reg=op[1], imm=int(op[2])).print())
        elif op[0] == "PUT" or op[0] == "<-":
            if len(op) != 3: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            res.append(PUT(reg1=op[1], reg2=op[2]).print())
        elif op[0] == "ADD" or op[0] == "+":
            if len(op) != 4: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            if op[1].isdecimal() and op[2].isdecimal():
                res.append(ADD(val1=int(op[1]), val2=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and op[2].isdecimal():
                res.append(ADD(reg1=op[1], val1=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and not op[2].isdecimal():
                res.append(ADD(reg1=op[1], reg2=op[2], regOut=op[3]).print())
        elif op[0] == "SUB" or op[0] == "-":
            if len(op) != 4: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            if op[1].isdecimal() and op[2].isdecimal():
                res.append(SUB(val1=int(op[1]), val2=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and op[2].isdecimal():
                res.append(SUB(reg1=op[1], val1=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and not op[2].isdecimal():
                res.append(SUB(reg1=op[1], reg2=op[2], regOut=op[3]).print())
            else:
                raise OPERATOR_CONSTRUCT_ERROR("Invalid assignment of argument(s)")
        elif op[0] == "MULT" or op[0] == "*":
            if len(op) != 4: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            if op[1].isdecimal() and op[2].isdecimal():
                res.append(MULT(val1=int(op[1]), val2=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and op[2].isdecimal():
                res.append(MULT(reg1=op[1], val1=int(op[2]), regOut=op[3]).print())
            elif not op[1].isdecimal() and not op[2].isdecimal():
                res.append(MULT(reg1=op[1], reg2=op[2], regOut=op[3]).print())
            else:
                raise OPERATOR_CONSTRUCT_ERROR("Invalid assignment of argument(s)")
        elif op[0] == "LSH" or op[0] == "<<":
            if len(op) != 4: raise OPERATOR_CONSTRUCT_ERROR("Invalid number of argument(s)")
            res.append(LSHIFT(reg1=op[1], val1=int(op[2]), regOut=op[3]).print())
        elif op[0] == "JMP" or op[0] == "goto":
            imm = int(op[1])
            if imm > 15 or imm < 0: raise Exception("goto address must be 0 ~ 15")
            res.append("JMP {0}".format(imm))
        elif op[0] == "loop":
            isLoop = True
            loopCnt = int(op[1])
            loopStart = len(res)
        elif op[0] == "pool":
            if isLoop:
                tmp = res[loopStart:]
                for i in range(loopCnt - 1):
                    res.extend(tmp)
                isLoop = False
                loopCnt = 0
                loopStart = 0
            else:
                raise Exception("Must designate start of the loop")
        else:
            raise OPERATOR_CONSTRUCT_ERROR("Invalid operand.")

    # 細分化する
    opList = []
    for r in res:
        opList.extend(r.splitlines())

    for i, r in enumerate(opList):
        # print("{:03d}: ".format(i), end='')
        # 0000
        if re.match("MOV A, (?:[023456789]|1[012345]?)", r):
            resHex.append('{:01x}{:01x}'.format(0x0, int(r.split(" ")[2])))
        # 0001
        if re.match("ADD A, (?:[023456789]|1[012345]?)", r):
            resHex.append('{:01x}{:01x}'.format(0x1, int(r.split(" ")[2])))
        # 0010
        if re.match("MOV A, B", r):
            resHex.append('{:01x}{:01x}'.format(0x2, 0x0))
        # 0011
        if re.match("MOV A, IN", r):
            resHex.append('{:01x}{:01x}'.format(0x3, 0x0))
        # 0100
        if re.match("MOV B, (?:[023456789]|1[012345]?)", r):
            resHex.append('{:01x}{:01x}'.format(0x4, int(r.split(" ")[2])))
        # 0101
        if re.match("ADD B, (?:[023456789]|1[012345]?)", r):
            resHex.append('{:01x}{:01x}'.format(0x5, int(r.split(" ")[2])))
        # 0110
        if re.match("MOV B, A", r):
            resHex.append('{:01x}{:01x}'.format(0x6, 0x0))
        # 0111
        if re.match("MOV B, IN", r):
            resHex.append('{:01x}{:01x}'.format(0x7, 0x0))
        # 1000
        if re.match("MOV OUT, (?:[023456789]|1[012345]?)", r):
            resHex.append('{:01x}{:01x}'.format(0x8, int(r.split(" ")[2])))
        # 1001
        if re.match("MOV OUT, B", r):
            resHex.append('{:01x}{:01x}'.format(0x9, 0x0))
        # 1010
        if re.match("MOV B, GPR\[(?:[023456789]|1[012345]?)\]", r):
            resHex.append('{:01x}{:01x}'.format(0xa, int(re.match("GPR\[([0-9]+)\]", r.split(" ")[2]).group(1))))
        # 1011
        if re.match("MOV GPR\[(?:[023456789]|1[012345]?)\], B", r):
            resHex.append('{:01x}{:01x}'.format(0xb, int(re.match("GPR\[([0-9]+)\]", r.split(" ")[1]).group(1))))
        # 1100
        if re.match("SUB A, B", r):
            resHex.append('{:01x}{:01x}'.format(0xc, 0x0))
        # 1101
        if re.match("MULT A, B", r):
            resHex.append('{:01x}{:01x}'.format(0xd, 0x0))
        # 1110
        if re.match("JNC (?:[023456789]|1[012345]?)", r):
            resHex.append('{:01x}{:01x}'.format(0xe, int(r.split(" ")[1])))
        # 1111
        if re.match("JMP (?:[023456789]|1[012345]?)", r):
            resHex.append('{:01x}{:01x}'.format(0xf, int(r.split(" ")[1])))

    if ishex:
        return resHex
    return res


parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
parser.add_argument('--hex', action='store_true')
args = parser.parse_args()

fileName = args.file
ishex = args.hex
res = compileFromFile(loadOp(fileName), ishex)
saveOp(fileName, res)
