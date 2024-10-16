from helpers import readdaylines, cycle
from functools import reduce
import re

def parse(line):
    lhs, rhs = line.split(' -> ')
    fr = lhs
    to = re.findall(r'\w+', rhs)
    return (fr, to)
input = [parse(line) for line in readdaylines(20, 2023, example=False)]

LO, HI = 0, 1
class Mod:
    def __init__(self, name):
        self.receivers = []
        self.name = name
    
    @staticmethod
    def new(name):
        if (name[0] == '%'):
            return FlipFlop(name[1:])
        elif (name[0] == '&'):
            return Conjunction(name[1:])
        else:
            return Broadcast(name)
        
    def addreceiver(self, receiver):
        receiver.notifyadded(self)
        self.receivers.append(receiver)
        
    def pulse(self, pulse):
        return [*zip(cycle([pulse]), self.receivers)]
    
    def noop(self):
        return []

    def notifyadded(self, sender):
        pass
    
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        t = type(self)
        return f'{self.name} ({t.__name__})'

class Broadcast(Mod):
    def receive(self, sender, pulse):
        return self.pulse(pulse)

class FlipFlop(Mod):
    def __init__(self, name):
        super().__init__(name)
        self.state = False

    def receive(self, sender, pulse):
        if pulse == LO:
            self.state = not self.state
            return self.pulse(self.state)
        return self.noop()

class Conjunction(Mod):
    def __init__(self, name):
        super().__init__(name)
        self.memory = {} 

    def notifyadded(self, sender):
        self.memory[sender.name] = False

    def receive(self, sender, pulse):
        self.memory[sender] = pulse
        return self.pulse(not all(self.memory.values()))
        
class Noop(Mod):
    def receive(self, _, __):
        return self.noop()

def extractname(name): return re.findall(r'\w+', name)[0]
receivers = {extractname(k): v for k, v in input}
mods = {extractname(k): Mod.new(k) for k, _ in input}

for k, v in receivers.items():
    for r in v:
        if (r in mods):
            mods[k].addreceiver(mods[r])
        else:
            mods[k].addreceiver(Noop(r))

CYCLES = 1000000000
def part1():
    los, his = 0, 0
    for cycle in range(1, CYCLES+1):
        q = [(0, 'Button', mods['broadcaster'])] # pulse, from (name), to (mod)
        while q:
            pulse, frommodname, tomod = q.pop(0)
            # print(f'{frommodname} -> {tomod.name} ({int(pulse)})')
            los += pulse == LO
            his += pulse == HI
            for pulse, totomod in tomod.receive(frommodname, pulse):
                q.append((pulse, tomod.name, totomod))

    return (los, his, los * his)

            