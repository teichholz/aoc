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
print(p1('root'))

# part 2
n1, _, n2 = msd['root']
print(n1, n2) # n1 = n2 is what we want to solve for
print(p1(n1), p1(n2))

msd['humn'] = 9141913668089

# 9141913668089 is too high
# solves the equality equation for humn
def solveForHumn():
    n1, _, n2 = msd['root']
    right = p1(n2) 
    path = findPathTo('humn')[1:] # i know humn is in my left tree so I cheat

    n = n1
    tr = None # node to take on the other side of the equation
    for goLeft in path:
        n1, op, n2 = msd[n]
        if (goLeft):
            n = n1
            tr = n2
        else:
            n = n2
            tr = n1
        right = eval(f"(right {inverse(op)} {p1(tr)})")
    return right

def inverse(op: str):
    if (op == '+'): return '-'
    elif (op == '-'): return '+'
    elif (op == '*'): return '/'
    elif (op == '/'): return '*'


# quick check if my path works
def followPath(ps: list[bool], root: str = 'root'):
    n = root
    for goLeft in ps:
        if (goLeft):
            n1, _, _ = msd[n]
            n = n1
        else:
            _, _, n2 = msd[n]
            n = n2
    return n

# find the path to a specific node. A path is either left or right (1, 0 / true, false)
# we do this bottom up
def findPathTo(s: str, root: str = 'root'):
    if (s == root): return []
    for k, v in msd.items():
        if (isinstance(v, int)):
            continue

        n1, _, n2 = v

        if (n1 == s):
            return findPathTo(k) + [True]
        elif (n2 == s):
            return findPathTo(k) + [False]
    
# finds occurences of s in m in regard to msd
# humn appears once in the left side of my tree
def findOccurences(s: str, root: str = 'root'):
    if (isinstance(msd[root], int)):
        return 0

    n1, _, n2 = msd[root]

    if (n1 == s):
        return 1 + findOccurences(s, n2)
    elif (n2 == s):
        return 1 + findOccurences(s, n1)
    else:
        return findOccurences(s, n1) + findOccurences(s, n2)