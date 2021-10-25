OP = {
    "0000": "MOV A, {0}(0x{1})",
    "0001": "ADD A, {0}(0x{1})",
    "0010": "MOV A, B",
    "0011": "MOV A, IN",
    "0100": "MOV B, {0}(0x{1})",
    "0101": "ADD B, {0}(0x{1})",
    "0110": "MOV B, A",
    "0111": "MOV B, IN",
    "1000": "MOV OUT, {0}(0x{1})",
    "1001": "MOV OUT, B",
    "1010": "MOV B, GPR[{0}]",
    "1011": "MOV GPR[{0}], B",
    "1100": "SUB A, B",
    "1101": "MULT A, B",
    "1110": "JNC {0}(0x{1})",
    "1111": "JMP {0}(0x{1})"
}


def convertFromHex(codes: list):
    for i in range(len(codes)):
        code = codes[i]
        opcode = '{:04b}'.format(int(code[0], 16))
        print(OP[opcode].format(int(code[1], 16), code[1]))
    return


def loadHex(fileName: str):
    codes = []
    file = open(fileName)
    for f in file:
        codes.append(f)
    return codes


convertFromHex(loadHex("./example/sample1.hex"))
