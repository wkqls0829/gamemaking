import pygame
import sys
import random
import time
import copy
import os
import traceback
from pygame.locals import *
from Othello import *

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class VisualOthello(Othello):

    def __init__(self):
        self.FPS = 10
        self.WINDOW_WIDTH = 640
        self.WINDOW_HEIGHT = 480
        self.SPACE_SIZE = 50
        self.BOARD_WIDTH = 8
        self.BOARD_HEIGHT = 8
        self.TILE_COLOR = {'O': "WHITE_TILE", 'X': "BLACK_TILE"}
        self.ANIMATIONSPEED = 25

        #                 R   G   B
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BRIGHT_BLUE = (0, 50, 255)
        self.DARK_TURQUOISE = (3, 54, 73)
        self.GREEN = (0, 204, 0)
        self.BROWN = (174, 94, 0)

        self.BG_COLOR = self.DARK_TURQUOISE
        self.TILE_COLOR = self.GREEN
        self.TEXT_BG_COLOR1 = self.BRIGHT_BLUE
        self.TEXT_BG_COLOR2 = self.GREEN
        self.GRID_LINE_COLOR = self.BLACK
        self.TEXT_COLOR = self.WHITE
        self.HINT_COLOR = self.BROWN
        self.BASIC_FONT_SIZE = 16

        self.XMARGIN = int((self.WINDOW_WIDTH - (self.SPACE_SIZE * self.BOARD_WIDTH + (self.BOARD_WIDTH - 1)))/2)
        self.YMARGIN = int((self.WINDOW_HEIGHT - (self.SPACE_SIZE * self.BOARD_HEIGHT + (self.BOARD_HEIGHT - 1))))
        self.start_game()

    def start_game(self):

        while True:
            if self.run_game() == False:
                break

    def run_game(self):
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
        self.turn = random.choice(['computer', 'player'])
        self.player_tile = random.choice(['O', 'X'])
        pygame.init()
        self.main_clock = pygame.time.Clock()
        self.display_surf = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        pygame.display.set_caption('Othello')
        self.BASIC_FONT = pygame.font.SysFont('Sans', self.BASIC_FONT_SIZE)
        self.BIG_FONT = pygame.font.SysFont('Sans', 32)
        #raise NameError('1')
        board_url = resource_path('flippyboard.png')
        self.board_image = pygame.image.load(board_url)
        self.board_image = pygame.transform.smoothscale(self.board_image, (
            self.BOARD_WIDTH * self.SPACE_SIZE, self.BOARD_HEIGHT * self.SPACE_SIZE))
        #raise NameError('2')
        self.board_image_rect = self.board_image.get_rect()
        self.board_image_rect.topleft = (self.XMARGIN, self.YMARGIN)
        BGI_url = resource_path('flippybackground.png')
        self.BGIMAGE = pygame.image.load(BGI_url)
        self.BGIMAGE = pygame.transform.smoothscale(self.BGIMAGE, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.BGIMAGE.blit(self.board_image, self.board_image_rect)
        self.hint = False
        self.turn = random.choice(['computer', 'player'])
        self.draw_board('')
        self.player_tile = self.choose_tile()
        if self.player_tile == 'X':
            self.computer_tile = 'O'
        else:
            self.computer_tile = 'X'
        if self.player_tile in ["x", "X"]:
            self.tile["player"] = "X"
            self.tile["computer"] = "O"
        else:
            self.tile["player"] = "O"
            self.tile["computer"] = "X"

        new_game_surf = self.BASIC_FONT.render('New Game', True, self.TEXT_COLOR, self.TEXT_BG_COLOR2)
        new_game_rect = new_game_surf.get_rect()
        new_game_rect.topright = (self.WINDOW_WIDTH - 8, 10)

        hints_surf = self.BASIC_FONT.render('Hints', True, self.TEXT_COLOR, self.TEXT_BG_COLOR2)
        hints_rect = hints_surf.get_rect()
        hints_rect.topright = (self.WINDOW_WIDTH - 8, 40)
        while True:
            if self.turn == 'player':
                if not self.get_hints():
                    break
                movexy = None
                while not movexy:
                    self.check_for_quit()
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP:
                            mousep = event.pos
                            if new_game_rect.collidepoint(mousep):
                                return True
                            elif hints_rect.collidepoint(mousep):
                                self.hint = not self.hint
                            movexy = self.get_space_clicked(mousep)
                            if movexy and not self.is_valid_move(movexy):
                                movexy = None
                    self.draw_board('')
                    self.draw_info()

                    self.display_surf.blit(new_game_surf, new_game_rect)
                    self.display_surf.blit(hints_surf, hints_rect)

                    self.main_clock.tick(self.FPS)
                    pygame.display.update()
                self.make_move(movexy, True)
                self.turn = 'computer'
                if not self.get_hints():
                    self.turn = 'player'

            else:
                if not self.get_hints():
                    break
                self.draw_board('')
                self.draw_info()

                self.display_surf.blit(new_game_surf, new_game_rect)
                self.display_surf.blit(hints_surf, hints_rect)
                pause_until = time.time() + random.randint(5,15) * 0.1
                while time.time() < pause_until:
                    pygame.display.update()

                movep = self.get_computer_move()[1]
                self.make_move(movep, True)
                self.turn = 'player'
                if not self.get_hints():
                    self.turn = 'computer'

        self.draw_board('')
        scores = self.get_scores()

        if scores[0] > scores[1]:
            text = f'You beat the computer by {scores[0] - scores[1]} points! Congratulations!'
        elif scores[0] < scores[1]:
            text = f'You lost. The computer beat you by {scores[1] - scores[0]} points.'
        else:
            text = 'The game was a tie!'

        text_surf = self.BIG_FONT.render(text, True, self.TEXT_COLOR, self.TEXT_BG_COLOR1)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(self.WINDOW_WIDTH/2), int(self.WINDOW_HEIGHT/2))
        self.display_surf.blit(text_surf, text_rect)

        text_surf2 = self.BIG_FONT.render('Play again?', True, self.TEXT_COLOR, self.TEXT_BG_COLOR1)
        text_rect2 = text_surf2.get_rect()
        text_rect2.center = (int(self.WINDOW_WIDTH / 2), int(self.WINDOW_HEIGHT / 2) + 50)

        yes_surf = self.BIG_FONT.render('Yes', True, self.TEXT_COLOR, self.TEXT_BG_COLOR1)
        yes_rect = yes_surf.get_rect()
        yes_rect.center = (int(self.WINDOW_WIDTH/2) - 60, int(self.WINDOW_HEIGHT/2) + 90)

        no_surf = self.BIG_FONT.render('No', True, self.TEXT_COLOR, self.TEXT_BG_COLOR1)
        no_rect = no_surf.get_rect()
        no_rect.center = (int(self.WINDOW_WIDTH/2) + 60, int(self.WINDOW_HEIGHT/2) + 90)

        while True:
            self.check_for_quit()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mousep = event.pos
                    if yes_rect.collidepoint(mousep):
                        return True
                    elif no_rect.collidepoint(mousep):
                        return False
            self.display_surf.blit(text_surf, text_rect)
            self.display_surf.blit(text_surf2, text_rect2)
            self.display_surf.blit(yes_surf, yes_rect)
            self.display_surf.blit(no_surf, no_rect)
            pygame.display.update()
            self.main_clock.tick(self.FPS)

    def animate_tile_change(self, tiles_to_flip, tilec, tilep):
        if tilec == "O":
            add_tilec = self.WHITE
        else:
            add_tilec = self.BLACK
        add_tilep = self.board_to_pixel(tilep[0], tilep[1])
        pygame.draw.circle(self.display_surf, add_tilec, add_tilep, int(self.SPACE_SIZE/2) - 4)
        pygame.display.update()

        for rgb_values in range(0, 255, int(self.ANIMATIONSPEED*2.55)):
            if rgb_values > 255:
                rgb_values = 255
            elif rgb_values < 0:
                rgb_values = 0

            if tilec == "O":
                color = tuple([rgb_values]*3)
            else:
                color = tuple([255 - rgb_values]*3)

            for x,y in tiles_to_flip:
                centerp = self.board_to_pixel(x, y)
                pygame.draw.circle(self.display_surf, color, centerp, int(self.SPACE_SIZE/2) - 4)
            pygame.display.update()
            self.main_clock.tick(self.FPS)
            self.check_for_quit()

    def make_move(self, movep, real_move = True):
        tiles_to_flip = self.is_valid_move(movep)

        if not tiles_to_flip:
            return False

        if self.turn == "player":
            tile = self.player_tile
        else:
            tile = self.computer_tile
        self.board[movep[1]][movep[0]] = tile

        if real_move:
            self.animate_tile_change(tiles_to_flip, tile, movep)

        for x,y in tiles_to_flip:
            self.board[y][x] = tile
        return True

    def get_scores(self):
        x_num = 0
        o_num = 0
        for x in range(self.BOARD_HEIGHT):
            for y in range(self.BOARD_WIDTH):
                if self.board[y][x] == "X":
                    x_num += 1
                elif self.board[y][x] == "O":
                    o_num += 1
        if self.tile["player"] in ["X", "x"]:
            return x_num, o_num
        elif self.tile["player"] in ["O", "o"]:
            return o_num, x_num

    def draw_info(self):
        scores = self.get_scores()
        score_surf = self.BASIC_FONT.render(f"Player Score:{scores[0]}  Computer Score:{scores[1]}  {self.turn}'s turn.", True, self.TEXT_COLOR)
        score_rect = score_surf.get_rect()
        score_rect.bottomleft = (10, self.WINDOW_HEIGHT - 5)
        self.display_surf.blit(score_surf, score_rect)

    def draw_board(self, message):
        if self.hint:
            self.display_hints()
        self.display_surf.blit(self.BGIMAGE, self.BGIMAGE.get_rect())
        if message:
            textSurf, textRect = self.makeText(message, self.MESSAGECOLOR, 5, 5)
            self.display_surf.blit(textSurf, textRect)

        for x in range(self.BOARD_WIDTH+1):
            startp = ((x * self.SPACE_SIZE) + self.XMARGIN, self.YMARGIN)
            endp = ((x* self.SPACE_SIZE) + self.XMARGIN, self.YMARGIN + (self.BOARD_HEIGHT * self.SPACE_SIZE))
            pygame.draw.line(self.display_surf, self.GRID_LINE_COLOR, startp, endp)
        for y in range(self.BOARD_HEIGHT+1):
            startp = (self.XMARGIN, (y*self.SPACE_SIZE) + self.YMARGIN)
            endp = (self.XMARGIN + (self.BOARD_WIDTH*self.SPACE_SIZE), (y*self.SPACE_SIZE) + self.YMARGIN)
            pygame.draw.line(self.display_surf, self.GRID_LINE_COLOR, startp, endp)

        for x in range(self.BOARD_WIDTH):
            for y in range(self.BOARD_HEIGHT):
                centerx, centery = self.board_to_pixel(x, y)
                if self.board[y][x] in ("O", "X"):
                    if self.board[y][x] == "O":
                        tileColor = self.WHITE
                    else:
                        tileColor = self.BLACK
                    pygame.draw.circle(self.display_surf, tileColor, (centerx, centery), int(self.SPACE_SIZE/2) - 4)
                if self.board[y][x] == '.':
                    pygame.draw.rect(self.display_surf, self.HINT_COLOR, (centerx - 4, centery - 4, 8, 8))
        if self.hint:
            self.clear_hints()

    def board_to_pixel(self, x, y):
        return self.XMARGIN + x*self.SPACE_SIZE + int(self.SPACE_SIZE / 2), \
               self.YMARGIN + y*self.SPACE_SIZE + int(self.SPACE_SIZE/2)

    def get_space_clicked(self, mousep):
        for x in range(self.BOARD_WIDTH):
            for y in range(self.BOARD_HEIGHT):
                if x * self.SPACE_SIZE + self.XMARGIN < mousep[0] < (x + 1) * self.SPACE_SIZE + self.XMARGIN and y * self.SPACE_SIZE + self.YMARGIN < mousep[1] < (y + 1) * self.SPACE_SIZE + self.YMARGIN:
                    return (x, y)
        return None

    def makeText(self, text, color, top, left):
        # create the surface and rect objects for some text.
        textSurf = self.BASIC_FONT.render(text, True, color, self.BG_COLOR)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)

    def choose_tile(self):
        text_surf = self.BASIC_FONT.render('Do you want to be white or black?', True, self.TEXT_COLOR, self.TEXT_BG_COLOR1)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(self.WINDOW_WIDTH/2), int(self.WINDOW_HEIGHT/2))

        o_surf = self.BIG_FONT.render('White', True, self.TEXT_COLOR, self.TEXT_BG_COLOR1)
        o_rect = o_surf.get_rect()
        o_rect.center = (int(self.WINDOW_WIDTH/2) - 60, int(self.WINDOW_HEIGHT / 2) + 40)

        x_surf = self.BIG_FONT.render('Black', True, self.TEXT_COLOR, self.TEXT_BG_COLOR1)
        x_rect = x_surf.get_rect()
        x_rect.center = (int(self.WINDOW_WIDTH/2) + 60, int(self.WINDOW_HEIGHT / 2) + 40)

        while True:
            self.check_for_quit()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mousep = event.pos
                    if o_rect.collidepoint(mousep):
                        return 'O'
                    elif x_rect.collidepoint(mousep):
                        return 'X'
            self.display_surf.blit(text_surf, text_rect)
            self.display_surf.blit(x_surf, x_rect)
            self.display_surf.blit(o_surf, o_rect)
            pygame.display.update()
            self.main_clock.tick(self.FPS)


    def check_for_quit(self):
        for event in pygame.event.get((QUIT, KEYUP)):
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()



if __name__ == '__main__':
    try:
        v_oth = VisualOthello()
    except pygame.error as e:
        print(e)
        traceback.print_exc()
        time.sleep(20)

