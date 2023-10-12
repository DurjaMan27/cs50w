# importing function from functions.py
from functions import square

for i in range(10):
    print(f"The square of {i} is {square(i)}")

'''
You could also do this:
import functions
print(f"The square of {i} is {functions.square(i)}")
'''