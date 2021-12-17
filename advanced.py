'''
This is the main function of the final project.
Calls all necessary code files for the mine sweeper game.

**Imported modules**
    pygame: an open-source module for Python intended to make games and other multimedia applications.
    
**Called files**
    custom.py: Parameters that can be modified by the user.
    
@author: Po-I Hsieh, Vina Ro
'''

import pygame
import sys
import time
import custom
import random
from enum import Enum

# Call parameters from custom.py
bk_size = custom.bk_size
face_size = custom.face_size
Width = custom.Blocks_in_row
Height = custom.Blocks_in_column


# Size of game window
WIN_WIDTH = custom.Blocks_in_row * bk_size
WIN_HEIGHT = (custom.Blocks_in_column + 2) * bk_size

# Color parameters
bgcolor = (225, 225, 225)
red = (255, 0, 0)
black = (0, 0, 0)
slategrey = (112, 128, 144)
lightgrey = (165, 175, 185)
blackish = (10, 10, 10)


# Load images then scale image
mine0_image = pygame.image.load('assets/0.bmp')
mine0 = pygame.transform.scale(mine0_image, (bk_size, bk_size))
mine1_image = pygame.image.load('assets/1.bmp')
mine1 = pygame.transform.scale(mine1_image, (bk_size, bk_size))
mine2_image = pygame.image.load('assets/2.bmp')
mine2 = pygame.transform.scale(mine2_image, (bk_size, bk_size))
mine3_image = pygame.image.load('assets/3.bmp')
mine3 = pygame.transform.scale(mine3_image, (bk_size, bk_size))
mine4_image = pygame.image.load('assets/4.bmp')
mine4 = pygame.transform.scale(mine4_image, (bk_size, bk_size))
mine5_image = pygame.image.load('assets/5.bmp')
mine5 = pygame.transform.scale(mine5_image, (bk_size, bk_size))
mine6_image = pygame.image.load('assets/6.bmp')
mine6 = pygame.transform.scale(mine6_image, (bk_size, bk_size))
mine7_image = pygame.image.load('assets/7.bmp')
mine7 = pygame.transform.scale(mine7_image, (bk_size, bk_size))
mine8_image = pygame.image.load('assets/8.bmp')
mine8 = pygame.transform.scale(mine8_image, (bk_size, bk_size))
blank_image = pygame.image.load('assets/blank.bmp')
blank = pygame.transform.scale(blank_image, (bk_size, bk_size))
flag_image = pygame.image.load('assets/flag.bmp')
flag = pygame.transform.scale(flag_image, (bk_size, bk_size))
ask_image = pygame.image.load('assets/ask.bmp')
ask = pygame.transform.scale(ask_image, (bk_size, bk_size))
mine_image = pygame.image.load('assets/mine.bmp')
mine = pygame.transform.scale(mine_image, (bk_size, bk_size))
blood_image = pygame.image.load('assets/blood.bmp')
blood = pygame.transform.scale(blood_image, (bk_size, bk_size))
error_image = pygame.image.load('assets/error.bmp')
error = pygame.transform.scale(error_image, (bk_size, bk_size))
failface_image = pygame.image.load('assets/face_fail.bmp')
failface = pygame.transform.scale(failface_image, (face_size, face_size))
normalface_image = pygame.image.load('assets/face_normal.bmp')
normalface = pygame.transform.scale(normalface_image, (face_size, face_size))
successface_image = pygame.image.load('assets/face_success.bmp')
successface = pygame.transform.scale(successface_image, (face_size, face_size))

# Position of the yellow face image
face_pos_x = (WIN_WIDTH - face_size) // 2
face_pos_y = (bk_size * 2 - face_size) // 2

# Dictionary for matching the number image to the count of surrounding mines
img_dict = {
    0: mine0,
    1: mine1,
    2: mine2,
    3: mine3,
    4: mine4,
    5: mine5,
    6: mine6,
    7: mine7,
    8: mine8
}

# Initializing of the game.
# 1. Set window size
# 2. Set window caption
pygame.init()
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Minesweeper")

# Set font
font1 = pygame.font.Font('assets/a.TTF', bk_size * 2)
fwidth, fheight = font1.size('999')
font2 = pygame.font.SysFont('comicsans', 12)
font3 = pygame.font.Font(None, 32)

class BlockStatus(Enum):
    '''
    This enumeration is a set of symbolic names bound to unique, 
    constant values that describes the status of one block.

    The block can be
    'normal'--unonpened
    'opened'--opened block
    'mine'--block that contains a mine
    'flag'--block that was flagged by the user
    'ask'--block that was put a question mark on by the user
    'bomb'--block with mine that was opened by the user
    '''
    normal = 1
    opened = 2
    mine = 3
    flag = 4
    ask = 5
    bomb = 6


class GameStatus(Enum):
    '''
    This enumeration is a set of symbolic names bound to unique, 
    constant values that describes the current status of the game.

    The game can be
    'readied'--The user has not started opening any blocks
    'started'--The user has started the game by opening one block.
    'over'--The user has opened a block containing a mine.
    'win'--The user has successfully opened all blocks without a bomb.
    '''
    readied = 1
    started = 2
    over = 3
    win = 4


def cor_surround(x, y):
    '''
    This is a function that returns a list of surrounding coordinates of (x, y)

    **Parameters**
        x: *int*
            x coordinate
        y: *int*
            y coordinate

    **Returns**
        list of all surrounding coordinates within the grid.
    '''
    return [(i, j) for i in range(max(0, x - 1), min(Width - 1, x + 1) + 1)
            for j in range(max(0, y - 1), min(Height - 1, y + 1)+1) if i != x or j != y]


class Mine:
    '''
    Getting and setting the properties of a block using property class.
    '''

    def __init__(self, x, y, value=0):
        '''
        This function initializes the block.

        **Parameters**
            x: *int*
                x coordinate
            y: *int*
                y coordinate
            value: status of block(0=blank, 1=mine) 
            mine_surround: the number of surrounding mines of the block
            status: current status of block operated by the user
            set_value(value): setting the status of the block(0 or 1)
        '''
        self._x = x
        self._y = y
        self._value = 0
        self._mine_surround = -1
        self._status = BlockStatus.normal
        self.set_value(value)

    def __repr__(self):
        '''
        This function converts the object to a string.
        '''
        return str(self._value)

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x
    x = property(fget=get_x, fset=set_x)

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y
    y = property(fget=get_y, fset=set_y)

    def get_value(self):
        return self._value

    def set_value(self, value):
        if value:
            self._value = 1
        else:
            self._value = 0
    value = property(fget=get_value, fset=set_value, doc='0:blank 1:mine')

    def get_mine_surround(self):
        return self._mine_surround

    def set_mine_surround(self, mine_surround):
        self._mine_surround = mine_surround
    mine_surround = property(
        fget=get_mine_surround, fset=set_mine_surround, doc='surrounding mine count')

    def get_status(self):
        return self._status

    def set_status(self, value):
        self._status = value
    status = property(fget=get_status, fset=set_status, doc='Block status')


class MineBlock:
    '''
    This class contains the algorithm of the mine sweeper game.
    '''

    def __init__(self):
        '''
        This function initializes the block and buries mines in the block. 
        '''
        self._block = [[Mine(i, j) for i in range(Width)]
                       for j in range(Height)]

        # Bury mines
        for k in random.sample(range(Width * Height), int(num)):
            self._block[k // Width][k % Width].value = 1

    def get_block(self):
        return self._block
    block = property(fget=get_block)

    def getmine(self, x, y):
        return self._block[y][x]

    def open_mine(self, x, y):
        '''
        **Parameters**
            x : *int*
                x coordinate of current block.
            y : *int*
                y coordinate of current block.
        **Returns**
            bool
        '''
        # When stepped on mine, change status to bomb.
        if self._block[y][x].value:
            self._block[y][x].status = BlockStatus.bomb
            return False

        # First set status to opened.
        self._block[y][x].status = BlockStatus.opened

        surround = cor_surround(x, y)

        # The sum of surrounding mines
        sum_mine_surround = 0
        for i, j in surround:
            if self._block[j][i].value:
                sum_mine_surround += 1
        self._block[y][x].mine_surround = sum_mine_surround

        # If surrounding mines count==0, open all blocks without mines.
        if sum_mine_surround == 0:
            for i, j in surround:
                if self._block[j][i].mine_surround == -1:
                    self.open_mine(i, j)

        return True

def start_screen():
    '''
    This function draws the start screen. 
    '''
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    startText = font3.render("Welcome! Enter the total number of mines you want:", True, slategrey)
    hopkins_logo = pygame.image.load("hopkins.png")
    input_box = pygame.Rect(100, 100, 30, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        global num
                        num = text
                        text = ''
                        main()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((255,255,255))
        # Render the current text.
        txt_surface = font3.render(text, True, color)
        # Blit the text and images.
        screen.blit(hopkins_logo, (WIN_WIDTH * .075, WIN_HEIGHT * .45))
        screen.blit(startText, ((WIN_WIDTH - startText.get_width()) / 2, 70))
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        

def draw_window():
    '''
    Function that place images and text in window.
    '''
    WIN.fill(bgcolor)
    course_name = font2.render("Software Carpentry", 1, black)
    editors_name = font2.render("Editors: Po-I & Vina", 1, black)
    WIN.blit(course_name, (WIN_WIDTH / 4 - 50, bk_size - 6))
    WIN.blit(editors_name, (WIN_WIDTH * 3 / 4 - 100, bk_size - 6))


def show_text(WIN, font, x, y, text, fcolor):
    '''
    Function that refreshes text(stopwatch, number of mines) in window.
    '''
    imgText = font.render(text, True, fcolor)
    WIN.blit(imgText, (x, y))


def main():
    '''
    Function that runs our game.
    '''
    Status = GameStatus.readied
    block = MineBlock()
    time_played = 0
    run = True
    while run:
        draw_window()
        flag_count = 0
        revealed_block_count = 0

        for event in pygame.event.get():
            # If the user closes the window, terminate code
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            # When the user presses the mouse button,
            # get the position of the cursor.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x = mouse_x // bk_size
                y = mouse_y // bk_size - 2
                m_left, m_middle, m_right = pygame.mouse.get_pressed()

            # When the user releases the mouse button,
            # reveal block
            elif event.type == pygame.MOUSEBUTTONUP:

                # When the yellow face is pressed, restart game
                if (mouse_x in range(face_pos_x, face_pos_x + face_size) and
                        mouse_y in range(face_pos_y, face_pos_y + face_size)):
                    main()

                # Start game and start the stopwatch
                elif Status == GameStatus.readied:
                    Status = GameStatus.started
                    start_time = time.time()

                # If game is already started, reveal the blocks according to
                # the corresponding events.
                elif Status == GameStatus.started:
                    mineblock = block.getmine(x, y)

                    # If left button is pressed, reveal block.
                    # If the block is a mine, game over.
                    if m_left:
                        if mineblock.status == BlockStatus.normal:
                            if not block.open_mine(x, y):
                                Status = GameStatus.over

                    # If right button is pressed, mark the block as a flag/ask/normal.
                    elif m_right:
                        if mineblock.status == BlockStatus.normal:
                            mineblock.status = BlockStatus.flag
                        elif mineblock.status == BlockStatus.flag:
                            mineblock.status = BlockStatus.ask
                        elif mineblock.status == BlockStatus.ask:
                            mineblock.status = BlockStatus.normal

        # Draw images on all blocks according to their status.
        for row in block.block:
            for spot in row:
                pos = (spot.x * bk_size, (spot.y + 2) * bk_size)
                if spot.status == BlockStatus.opened:
                    WIN.blit(img_dict[spot.mine_surround], pos)
                    revealed_block_count += 1
                elif spot.status == BlockStatus.bomb:
                    WIN.blit(blood, pos)
                elif spot.status == BlockStatus.flag:
                    WIN.blit(flag, pos)
                    flag_count += 1
                elif spot.status == BlockStatus.ask:
                    WIN.blit(ask, pos)
                elif Status == GameStatus.over and spot.value:
                    WIN.blit(mine, pos)
                elif spot.value == 0 and spot.status == BlockStatus.flag:
                    WIN.blit(error, pos)
                elif spot.status == BlockStatus.normal:
                    WIN.blit(blank, pos)

        # Calculate elapsed time and show it on the window.
        if Status == GameStatus.started:
            time_played = int(time.time() - start_time)
        show_text(WIN, font1, 30, (bk_size * 2 - fheight) // 2 - 2,
                  '%02d' % (int(num) - flag_count), red)
        show_text(WIN, font1, WIN_WIDTH - fwidth - 30, (bk_size *
                  2 - fheight) // 2 - 2, '%03d' % time_played, red)

        # Set requirements to win the game.
        if flag_count + revealed_block_count == 16 * 30:
            Status = GameStatus.win

        # Change face image according to the game status.
        if Status == GameStatus.over:
            WIN.blit(failface, (face_pos_x, face_pos_y))
        elif Status == GameStatus.win:
            WIN.blit(successface, (face_pos_x, face_pos_y))
        else:
            WIN.blit(normalface, (face_pos_x, face_pos_y))

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    start_screen()
    pygame.quit()

