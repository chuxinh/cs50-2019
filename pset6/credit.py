"""Implement a program that determines whether a provided credit card number is valid according to Luhn’s algorithm.
$ python credit.py
Number: 378282246310005
AMEX
Detailed credit logic can be found here (Luhn’s algorithm): https://lab.cs50.io/cs50/labs/2019/x/credit/
"""
from cs50 import get_int

def main():
    while True:
        cc_number = get_int("Number: ")
        if isinstance(cc_number, int) and cc_number > 0:
            break

    # make a list and extract each digit of the credit card number
    cc_list = list(map(int, str(cc_number)))

    # reverse the cc_list
    cc_list.reverse()

    # get every second digit
    even_digit = [x*2 for x in cc_list[1::2]]
    # lopp over the list and every single character to get every signle digit
    even_digit = [int(ch) for i in even_digit for ch in str(i)]

    odd_digit = [x for x in cc_list[0::2]]
    validation = sum(even_digit) + sum(odd_digit)
    is_valid = validation % 10 == 0

    first_two_digits = str(cc_number)[0:2]
    num_digits = len(str(cc_number))

    if is_valid and first_two_digits in ['34', '37'] and num_digits == 15:
        # All American Express numbers start with 34 or 37
        print("AMEX\n")
    elif is_valid and first_two_digits in ['51', '52', '53', '54', '55'] and num_digits == 16:
        # Most MasterCard numbers start with 51, 52, 53, 54, or 55
        print("MASTERCARD\n")
    elif is_valid and first_two_digits[0] == '4' and num_digits in [13, 16]:
        # Visa numbers starts with 4
        print("VISA\n")
    else:
        print("INVALID\n")


if __name__ == "__main__":
    main()