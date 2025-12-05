import helpers as h

input = h.readdaylines(1, 2025, example=False)


def parse(line: str) -> int:
    dir, *num = line
    return int(''.join(num)) if dir == 'R' else -int(''.join(num))

def part1():
    parsed = [parse(line) for line in input]
    sum = 50
    password = 0

    for num in parsed:
        sum += num
        sum = sum % 100
        if sum == 0:
            password += 1

    return password

class Dial:
    def __init__(self) -> None:
        self.password = 0
        self.value = 50

    def rotate(self, steps: int) -> None:
        self.value += steps

    def forward(self, steps: int) -> None:
        pass

    def backward(self, steps: int) -> None:
        pass

def part2():
    parsed = [parse(line) for line in input]
    sum = 50
    password = 0

    return password
