import random


if __name__ == "__main__":
    player_name = input("Hello! what is your name?")
    The_number = random.randint(1,20)
    print("Well, ", player_name, ", I am thinking of a number between 1 and 20")
    guesses = 0
    while(True):
        guess = int(input("Take a guess."))
        guesses += 1
        if (guess == The_number):
            print("Good job, ", player_name, " You guessed my number in ", guesses, " guesses!")
            break
        elif (guess > The_number):
            print("Your guess is too high.")
        else:
            print("Your guess is too low")
