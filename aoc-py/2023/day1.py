import helpers as h 
import re

# Create a dictionary that maps string representation of numbers to their numeric values
input = h.readday(1, 2023)
find = lambda str: re.findall(r'(?=(one|two|three|four|five|six|seven|eight|nine|\d))', str)
numdict = {n:f'{i+1}' for i,n in enumerate(['one','two','three','four','five','six','seven','eight','nine'])}
get = lambda n: n if n.isnumeric() else numdict[n]
nums = [*map(find, input.splitlines())]
concat = [int(get(num[0]) + get(num[-1])) for num in nums]
sum = sum(concat)

# Idee 1. Regex
# Idee 2. Filter der numerischen Charktere im String
# Idee 3. For-Schleife 2 Variablen f, l

