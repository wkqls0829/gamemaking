import random
import sys
import numpy as np


class Sonar:

    def __init__(self):
        print("S O N A R!")
        self.board_height = 15
        self.board_width = 60
        self.num_of_treasure = 3
        self.treasure = list(np.array([random.randint(0, 49), random.randint(0, 15)]) for k in range(3))
        self.num_of_device = 16
        self.device_loc = []

        check = True
        while check:
            check = False
            for i in self.treasure:
                for k in self.treasure:
                    if i is not k and np.array_equal(i, k):
                        self.treasure = list(np.array([random.randint(0, 49), random.randint(0, 15)]) for k in range(3))
                        check = True
                        break

        self.sea = []
        for i in range(self.board_height):
            self.sea.append([])
            for k in range(self.board_width):
                self.sea[i].append(self.wave_shape())

        self.instruction()
        self.draw_board()

        while self.check_remaining():
            if not self.drop_device():
                return


        again = input("Do you want to play again? (yes or no)")
        if again == "yes":
            Sonar()

    def drop_device(self):
        drop_input = input("Where do you want to drop the next sonar device? (0-59 0-14) (or type quit)")
        if drop_input == "quit":
            return False
        drop = np.array(list(map(int, drop_input.split(" "))))
        while not self.is_valid(drop):
            drop_input = input(f"Please type in number on 0-{self.board_width} 0-{self.board_height} (or type quit)")
            if drop_input == "quit":
                return False
            drop = np.array(list(map(int, drop_input.split(" "))).reverse())
        self.device_loc.append(drop)
        closest = 10
        closest_idx = -1
        for idx, tr in enumerate(self.treasure):
            dist = max(list(map(abs, drop - tr)))
            if dist < closest:
                closest = dist
                closest_idx = idx
        if closest == 0:
            del self.treasure[closest_idx]
            self.reset()
            self.draw_board()
            print("You have found a sunken treasure chest!")
        elif closest == 10:
            self.sea[drop[1]][drop[0]] = 0
            self.draw_board()
            print("There are no treasures found near by.")
        else:
            self.sea[drop[1]][drop[0]] = closest
            self.draw_board()
            print(f"Treasure detected at a distance of {closest} from the sonar device")
        self.num_of_device -= 1
        return True

    def reset(self):
        for pos in self.device_loc:
            closest = 10
            for tr in self.treasure:
                dist = max(list(map(abs, pos - tr)))
                if dist < closest:
                    closest = dist
            if closest == 10:
                closest = 0
            self.sea[pos[1]][pos[0]] = closest

    def is_valid(self, drop):
        return 0 <= drop[0] < self.board_width and 0 <= drop[1] < self.board_height

    def check_remaining(self):
        if len(self.treasure) == 0:
            print("Congratulation! You have found all the Treasure!")
            return False
        elif self.num_of_device == 0:
            print("We've run out of sonar device! Now we have to turn the ship around and head for home with treasure chests still out there! Game over.")
            print(" The remaining chests were here: ")
            for i in self.treasure:
                print(i)
            return False
        else:
            print(f"You have {self.num_of_device} left. {len(self.treasure)} treasure chests remaining.")
            return True

    def wave_shape(self):
        num = random.randint(0,2)
        if num:
            return "~"
        else:
            return "'"

    def instruction(self):
        instruct = input("Would you like to view the instruction? (yes/no)")
        if instruct == "yes":
            print('''Instructions:
            You are the captain of the Simon, a treasure-hunting ship. Your current mission
            is to find the three sunken treasure chests that are lurking in the part of the
            ocean you are in and collect them.

            To play, enter the coordinates of the point in the ocean you wish to drop a
            sonar device. The sonar can find out how far away the closest chest is to it.
            For example, the d below marks where the device was dropped, and the 2's
            represent distances of 2 away from the device. The 4's represent
            distances of 4 away from the device.
    
                444444444
                4       4
                4 22222 4
                4 2   2 4
                4 2 d 2 4
                4 2   2 4
                4 22222 4
                4       4
                444444444
            Press enter to continue...''')
            input()
            print('''For example, here is a treasure chest (the c) located a distance of 2 away
            from the sonar device (the d):
            
                22222
                c   2
                2 d 2
                2   2
                22222
            
            The point where the device was dropped will be marked with a 2.
            
            The treasure chests don’t move around. Sonar devices can detect treasure
            chests up to a distance of 9. If all chests are out of range, the point
            will be marked with O
            
            If a device is directly dropped on a treasure chest, you have discovered
            the location of the chest, and it will be collected. The sonar device will
            remain there.
            
            When you collect a chest, all sonar devices will update to locate the next
            closest sunken treasure chest.
            Press enter to continue...''')
            input()
            print()

    def draw_board(self):
        print("   ", end="")
        for i in range(1, (self.board_width)//10):
            print(f"         {i}", end="")
        print("")
        print("  ", end="")
        for i in range(self.board_width):
            print(i % 10, end="")
        print("")
        for i,opensea in enumerate(self.sea):
            print(str(i).zfill(2), end="")
            for k in opensea:
                print(k, end="")
            print(str(i).zfill(2), end="")
            print("")
        print("  ", end="")
        for i in range(self.board_width):
            print(i % 10, end="")
        print("")
        print("   ", end="")
        for i in range(1, (self.board_width) // 10):
            print(f"         {i}", end="")
        print("")
        return


if __name__ == "__main__":
    Sonar()

