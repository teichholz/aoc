from helpers import readday
from dataclasses import dataclass
import re
import signal
import sys

lines = readday(17, 2024, example=False).strip()

@dataclass
class Machine:
    regs: dict[str, int]
    prog: list["OP"]

    out: list[int]
    instr: int
    jumped: bool

    def exe(self):
        self.out = []
        while self.instr < len(self.prog):
            self.prog[self.instr].exe(self)
            if self.jumped:
                self.jumped = False
            else:
                self.instr += 1

@dataclass
class OP:
    operand: int

    def combo(self, regs):
        match self.operand:
            case 0 | 1 | 2 | 3:
                return self.operand
            case 4:
                return regs['A']
            case 5:
                return regs['B']
            case 6:
                return regs['C']
            case 7:
                raise ValueError("Invalid operand: Operand 7 is reserved and cannot be used.")
            case _:
                raise ValueError(f"Invalid operand value: {self.operand}")

    def exe(self, mach: Machine):
        pass

class ADV(OP):
    def exe(self, mach: Machine):
        num, denom = mach.regs["A"], 2 ** self.combo(mach.regs)
        mach.regs["A"] = num // denom

class BXL(OP):
    def exe(self, mach: Machine):
        mach.regs["B"] = mach.regs["B"] ^ self.operand

class BST(OP):
    def exe(self, mach: Machine):
        mach.regs["B"] = self.combo(mach.regs) & 7

class JNZ(OP):
    def exe(self, mach: Machine):
        if mach.regs["A"] != 0:
            mach.jumped = True
            mach.instr = self.operand // 2

class BXC(OP):
    def exe(self, mach: Machine):
        mach.regs["B"] = mach.regs["B"] ^ mach.regs["C"]

class OUT(OP):
    def exe(self, mach: Machine):
        mach.out += [self.combo(mach.regs) & 7]

class BDV(OP):
    def exe(self, mach: Machine):
        num, denom = mach.regs["A"], 2 ** self.combo(mach.regs)
        mach.regs["B"] = num // denom

class CDV(OP):
    def exe(self, mach: Machine):
        num, denom = mach.regs["A"], 2 ** self.combo(mach.regs)
        mach.regs["C"] = num // denom

def parse():
    regs, prog = lines.split("\n\n")
    a, b, c = map(int, re.findall(r"\d+", regs))
    prog = list(map(int, re.findall(r"\d+", prog)))
    return {"A": a, "B": b, "C": c}, prog


def part1():
    regs, prog = parse()
    opcodes = prog[::2]
    operands = prog[::-2][::-1]
    instrs = [op(operand) for op, operand in zip(map(op, opcodes), operands)]
    machine = Machine(dict(regs), instrs, [], 0, False)
    print(machine)
    machine.exe()

    return ",".join(map(str, machine.out))

def op(opcode: int):
    mapping = {0: ADV, 1: BXL, 2: BST, 3: JNZ, 4: BXC, 5: OUT, 6: BDV, 7: CDV}
    return mapping[opcode]

def part2():
    """
    Considering the Machine:
    Machine(regs={'A': x, 'B': 0, 'C': 0},
            prog=[BST(operand=4), BXL(operand=1), CDV(operand=5), BXL(operand=5), BXC(operand=0), OUT(operand=5), ADV(operand=3), JNZ(operand=0)],
            out=[],
            instr=0,
            jumped=False)
    Opcode effects:[B=A&7, B=B^1, C=A//2**B, B=B^5, B=B^C, out+=[B&7],A=A//8, jump start A!=0]
    inlined effects: [B=(((A&7)^1)^5)^(A//2**((A&7)^1), out+=[B&7],A=A//8, jump start A!=0]
    1=b0000'0001
    5=b0000'0101
    7=b0000'0111
    We need: 2,4,1,1,7,5,1,5,4,0,5,5,0,3,3,0  len=16
    We can make the following observations:
    - A must start with the lowest possible value
    - We must end in A=0, so that we do not jump with JNZ
    - OUT will be called len(out) times and so B (combo operand 5) must contain the value 'whatever & opcode' or 'whatever % 8 = opcode'
    - the longest path from start to end is len(opcodes) * len(out). Every iteration outputs the corresponding opcode / operand of the program.
    - B and C will be overwritten in the second and third step, so their value in each iteration solely depends on the value of A
    - In order to output 16 times we need to repeat 15 times, A must be dividable by 8 15 times. That is A >= 8 ** 15
    - Dividing by multiples of 2 is the same as >>
    """
    pass

def generate_output(A, target):
    inc = 0
    while A != 0:
        B = A & 7

        B ^= 1

        C = A >> (2 ** B)

        B ^= 5

        B ^= C

        result = B & 7
        if result != target[inc]:
            return False

        A = A >> 8

        inc += 1

    return True


target_output = [2, 4, 1, 1, 7, 5, 1, 5, 4, 0, 5, 5, 0, 3, 3, 0]

A = 35188651556392
def find_A_for_output(target_output):
    # 8 ** 15 <= A < 8 ** 16
    global A
    while True:
        same = generate_output(A, target_output)
        if same:
            return A
        A += 1

def signal_handler(sig, frame):
    print(f"SIGINT received! A is {A}")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
