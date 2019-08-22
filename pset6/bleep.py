"""Implement a program that censors messages that contain words that appear on a list of supplied "banned words."

$ python bleep.py banned.txt
What message would you like to censor?
What the heck
What the ****
$ python bleep.py banned.txt
What message would you like to censor?
gosh darn it
**** **** it

"""
from cs50 import get_string
from sys import argv

# the tutorial suggested to use set() here
# some difference between set and list:
    # A set is an unordered collection with no duplicate elements, only hashable objects can participate (what's hash?)
    # Set objects also support mathematical operations like union, intersection, difference, and symmetric difference
    # List can have duplicates and the order is well defined, can contain any objects

words = set()

def main():
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        # exit(0) means a clean exit without any errors / problems
        # exit(1) means there was some issue / error / problem and that is why the program is exiting
        exit(1)

    input = (argv[1])

    file = open(input, "r")

    for line in file:
        # rsplit remove spaces to the right of the string
        # get the word only
        word = line.rsplit("\n")[0]
        words.add(word)
    file.close()


    message = get_string("What message would you like to censor? \n")
    string = message.split()

    filtered = []

    for i in string:
        if i in words:
                filtered.append("*" * len(i))

        else:
            filtered.append(i)

    new_message = " ".join(map(str, filtered))

    print(new_message, "\n")


if __name__ == "__main__":
    main()