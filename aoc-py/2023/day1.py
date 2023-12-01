import helpers as h 
import re

# Create a dictionary that maps string representation of numbers to their numeric values
num_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

# Function to replace string representation with numeric value
def replace(str):
    if (str.isnumeric()): return str
    return num_dict[str]

input = h.readdaylines(1, 2023)
numsstr = [re.findall(r'one|two|three|four|five|six|seven|eight|nine|\d', line.lower()) for line in input]
nums = [list(map(replace, num)) for num in numsstr]
concat = [int(num[0] + num[-1]) for num in nums]
sum = sum(concat)

# Idee 1. Regex
# Idee 2. Filter der numerischen Charktere im String
# Idee 3. For-Schleife 2 Variablen f, l

