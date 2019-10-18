import random


class Bagels:

    def __init__(self):
        print("I an thinking of a 3-digit number. Try to guess what it is.")
        print("Here are some clues:")
        print("When I say:    That means")
        print(" Pico          One digit is correct but in the wrong position.")
        print(" Fermi         One digit is correct and in the right position.")
        print(" Bagels        No digit is correct.")
        response = (["Fermi", 0], ["Pico", 0], ["Bagels", 0])

        self.the_number = str(random.randint(1, 999)).zfill(3)
        self.num_set = set(list(self.the_number))
        print("I have thought up a number. You have 10 guesses to get it.")
        for i in range(1, 11):
            guess = input(f'Guess #{i}:')
            if guess == self.the_number:
                print("You got it!")
                break
            for k in range(3):
                if guess[k] == self.the_number[k]:
                    response[0][1] += 1
                elif guess[k] in self.num_set:
                    response[1][1] += 1
            for k in range(response[0][1]):
                print(f'{response[0][0]} ')
            for k in range(response[1][1]):
                print(f'{response[1][0]} ')
            if response[0][1] + response[1][1] == 0:
                print(response[2][0])
            if i == 10:
                print(f"You have failed to guess the number. The number was {self.the_number}.")
            response[0][1] = 0
            response[1][1] = 0
        again = input("Do you want to play again?(yes or no)")
        while again != "yes" and again != "no":
            again = input("Please choose between yes or no.")
        if again == "yes":
            Bagels()


if __name__ == "__main__":
    Bagels()