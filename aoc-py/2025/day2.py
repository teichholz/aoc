import helpers as h

input = h.readday(2, 2025, example=False)


def parse(input: str) -> list[tuple[int, int]]:
    return [tuple(map(int, range.split("-"))) for range in input.split(",")]


def part1():
    parsed = parse(input)
    sum = 0

    for start, end in parsed:
        for i in range(start, end + 1):
            st = str(i)
            ln = len(st)
            if ln % 2 == 0 and st[0 : ln // 2] == st[ln // 2 :]:
                print(i)
                sum += i

    return sum

def part2():
    parsed = parse(input)
    sum = 0

    for (start, end) in parsed:
        print(start, end)
        for i in range(start, end + 1):
            st = str(i)
            for win_size in range(1, len(st) // 2 + 1):
                if (len(st) % win_size != 0):
                    continue

                chunks = list(h.chunked(st, win_size))
                if all(chunk == chunks[0] for chunk in chunks):
                    print(i, chunks)
                    sum += i
                    break


    return sum
