import math

min_num = math.inf

curr_num = input()
while curr_num != '.':
    curr_num = float(curr_num)
    min_num = min(min_num, curr_num)
    curr_num = input()

print(min_num)
