'''
Includes functions and classes to generate the minefield and mouse-click events.
 
@author: Po-I Hsieh, Vina Ro
'''

import random
from enum import Enum
import custom

Total_mine = custom.Total_mine
Width = custom.Blocks_in_row
Height = custom.Blocks_in_column


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
        for k in random.sample(range(Width * Height), Total_mine):
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
