import random
import re
import heapq


class Othello:

    def __init__(self):
        self.board = [[" " for k in range(8)] for i in range(8)]
        self.alpha_map = {chr(ord("A") + i): i for i in range(8)}
        self.priority = [[10 for k in range(8)] for i in range(8)]
        self.set_priority()
        for k in range(8):
            self.alpha_map[chr(ord("a") + k)] = k
        self.board[3][3] = "X"
        self.board[3][4] = "O"
        self.board[4][4] = "X"
        self.board[4][3] = "O"
        self.x_num = 0
        self.o_num = 0
        self.count()
        self.tile = {}
        self.hint = False
        self.start_game()

    def set_priority(self):
        for i in [0, 7]:
            for k in [0, 7]:
                self.priority[i][k] = 1
            for k in range(4):
                self.priority[i][2+k] = 2
                self.priority[2+k][i] = 2
            for k in [1, 6]:
                self.priority[i][k] = 6
                self.priority[k][i] = 6
        for i in [1, 6]:
            for k in [1, 6]:
                self.priority[i][k] = 7
            for k in range(4):
                self.priority[i][2+k] = 5
                self.priority[2+k][i] = 5
        for i in [2, 5]:
            for k in [2, 5]:
                self.priority[i][k] = 3
            for k in [3, 4]:
                self.priority[i][k] = 4
                self.priority[k][i] = 4

    def play_again(self):
        again = input("Do you want to play again? (yes or no)")
        while again not in ("yes", "no"):
            again = input("please choose between yes or no")
        if again == "yes":
            Othello()

    def start_game(self):
        print("Welcome to Othello!")
        player_tile = input("Do you want to be X or O?")
        while player_tile not in ["X", "x", "O", "o"]:
            player_tile = input("Please choose between X and O")
        if player_tile in ["x", "X"]:
            self.tile["player"] = "X"
            self.tile["computer"] = "O"
        else:
            self.tile["player"] = "O"
            self.tile["computer"] = "X"

        self.turn = self.who_goes_first()
        print(f"The {self.turn} will go first")
        for i in range(60):
            if self.turn == "player":
                if not self.display_hints():
                    print("There are no move to make. The turn goes to the computer.")
                    self.turn = "computer"
                    continue
                self.print_board()
                self.clear_hints()
                player_move = self.get_player_move()
                self.flip(player_move)
                if not player_move:
                    return
                self.print_board()
                self.turn = "computer"
            elif self.turn == "computer":
                if not self.display_hints():
                    print("There are no moves to make for the computer the turn goes to player.")
                    self.turn = "player"
                    continue
                self.clear_hints()
                computer_move = self.get_computer_move()
                self.flip(computer_move[1])
                input("Press Enter to see the computer's move.")
                self.print_board()
                self.turn = "player"
            if self.end_game():
                self.play_again()
                break

    def end_game(self):
        self.display_hints()
        for i in self.board:
            for k in i:
                if k == " ":
                    return False
        self.clear_hints()
        if self.tile["player"] == "X":
            player_tile_num = self.x_num
            computer_tile_num = self.o_num
        else:
            player_tile_num = self.o_num
            computer_tile_num = self.x_num
        if player_tile_num == computer_tile_num:
            print("Draw game!")
            return True
        elif player_tile_num > computer_tile_num:
            print(f"You won!. You have beaten computer by {player_tile_num - computer_tile_num} points.")
            return True
        else:
            print(f"you lost. The computer beat you by {computer_tile_num - player_tile_num} points.")
            return True

    def flip(self, move):
        to_flip = self.is_valid_move(move)
        self.board[move[1]][move[0]] = self.tile[self.turn]
        for tile in to_flip:
            self.board[tile[1]][tile[0]] = self.tile[self.turn]
        self.count()

    def get_computer_move(self):
        moves = self.get_hints()
        h = []
        for move in moves:
            heapq.heappush(h, (self.priority[move[1]][move[0]], move))
        return heapq.heappop(h)

    def get_player_move(self):
        move_input = input("Enter your move, \"quit\" to end the game, or \"hints\" to toggle hints.")
        p = re.compile("[a-hA-H]\d")
        if move_input == "quit":
            return []
        elif move_input == "hints":
            self.hint = not self.hint
            self.display_hints()
            self.print_board()
            self.clear_hints()
            move_input = input("Enter your move.")
        tiles_to_flip = []
        if p.match(move_input):
            move = [self.alpha_map[move_input[0]], int(move_input[1]) - 1]
            tiles_to_flip = self.is_valid_move(move)
        while not tiles_to_flip:
            move_input = input("That is not a valid move. "
                               "Enter your move in form of ex)\"A1\" or enter \"hints\" to toggle hints.")
            if move_input == "hints":
                self.hint = not self.hint
                self.display_hints()
                self.print_board()
                self.clear_hints()
                move_input = input("Enter your move.")
            if not p.match(move_input):
                continue
            move = [self.alpha_map[move_input[0]], int(move_input[1]) - 1]
            tiles_to_flip = self.is_valid_move(move)
        return move

    def is_on_board(self, move):
        if not all(0 <= a < 8 for a in move):
            return False
        return True

    def is_valid_move(self, move):
        if not all(0 <= a < 8 for a in move):
            print("That move is out of board.")
            return False
        if self.board[move[1]][move[0]] in ["X", "O"]:
            return False
        this_tile = self.tile[self.turn]
        if this_tile == "O":
            op_tile = "X"
        else:
            op_tile = "O"

        tiles_to_flip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1],
                                       [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = move
            x += xdirection  # First step in the x direction
            y += ydirection  # First step in the y direction
            while self.is_on_board([x,y]) and self.board[y][x] == op_tile:
                x += xdirection
                y += ydirection
                if self.is_on_board([x, y]) and self.board[y][x] == this_tile:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == move[0] and y == move[1]:
                            break
                        tiles_to_flip.append([x, y])
        if len(tiles_to_flip) == 0:
            return False
        return tiles_to_flip

    def clear_hints(self):
        for i in self.board:
            for k in range(8):
                if i[k] == ".":
                    i[k] = " "

    def get_hints(self):
        hints = []
        for i in range(8):
            for k in range(8):
                if self.is_valid_move([i, k]):
                    hints.append([i, k])
        return hints

    def display_hints(self):
        hint_num = 0
        for i in range(8):
            for k in range(8):
                if self.is_valid_move([i, k]):
                    if self.hint:
                        self.board[k][i] = "."
                    hint_num += 1
        if hint_num == 0:
            return False
        return True

    def who_goes_first(self):
        if random.randint(0, 1) == 0:
            return "computer"
        else:
            return "player"

    def print_board(self):
        print("   A B C D E F G H")
        print(" +-----------------+")
        for i,line in enumerate(self.board):
            print(f"{i+1}|", end=" ")
            for k in line:
                print(k, end=" ")
            print(f"|{i+1}")
        print(" +-----------------+")
        print("   A B C D E F G H")
        if self.tile["player"] in ["X", "x"]:
            player_num = self.x_num
            com_num = self.o_num
        else:
            player_num = self.o_num
            com_num = self.x_num
        print(f"You: {player_num} points. Computer: {com_num} points.")

    def count(self):
        x_count = 0
        o_count = 0
        for i in self.board:
            for k in i:
                if k == "O":
                    o_count+=1
                elif k == "X":
                    x_count+=1
        self.x_num = x_count
        self.o_num = o_count


if __name__ == "__main__":
    othello = Othello()

