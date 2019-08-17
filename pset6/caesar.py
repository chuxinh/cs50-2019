"""Implement a program that encrypts messages using Caesar’s cipher, per the below.
$ python caesar.py 13
plaintext:  HELLO
ciphertext: URYYB
Details of Caesar’s cipher can be found here: https://lab.cs50.io/cs50/labs/2019/x/caesar/
"""

from cs50 import get_string
import sys

def main():
    # validate command line argument
    try:
        key = int(sys.argv[1])
        if key > 0 and len(sys.argv) == 2:

            # get string to encrypt
            input = get_string("plaintext: " )

            print("ciphertext: ", end="")

            for i in range(len(input)):
                if input[i].isupper():
                    upper = (((ord(input[i]) - 65) + key) % 26) + 65
                    print(chr(upper), end="")

                elif input[i].islower():
                    lower = (((ord(input[i]) - 97) + key) % 26) + 97
                    print(chr(lower), end="")
                else:
                    print("{}".format(input[i]), end="")

            # print new line
            print()

        else:
            print("Usage: python caesar.py k")
    except:
        print("Usage: python caesar.py k")


if __name__ == "__main__":
    main()
