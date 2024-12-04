import helpers as h

input = h.readdaylines(4, 2024, example=False)

def part1():
    word = "XMAS"

    sum = 0
    for i in range(len(input)):
        for j in range(len(input[i])):
            for dir in h.dirs8:
                sum += search(input, word, (i, j), dir)

    return sum

def search(puzzle: list[str], word: str, pos: (int, int), dir: (int, int), depth=0) -> int:
    found = 0
    row, col = pos
    drow, dcol = dir

    if (not 0 <= row < len(puzzle) or not 0 <= col < len(puzzle[0])):
        return 0

    if depth >= len(word):
        return 0

    if puzzle[row][col] == word[depth] and depth == len(word) - 1:
        return 1

    if puzzle[row][col] == word[depth]:
        found += search(puzzle, word, (row + drow, col + dcol), dir, depth + 1)

    return found


def part2():
    sum = 0
    for row in range(1, len(input) - 1):
        for col in range(1, len(input[row]) - 1):
            if input[row][col] == "A":
                diag1 = {input[row - 1][col - 1], input[row + 1][col + 1]}
                diag2 = {input[row + 1][col - 1], input[row - 1][col + 1]}
                if diag1 == {"M", "S"} and diag2 == {"M", "S"}:
                    sum += 1
    return sum
