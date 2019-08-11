"""Implement a program that prints out a half-pyramid of a specified height, per the below.
$ python mario.py
Height: 5
    #
   ##
  ###
 ####
#####

$ python mario.py
Height: 3
  #
 ##
###
"""
from cs50 import get_int

while True:
    n = get_int("Height: ")
    if n > 0 and n < 9:
        break

for i in range(1, n+1):
    print((n-i) * " ", i*"#")