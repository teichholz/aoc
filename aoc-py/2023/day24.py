import helpers as h
from z3 import Real, solve, Solver, sat

# Create a dictionary that maps string representation of numbers to their numeric values
lines = h.readdaylines(24, 2023, example=True)

def parse(lines):
    ls = []
    for line in lines:
        pos, dir = line.split(" @ ")
        x, y, z = list(map(int, pos.split(", ")))
        vx, vy, vz = list(map(int, dir.split(", ")))
        ls.append(((x, y, z), (vx, vy, vz)))
    return ls


def lin_funs(lines):
    ls = []
    for pos, vel in lines:
        x = Real('x')
        m = (vel[1] / vel[0])  # dy / dx
        n = pos[1] - m * pos[0]  # y1 - m * x1
        ls.append(x * (vel[1] / vel[0]) + n)  # x * m + n
    return ls


least = 200000000000000
most = 400000000000000
def p1():
    intersections = 0
    fs = lin_funs(parse(lines))
    for i, f in enumerate(fs):
        for f2 in fs[i:]:
            s = Solver()
            s.add(f == f2)
            if s.check() == sat:
                m = s.model()

                x = m[Real('x')]
                y = m.evaluate(f)
                print(x)
                print(y)

                if x >= least and x <= most and y >= least and y <= most:
                    intersections = intersections + 1

    print(intersections)
