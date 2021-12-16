'''
This is the main function of the final project.
Calls all necessary code files for the mine sweeper game.

**Imported modules**
    pygame: an open-source module for Python intended to make games and other multimedia applications.
    
**Called files**
    custom.py: Parameters that can be modified by the user.
    objects.py: All necessary objects needed to run the game.
    
@author: Po-I Hsieh, Vina Ro
'''

import pygame
import sys
import time
import custom
import objects

# Call parameters from custom.py
bk_size = custom.bk_size
face_size = custom.face_size

# Size of game window
WIN_WIDTH = custom.Blocks_in_row * bk_size
WIN_HEIGHT = (custom.Blocks_in_column + 2) * bk_size

# Color parameters
bgcolor = (225, 225, 225)
red = (255, 0, 0)
black = (0, 0, 0)

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
    Status = objects.GameStatus.readied
    block = objects.MineBlock()
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
                elif Status == objects.GameStatus.readied:
                    Status = objects.GameStatus.started
                    start_time = time.time()

                # If game is already started, reveal the blocks according to
                # the corresponding events.
                elif Status == objects.GameStatus.started:
                    mineblock = block.getmine(x, y)

                    # If left button is pressed, reveal block.
                    # If the block is a mine, game over.
                    if m_left:
                        if mineblock.status == objects.BlockStatus.normal:
                            if not block.open_mine(x, y):
                                Status = objects.GameStatus.over

                    # If right button is pressed, mark the block as a flag/ask/normal.
                    elif m_right:
                        if mineblock.status == objects.BlockStatus.normal:
                            mineblock.status = objects.BlockStatus.flag
                        elif mineblock.status == objects.BlockStatus.flag:
                            mineblock.status = objects.BlockStatus.ask
                        elif mineblock.status == objects.BlockStatus.ask:
                            mineblock.status = objects.BlockStatus.normal

        # Draw images on all blocks according to their status.
        for row in block.block:
            for spot in row:
                pos = (spot.x * bk_size, (spot.y + 2) * bk_size)
                if spot.status == objects.BlockStatus.opened:
                    WIN.blit(img_dict[spot.mine_surround], pos)
                    revealed_block_count += 1
                elif spot.status == objects.BlockStatus.bomb:
                    WIN.blit(blood, pos)
                elif spot.status == objects.BlockStatus.flag:
                    WIN.blit(flag, pos)
                    flag_count += 1
                elif spot.status == objects.BlockStatus.ask:
                    WIN.blit(ask, pos)
                elif Status == objects.GameStatus.over and spot.value:
                    WIN.blit(mine, pos)
                elif spot.value == 0 and spot.status == objects.BlockStatus.flag:
                    WIN.blit(error, pos)
                elif spot.status == objects.BlockStatus.normal:
                    WIN.blit(blank, pos)

        # Calculate elapsed time and show it on the window.
        if Status == objects.GameStatus.started:
            time_played = int(time.time() - start_time)
        show_text(WIN, font1, 30, (bk_size * 2 - fheight) // 2 - 2,
                  '%02d' % (custom.Total_mine - flag_count), red)
        show_text(WIN, font1, WIN_WIDTH - fwidth - 30, (bk_size *
                  2 - fheight) // 2 - 2, '%03d' % time_played, red)

        # Set requirements to win the game.
        if flag_count + revealed_block_count == custom.Blocks_in_column * custom.Blocks_in_row:
            Status = objects.GameStatus.win

        # Change face image according to the game status.
        if Status == objects.GameStatus.over:
            WIN.blit(failface, (face_pos_x, face_pos_y))
        elif Status == objects.GameStatus.win:
            WIN.blit(successface, (face_pos_x, face_pos_y))
        else:
            WIN.blit(normalface, (face_pos_x, face_pos_y))

        pygame.display.update()


if __name__ == "__main__":
    main()
