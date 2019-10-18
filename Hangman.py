import random


class Hangman:

    def __init__(self):
        self.wordset = 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split()
        self.missed_letters = set([])
        self.guessed_letters = set([])
        self.secret_word = self.wordset[random.randint(0, len(self.wordset) - 1)]
        self.blank_letters = "_" * len(self.secret_word)
        print("H A N G M A N")

        while self.do_continue():
            self.print()
            self.make_a_guess()

    def print(self):
        print(" +_---+\n |  |")
        if len(self.missed_letters) >= 1:
            print (" O  |")
        else:
            print ("    |")

        if len(self.missed_letters) >= 4:
            print("/|\\ |")
        elif len(self.missed_letters) == 3:
            print("/|  |")
        elif len(self.missed_letters) == 2:
            print(" |  |")
        else:
            print("    |")

        if len(self.missed_letters) == 6:
            print("/ \\ |")
        elif len(self.missed_letters) == 5:
            print("/   |")
        else:
            print("    |")

        print("=========")
        print("Missed letters: ")
        for i in self.missed_letters:
            print(i, end=" ")
        print ("\n", self.blank_letters)

    def make_a_guess(self):
        guess = input("Guess a letter.")
        while guess in self.guessed_letters:
            guess = input("That guess has already been made, please type in other letter.")
        self.guessed_letters.add(guess)
        if self.secret_word.find(guess) != -1:
            blank_list = list(self.blank_letters)
            for i in range(0, len(blank_list)):
                if self.secret_word[i] == guess:
                    blank_list[i] = guess
            self.blank_letters = "".join(blank_list)
        else:
            self.missed_letters.add(guess)

    def do_continue(self):
        if self.blank_letters == self.secret_word:
            print("Yes! The secret word is \"", self.secret_word, "\"! You have won!")
            answer = input("Do you want to play again? (yes or no)")
            while answer != "yes" and answer != "no":
                answer = input("Please choose between yes or no")
            if answer == "yes":
                Hangman()
            return False
        elif len(self.missed_letters) > 6:
            print("You have failed to save the man. The secret word is \"", self.secret_word, "\". You have lost")
            answer = input("Do you want to play again? (yes or no)")
            while answer != "yes" and answer != "no":
                answer = input("Please choose between yes or no")
            if answer == "yes":
                Hangman()
            return False
        return True


if __name__ == "__main__":
    Hangman()