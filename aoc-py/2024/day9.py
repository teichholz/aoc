from typing import Generator
from helpers import readday

input = readday(9, 2024, example=False)

empty_id = -1
def parse() -> list[int]:
    nums = [int(n) for n in input.strip()]
    files = list()
    ctr = 0  # file id counter
    for i, n in enumerate(nums):
        if i % 2 == 0:
            files.extend([ctr] * n)
            ctr += 1
        else:
            # empty space has file id -1
            files.extend([empty_id] * n)

    # invariance that the final block is a file
    while files[-1] == empty_id:
        files = files[:-1]

    return files

def part1():
    fs = parse()

    empty_ptr = fs.index(empty_id)
    file_ptr = len(fs) - 1
    while empty_ptr < file_ptr:
        fs[empty_ptr], fs[file_ptr] = fs[file_ptr], fs[empty_ptr]

        while fs[empty_ptr] != empty_id:
            empty_ptr += 1
        while fs[file_ptr] == empty_id:
            file_ptr -= 1

    return checksum(fs)

def part2():
    """
    inefficient, since it it has quadratic complexity
    """
    fs = parse()

    cur_id = max(fs)
    file_start = fs.index(cur_id)
    file_end = len(fs)

    while cur_id >= 0:
        for empty_start, empty_end in empties(fs):
            if empty_start >= file_start:
                continue

            empty_size = size(empty_start, empty_end)
            file_size = size(file_start, file_end)
            if empty_size >= file_size:
                fs[empty_start:empty_start + file_size], fs[file_start:file_end] = fs[file_start:file_end], fs[empty_start:empty_start + file_size]
                break

        cur_id -= 1
        file_start = fs.index(cur_id)
        file_end = file_start
        while fs[file_end] == cur_id:
            file_end += 1

    return checksum(fs)

def empties(fs) -> Generator[tuple[int, int]]:
    start = None
    count = 0

    for i, val in enumerate(fs):
        if val == empty_id:
            if start is None:
                start = i
            count += 1
        else:
            if count > 0:
                yield start, start + count
                start = None
                count = 0

    if count > 0:
        yield start, start + count

def size(start, end):
    return end - start

def checksum(files):
    return sum(index * id if id >= 0 else 0 for index, id in enumerate(files))

def flatten(files):
    return [id for id, size in files for _ in range(size)]
