from dataclasses import dataclass
from typing import ForwardRef

from helpers import profiler, readday

input = readday(24, 2024, example=False).strip()


@dataclass(frozen=True)
class Gate:
    in1: str
    in2: str
    op: str
    out: str

    def calc(self, vals: dict[str, bool]):
        b1 = vals[self.in1]
        b2 = vals[self.in2]

        match self.op:
            case "AND":
                vals[self.out] = b1 and b2
            case "OR":
                vals[self.out] = b1 or b2
            case "XOR":
                vals[self.out] = b1 ^ b2


def parse():
    seen, left = input.split("\n\n")
    wires = dict()
    for wire in seen.split("\n"):
        name, val = wire.split(": ")
        wires[name] = bool(int(val))
    gates = set()
    for gate in left.split("\n"):
        op, out = gate.split(" -> ")
        in1, op, in2 = op.split(" ")
        gates.add(Gate(in1, in2, op, out))
    return wires, gates


@profiler
def part1():
    wires, gates = parse()
    while gates:
        to_remove = set()
        for gate in gates:
            if gate.in1 in wires and gate.in2 in wires:
                gate.calc(wires)
                to_remove.add(gate)
        gates -= to_remove

    ks = [wire for wire in wires.keys() if wire.startswith("z")]
    ks.sort()
    is_ = reversed([str(int(wires[k])) for k in ks])
    return int("".join(is_), 2)


@profiler
def part2():
    pass
