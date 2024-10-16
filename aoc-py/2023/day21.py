from helpers import readdaylines, dirs
from collections import deque

input = readdaylines(21, 2023, example=True)

def start():
    for row in range(0, len(input)):
        for col in range(0, len(input[row])):
            if input[row][col] == 'S':
                return (row, col) 
    raise Exception('No start found')

ROWS = len(input)
COLS = len(input[0])
MOVES = 1000
def search(input=input, start=start()):
    q = deque([(0, start)])
    moves = set()
    seen = set()
    while q:
        r, cur = q.popleft()
        
        if cur in seen:
            continue

        if r == MOVES:
            moves.add(cur)
            continue

        if (r % 2 == 0):
            moves.add(cur)
        
        # print(r)
        seen.add(cur)

        for dx, dy in dirs:
            row, col = cur[0] + dy, cur[1] + dx

            if (input[row % ROWS][col % COLS] == '#'):
                continue

            q.append((r+1, (row, col)))

    # for row in range(0, len(input)):
    #     for col in range(0, len(input[row])):
    #         if (row, col) in moves:
    #             print('O', end='')
    #         else:
    #             print(input[row][col], end='')
    #     print()
    return (len(moves), moves)