from helpers import readdaylines, dirs4

lines = readdaylines(10, 2024, example=False)
W, H = len(lines[0]), len(lines)
input = {(row, col): int(char) for row, line in enumerate(lines) for col, char in enumerate(line)}
heads = {(row, col) for row, line in enumerate(lines) for col, char in enumerate(line) if char == "0"}

def part1():
    sum = 0
    for head in heads:
        sum += len(set(search(head)))

    return sum

def part2():
    sum = 0
    for head in heads:
        sum += len(search(head))

    return sum

def search(pos: tuple[int, int], elevation=0, seen=set()) -> list[tuple[int, int]]:
    row, col = pos

    if not (0 <= row < H) or not (0 <= col < W):
        return []

    if pos in seen:
        return []

    if input[pos] != elevation:
        return []

    if input[pos] == 9:
        return [pos]

    return [peak for drow, dcol in dirs4 for peak in search((row + drow, col + dcol), elevation + 1, seen | {pos})]
