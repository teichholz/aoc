import helpers as h
import itertools as i

ms = [line for line in h.readdaylines(21, 2022)]

def add(d: dict, line: str):
    match line.split():
        case [name, n1, op, n2]:
            d[name[:-1]] = (n1, op, n2)
        case [name, n]:
            d[name[:-1]] = int(n)
    return d
msd = list(i.accumulate(ms, add, initial={}))[-1]

def p1(n: str = 'root'):
    if isinstance(msd[n], int):
        return msd[n]
    else:
        n1, op, n2 = msd[n]
        return int(eval(f"({p1(n1)} {op} {p1(n2)})"))
print(p1())

# part 2
n1, _, n2 = msd['root']
print(n1, n2) # n1 = n2 is what we want to solve for
print(p1(n1), p1(n2))

msd['humn'] = 3509819803065

n1, _, n2 = msd['root']
print(n1, n2) # n1 = n2 is what we want to solve for
print(p1(n1), p1(n2))

def solveforhumn():
    """
    Solves the equality equation for humn\n
    How to handle non commutative operators like / and - ?
    ---
     10 / x = 5 should become x = 10 / 5
    ---
     5 - x = 10 should become x = 5 - 10
    """
    n1, _, n2 = msd['root']
    right = p1(n2) 
    path = findPathTo('humn')[1:] # i know humn is in my left tree so I cheat

    n = n1
    for goLeft in path:
        n1, op, n2 = msd[n]
        if (goLeft):
            n = n1
            right = int(eval(f"(right {inverse(op)} {p1(n2)})"))
        else:
            n = n2
            # we need to be smart here and be aware of non commutative operators like - and /
            if (iscommutative(op)):
                right = int(eval(f"(right {inverse(op)} {p1(n1)})"))
            else:
                right = int(eval(f"({p1(n1)} {op} right)")) 
        
    return right

def iscommutative(op: str):
    return op in ['+', '*']

def inverse(op: str):
    if (op == '+'): return '-'
    elif (op == '-'): return '+'
    elif (op == '*'): return '/'
    elif (op == '/'): return '*'

def findPathTo(s: str, root: str = 'root'):
    """
    Find the path to a specific node. A path is either left or right (1, 0 / true, false)
    """
    if (s == root): return []
    for k, v in msd.items():
        if (isinstance(v, int)):
            continue

        n1, _, n2 = v

        if (n1 == s):
            return findPathTo(k) + [True]
        elif (n2 == s):
            return findPathTo(k) + [False]