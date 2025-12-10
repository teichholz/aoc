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

def part2():
    parsed = [parse(line) for line in input]
    sum = 50
    password = 0

    for steps in parsed:
        assert steps != 0
        if steps > 0:
            zeros = (sum + steps) // 100
            sum = (sum + steps) % 100
        else:
            abs_steps = -steps
            if sum == 0:
                zeros = abs_steps // 100
            elif abs_steps >= sum:
                zeros = (abs_steps - sum) // 100 + 1
            else:
                zeros = 0
            sum = (sum - abs_steps) % 100

        password += zeros

    return password
