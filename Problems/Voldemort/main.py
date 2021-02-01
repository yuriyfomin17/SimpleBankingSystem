import random

# work with this variable
n = int(input())

random.seed(n)
word = "Voldemort"
char = random.randint(0, len(word))

print(word[char])
