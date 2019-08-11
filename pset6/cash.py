"""Implement a program that calculates the minimum number of coins required to give a user change.
$ python cash.py
Change owed: 0.41
4
"""
from cs50 import get_float

while True:
    # in dollar value
    change = get_float("Change owed: ")
    if isinstance(change, float) and change > 0:
        break

# convert dollar value to cents
change_cents = change * 100
remainder = change_cents

# init number of coins to be returned
n = 0

while remainder > 0:
    # divide by quarters
    if remainder >= 25:
        n = n + remainder // 25
        remainder = remainder % 25
    # divide by dimes
    elif remainder >= 10:
        n = n + remainder // 10
        remainder = remainder % 10
    # divide by nickels
    elif remainder >= 5:
        n = n + remainder // 5
        remainder = remainder % 5
    else:
        n = n + remainder // 1
        remainder = remainder % 1

print(int(n))