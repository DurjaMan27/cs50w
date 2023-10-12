import sys

try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    print("Error: invalid input")
    sys.exit(1) # necessary to end the program

try:
    result = x / y
except ZeroDivisionError:
    print("Error: cannot divide by zero")
    sys.exit(1)

print(f"{x} / {y} is result")