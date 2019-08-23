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

# the tutorial suggested use set() here
# some difference between set and list:
    # A set is an unordered collection with no duplicate elements, only hashable objects can participate (what's hash?)
    # Set objects also support mathematical operations like union, intersection, difference, and symmetric difference
    # List can have duplicates and the order is well defined, can contain any objects

banned_words = set()

def main():
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        # exit(0) means a clean exit without any errors / problems
        # exit(1) means there was some issue / error / problem and that is why the program is exiting
        exit(1)

    file_name = (argv[1])

    with open(file_name, "r") as file:
        for line in file:
        # rsplit remove spaces to the right of the string
        # get the word only
            banned_word = line.rsplit("\n")[0]
            banned_words.add(banned_word)
    file.close()


    message = input("What message would you like to censor? \n")
    words = message.split()

    filtered = []

    for word in words:
        if word in banned_words:
            iltered.append("*" * len(word))

        else:
            filtered.append(word)

    new_message = " ".join(map(str, filtered))

    print(new_message, "\n")


if __name__ == "__main__":
    main()
    