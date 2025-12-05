import helpers as h

input = h.readdaylines(4, 2025, example=False)


def parse(line: str) -> list[str]:
    return list(line)


def part1():
    parsed = [parse(line) for line in input]

    sum = 0

    for i, row in enumerate(parsed):
        for j, col in enumerate(row):
            neighbours = 0
            if col != "@":
                continue

            for (drow, dcol) in h.dirs8:
                if 0 <= i + drow < len(parsed) and 0 <= j + dcol < len(parsed[i + drow]):
                    if parsed[i + drow][j + dcol] == "@":
                        neighbours += 1

            if neighbours < 4:
                sum += 1


    return sum

def part2():
    parsed = [parse(line) for line in input]

    removed = set()
    could_remove_paper = True

    while could_remove_paper:
        newly_removed = set()
        for i, row in enumerate(parsed):
            for j, col in enumerate(row):
                neighbours = 0
                if col != "@":
                    continue

                for (drow, dcol) in h.dirs8:
                    if 0 <= i + drow < len(parsed) and 0 <= j + dcol < len(parsed[i + drow]):
                        if parsed[i + drow][j + dcol] == "@":
                            neighbours += 1

                if neighbours < 4:
                    newly_removed.add((i, j))

        for (i, j) in newly_removed:
            parsed[i][j] = "."

        removed |= newly_removed

        if len(newly_removed) == 0:
            could_remove_paper = False

    return len(removed)