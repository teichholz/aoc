import helpers as h 
import re

# Create a dictionary that maps string representation of numbers to their numeric values
num_dict = {
    'one': 'o1e',
    'two': 't2o',
    'three': 't3e',
    'four': 'f4r',
    'five': 'f5e',
    'six': 's6x',
    'seven': 's7n',
    'eight': 'e8t',
    'nine': 'n9e'
}

def replace(str):
    for i in range(3):
        str = re.sub(r'one|two|three|four|five|six|seven|eight|nine', lambda m: num_dict[m.group()], str)
    return str

input = h.readday(1, 2023)
# part 2, next line
input = replace(input)
nums = [re.findall(r'\d', line) for line in input.splitlines()]
concat = [int(num[0] + num[-1]) for num in nums]
sum = sum(concat)

# Idee 1. Regex
# Idee 2. Filter der numerischen Charktere im String
# Idee 3. For-Schleife 2 Variablen f, l

