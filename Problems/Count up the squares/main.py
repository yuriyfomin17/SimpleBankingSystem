# put your python code here
sum = int(input())
numbers = [sum]
while sum != 0:
    curr_num = int(input())
    numbers.append(curr_num)
    sum = sum + curr_num

sum_squares = 0
for i in range(0, len(numbers)):
    sum_squares += numbers[i] * numbers[i]
print(sum_squares)
