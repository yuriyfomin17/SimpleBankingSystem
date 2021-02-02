# put your python code here
import math

squirrels = int(input())
nuts = int(input())
nuts_left = nuts - squirrels * math.floor(nuts / squirrels)
print(nuts % squirrels)
