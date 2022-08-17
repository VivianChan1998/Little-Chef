from nis import match
import numpy as np
import emoji
from Enums import STATUS, STATIONS, ACTIONS
import Food
from User import User

'''
Global Parameters Init
'''
board = np.full((7,6), STATIONS.NONE)
board[6,3] = STATIONS.FINISH # make sure the location of finish counter
user = User()
tiles = np.full(100, ACTIONS.NONE) # RPi code should break it down into one single array for this code
tile_idx = -1
finished = []
status = STATUS.OK

'''
TEMP
'''
board[5][4] = STATIONS.STOVE 
board[2][3] = STATIONS.MEAT
tiles[0] = ACTIONS.RIGHT
tiles[1] = ACTIONS.DOWN
tiles[2] = ACTIONS.UP
tiles[3] = ACTIONS.RIGHT
tiles[4] = ACTIONS.RIGHT
tiles[5] = ACTIONS.CHOP
tiles[6] = ACTIONS.DOWN
tiles[7] = ACTIONS.DOWN
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
        if tiles[i] == ACTIONS.NONE:
            print()
            break
        if i == tile_idx:
            print(emoji.emojize(":backhand_index_pointing_down: "), end = '')
        else:
            print("  ", end = '')
    for i in range(len(tiles)):
        if tiles[i] == ACTIONS.NONE:
            break
        tile = tiles[i]
        if tile == ACTIONS.UP:
            print(emoji.emojize(":up_arrow:"), end = '')
        elif tile == ACTIONS.DOWN:
            print(emoji.emojize(":down_arrow:"), end = '')
        elif tile == ACTIONS.LEFT:
            print(emoji.emojize(":left_arrow:"), end = '')
        elif tile == ACTIONS.RIGHT:
            print(emoji.emojize(":right_arrow:"), end = '')
        elif tile == ACTIONS.COOK:
            print(emoji.emojize(":cooking:"), end = '')
        elif tile == ACTIONS.CHOP:
            print(emoji.emojize(":kitchen_knife:"), end = '')
        elif tile == ACTIONS.PUT:
            print(emoji.emojize(":palm_down_hand:"), end = '')
        elif tile == ACTIONS.TAKE:
            print(emoji.emojize(":palm_up_hand:"), end = '')
        print(' ', end='')


def wait_next():
    key = input("press enter to continue...") #TEMP
    # RPi-todo: return true when motor stuff done
    return key


def move(dir):
    next_loc_x = user.location[0] + (1 if dir == ACTIONS.DOWN else -1 if dir == ACTIONS.UP else 0)
    next_loc_y = user.location[1] + (1 if dir == ACTIONS.RIGHT else -1 if dir == ACTIONS.LEFT else 0)
    if next_loc_x > 5 or next_loc_x < 0 or next_loc_y > 5 or next_loc_y < 0 or board[next_loc_x][next_loc_y] != STATIONS.NONE:
        return STATUS.ERR_BUMP
    user.location = (next_loc_x, next_loc_y)
    return STATUS.OK

def cook():
    #TODO determine error and return status
    return STATUS.OK

def chop():
    #TODO determine error and return status
    return STATUS.OK

def take():
    #TODO determine error and return status
    #user.hold = ....
    return STATUS.OK

def put():
    #TODO determine error and return status
    return STATUS.OK

if __name__ == "__main__":

    print_actions()
    print_board()

    while True:
        if wait_next() == '':
            tile_idx += 1
            t = tiles[tile_idx]
            if t == ACTIONS.UP or t == ACTIONS.DOWN or t == ACTIONS.LEFT or t == ACTIONS.RIGHT:
                status = move(t)
            elif t == ACTIONS.COOK:
                status = cook()
            elif t == ACTIONS.CHOP:
                status = chop()
            elif t == ACTIONS.TAKE:
                status = take()
            elif t == ACTIONS.PUT:
                status = put()

            print_actions()
            print_board()

            if status != STATUS.OK:
                print(emoji.emojize(":angry_face_with_horns: "), end='')
                print(status)
                print()
                exit() # TEMP
        