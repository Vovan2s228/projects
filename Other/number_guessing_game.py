from random import randrange
import time


def game():
    points = 0
    for a in range(1, 4):
        print("Round " + str(a))
        while True:
            random_number = randrange(11)
            while True:
                n1 = input("Make a guess\n").lower()
                n1 = strings_to_numbers(n1)
                if n1.isnumeric():
                    n1 = int(n1)
                    break
                else:
                    print("You need to enter an integer number. Try again")
                    time.sleep(1)

            if n1 == random_number:
                points += 10
                print("You guessed it! Good job!\n")
                break
            elif n1 < random_number:
                print("Higher\n")
            else:
                print("Lower\n")

            while True:
                n2 = input("Make another guess\n").lower()
                n2 = strings_to_numbers(n2)
                if n2.isnumeric():
                    n2 = int(n2)
                    break
                else:
                    print("You need to enter an integer number. Try again.")
                    time.sleep(1)

            if n2 == random_number:
                points += 5
                print("You guessed it! Good job!\n")
                break
            else:
                print("Sorry, you did not guess it.\n")
            break
    if points >= 15:
        print(f"Congratulations, you won! You have achieved {points} points!")
    else:
        print(f"Better luck next time! You have achieved {points} points!")
    return


def strings_to_numbers(m):
    numbers = {
            "zero": '0',
            "one": '1',
            "two": '2',
            "three": '3',
            "four": '4',
            "five": '5',
            "six": '6',
            "seven": '7',
            "eight": '8',
            "nine": '9',
            "ten": '10'
        }
    if m.isalpha() and m in numbers:
        return numbers[m]
    else:
        return m


def main():
    intro = input("""To start the game type 'start'. For rules type 'help'.\n""").lower()
    if intro == "help":
        print("""
The computer will generate a number. 
Your task is to guess what number it is. 
If you get it on the first try you will get 10 points.
You will get a second try if you don't, so don't worry :)
Although this time you will only get 5 points.
The computer will also give you a clue whether you need to pick a number that is higher or lower.
After that the round will be over.
You will have three rounds in total.
Your goal is to get more than 15 points.
Good luck :)
""")
        time.sleep(3)
        game()
    elif intro == 'start':
        game()
    else:
        print("""Sorry, I don't understand what you are saying.""")
    return


try:
    while True:
        main()
        ans = input("Would you like to play another game?\n").lower()
        if ans == "yes" or ans == "y":
            continue
        else:
            break

except ValueError:
    print("Oops! You tried to type not a number")

except KeyboardInterrupt:
    print("You force quit the program")

except KeyError:
    print("Oops! You tried to type not a number")
