import numpy as np
import emoji
from Enums import Stations
from Enums import Actions
import Food
from User import User

'''
Global Parameters Init
'''
board = np.full((7,6), Stations.NONE)
board[6,3] = Stations.FINISH # make sure the location of finish counter
user = User()
tiles = np.full(100, Actions.NONE) # RPi code should break it down into one single array for this code
tile_idx = -1
finished = []

'''
TEMP
'''
board[5][4] = Stations.STOVE 
board[2][3] = Stations.MEAT
tiles[0] = Actions.LEFT
tiles[1] = Actions.DOWN
tiles[2] = Actions.UP
tiles[3] = Actions.RIGHT
tiles[4] = Actions.COOK
tiles[5] = Actions.CHOP
tiles[6] = Actions.PUT
tiles[7] = Actions.TAKE

''''''

def print_board():
    print('\n_________________________\n')
    for i in range(6):
        for j in range(6):
            if user.location[0] == i and user.location[1] == j:
                print ('|_O_', end = '' if j!=5 else '|\n')
            else:
                tmp = str(board[i][j])[9:12]
                if tmp == "NON":
                    print('|___', end = '' if j!=5 else '|\n')
                else:
                    print('|' + tmp, end = '' if j!=5 else '|\n')
    for j in range(6):
        tmp = str(board[6][j])[9:12]
        if tmp == "NON":
            print(' ' + '   ', end = '' if j!=5 else '\n')
        else:
            print('|' + tmp + '|', end = '')
    print('_________________________\n')

def print_actions():
    for i in range(len(tiles)):
        if tiles[i] == Actions.NONE:
            print()
            break
        if i == tile_idx:
            print(emoji.emojize(":backhand_index_pointing_down: "), end = '')
        else:
            print("  ", end = '')
    for i in range(len(tiles)):
        if tiles[i] == Actions.NONE:
            break
        tile = tiles[i]
        if tile == Actions.UP:
            print(emoji.emojize(":up_arrow:"), end = '')
        elif tile == Actions.DOWN:
            print(emoji.emojize(":down_arrow:"), end = '')
        elif tile == Actions.LEFT:
            print(emoji.emojize(":left_arrow:"), end = '')
        elif tile == Actions.RIGHT:
            print(emoji.emojize(":right_arrow:"), end = '')
        elif tile == Actions.COOK:
            print(emoji.emojize(":cooking:"), end = '')
        elif tile == Actions.CHOP:
            print(emoji.emojize(":kitchen_knife:"), end = '')
        elif tile == Actions.PUT:
            print(emoji.emojize(":palm_down_hand:"), end = '')
        elif tile == Actions.TAKE:
            print(emoji.emojize(":palm_up_hand:"), end = '')
        print(' ', end='')



def wait_next():
    key = input("press enter to continue...")
    # RPi-todo: return true when motor stuff done
    return key


if __name__ == "__main__":
    while True:
        if wait_next() == '':
            print_actions()
            print_board()