import helpers as h

dkey = 811589153
numbers = [int(x) * dkey for x in h.openday(20, 2022)]
# numbers = [1, 2, -3, 3, -2, 0, 4]
indices = list(range(len(numbers)))

# print(*map(lambda x: numbers[x], indices))
for i in indices * 10: # * 10 copies the list
    indices.pop(j := indices.index(i))
    indices.insert((j + numbers[i]) % len(indices), i)
    # print(*map(lambda x: numbers[x], indices))

zero = indices.index(numbers.index(0))
print(sum([numbers[indices[(zero + ind) % len(indices)]] for ind in [1000, 2000, 3000]]))