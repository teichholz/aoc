from helpers import readday
from dataclasses import dataclass
import re

lines = readday(17, 2024, example=False).strip()

@dataclass
class Machine:
    regs: dict[str, int]
    prog: list["OP"]
    out: list[int]
    instr: int

    jumped: bool = False

    def exe(self):
        self.out = []
        while self.instr < len(self.prog):
            self.prog[self.instr].exe(self)
            print(self)
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
        num, denom = mach.regs["A"], 2 ** self.combo(regs)
        mach.regs["A"] = num // denom

class BXL(OP):
    def exe(self, mach: Machine):
        mach.regs["B"] = mach.regs["B"] ^ self.operand

class BST(OP):
    def exe(self, mach: Machine):
        mach.regs["B"] = self.combo(mach.regs) & 7

class JNZ(OP):
    def exe(self, mach: Machine):
        if mach.regs["A"] == 0:
            return
        else:
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
        num, denom = mach.regs["A"], 2 ** self.combo(regs)
        mach.regs["B"] = num // denom

class CDV(OP):
    def exe(self, mach: Machine):
        num, denom = mach.regs["A"], 2 ** self.combo(regs)
        mach.regs["C"] = num // denom

def parse():
    regs, prog = lines.split("\n\n")
    a, b, c = map(int, re.findall(r"\d+", regs))
    prog = list(map(int, re.findall(r"\d+", prog)))
    return {"A": a, "B": b, "C": c}, prog


regs, prog = parse()

def part1():
    opcodes = prog[::2]
    operands = prog[::-2][::-1]
    instrs = [op(operand) for op, operand in zip(map(op, opcodes), operands)]
    machine = Machine(dict(regs), instrs, [], 0)
    print(machine)
    # machine.exe()

    # return ",".join(map(str, machine.out))

def op(opcode: int):
    mapping = {0: ADV, 1: BXL, 2: BST, 3: JNZ, 4: BXC, 5: OUT, 6: BDV, 7: CDV}
    return mapping[opcode]

def part2():
    pass
