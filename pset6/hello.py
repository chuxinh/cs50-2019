"""
cs50-2019 pset6/hello

The code is used to achieve the following:

$ python hello.py
What is your name?
David
hello, David

"""

from cs50 import get_float

name = get_string("What is your name?")
print(f"Hello, {name}")
