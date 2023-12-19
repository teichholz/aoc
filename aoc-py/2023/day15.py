from helpers import readdaylines

input = readdaylines(15, 2023, example=False)[0].split(',')

def HASH(str):
    cur = 0
    for char in str:
        cur += ord(char)
        cur *= 17
        cur %= 256
    return cur

def part1():
    return sum(map(HASH, input))

def part2():
    """
    Python 3.7 preserves the insertion order of dictionaries so they can act like a list of tuples with O(1) access + mutation and cheap appending
    """
    boxes = {}
    for lens in input:
        if ('-' in lens):
            label, *_ = lens.split('-')
            box = HASH(label)
            if (box in boxes and label in boxes[box]):
                del boxes[box][label]
        elif ('=' in lens):
            label, focall = lens.split('=')
            focall = int(focall)
            box = HASH(label)
            if (box in boxes):
                # add label to end
                boxes[box][label] = focall
            else:
                # create hashmap if box does not exist
                boxes[box] = {label: focall}
    power = 0
    for (boxnum, box) in boxes.items():
        boxnum += 1
        for slot, (label, focall) in enumerate(box.items(), 1):
            power += boxnum * slot * focall 
    return power