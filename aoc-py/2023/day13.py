from helpers import readday, transpose

input = [line.splitlines() for line in readday(13, 2023, example=False).split('\n\n')]
        
def bin(line):
    return ''.join(['1' if c == '#' else '0' for c in line])

def find(input):
    W = len(input)
    input = [bin(line) for line in input]
    for i in range(1, W):
        size = min(i, W - i)
        l = int(''.join([*reversed(input[i - size:i])]), 2)
        r = int(''.join(input[i:i + size]), 2)
        xor = l ^ r
        # use simple equality of l and r for part 1
        if (xor != 0 and xor & (xor - 1) == 0):
            # we know that each smudge causes another reflection to exist
            # so this checks, if xor has exactly one bit set
            return i
    return 0
        
def part():
    sum = 0
    for _, grid in enumerate(input):
        tgrid = transpose(grid)
        hor = find(grid)
        vert = find(tgrid)
        sum += 100 * hor + vert
    
    return sum