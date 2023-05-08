import sys

try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    sys.exit("Error: Invalid input")

try:
    result = x / y
except ZeroDivisionError:
    sys.exit("Error: Cannot divide by 0.")

print(f"{x} / {y} is {result}")
