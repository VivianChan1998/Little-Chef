import numpy as np
import emoji
from Enums import STATUS, STATIONS, ACTIONS
from Food import Food
from User import User

READ_CV = False
CURR_RECIPE = "HAMBURGER"

'''
Global Parameters Init
'''
START_POINT = (6,0)
board = np.full((7,6), STATIONS.NONE)
board[0][5] = STATIONS.FINISH # make sure the location of finish counter
user = User(START_POINT)
tiles = np.full(100, ACTIONS.NONE) # RPi code should break it down into one single array for this code
tile_idx = -1
finished = []
status = STATUS.OK
RECIPES = {
    "HAMBURGER": ["BUN", "LETTUCE", "TOMATO", "MEAT"],
    "SALAD": ["LETTUCE", "TOMATO"],
    "MACARONI": ["CHEESE", "SPAGHETTI"]
}
current_recipe = RECIPES[CURR_RECIPE]

interaction_vector = [
    [( 0, 0),( 0, 0),( 0, 0),( 0, 0),( 0, 0),( 1, 0)],
    [( 0, 1),( 1, 0),( 1, 0),( 1, 0),( 1, 0),( 0,-1)],
    [( 0, 1),( 1, 0),( 1, 0),( 1, 0),( 1, 0),( 0,-1)],
    [( 0, 1),( 0, 1),( 0,-1),( 0, 1),( 0,-1),( 0,-1)],
    [( 0, 1),( 0, 1),( 0,-1),( 0, 1),( 0,-1),( 0,-1)],
    [( 0, 1),(-1, 0),(-1, 0),(-1, 0),(-1, 0),( 0,-1)],
    [( 0, 1),(-1, 0),(-1, 0),(-1, 0),(-1, 0),( 0,-1)]] # make sure the location of finish counter

def read_tiles(isRead):
    if READ_CV:
        #TODO
        print('read CV...')
    else:
        tiles[0] = ACTIONS.RIGHT
        tiles[1] = ACTIONS.UP
        tiles[2] = ACTIONS.UP
        tiles[3] = ACTIONS.RIGHT
        tiles[4] = ACTIONS.RIGHT
        tiles[5] = ACTIONS.UP
        tiles[6] = ACTIONS.TAKE
        tiles[7] = ACTIONS.DOWN
        tiles[8] = ACTIONS.RIGHT
        tiles[9] = ACTIONS.COOK
        tiles[10] = ACTIONS.RIGHT
        tiles[11] = ACTIONS.UP
        tiles[12] = ACTIONS.UP
        tiles[13] = ACTIONS.UP
        tiles[14] = ACTIONS.PUT
        tiles[15] = ACTIONS.DOWN


def define_board():
    #TODO
    board[5][4] = STATIONS.COOK
    board[2][3] = STATIONS.MEAT
    
def return_to_start():
    print('return to start')
    #TODO

def add_interaction_area():
    for i in range(7):
        for j in range(6):
            if board[i][j] != STATIONS.NONE and board[i][j] != STATIONS.INTERACTION and board[i][j] != STATIONS.OBSTACLE:
                interaction_loc = (i + interaction_vector[i][j][0], j + interaction_vector[i][j][1])
                board[interaction_loc[0]][interaction_loc[1]] = STATIONS.INTERACTION
    return 0

def print_board():
    print('\n_________________________\n')
    print("user hold: ", end=' ')
    if user.isHolding:
        print(user.hold.name)
    else:
        print("None")
    print("finished:", end=' ')
    for i in range(len(finished)):
        print(finished[i].name + ' ')
    print()


    for j in range(6):
        tmp = str(board[0][j])[9:12]
        if tmp == "NON":
            print(' ' + '   ', end = '' if j!=5 else '\n')
        else:
            print('|' + tmp + '|', end = '' if j!=5 else '\n')
    for i in range(1,7):
        for j in range(6):
            if user.location[0] == i and user.location[1] == j:
                print ('|_O_', end = '' if j!=5 else '|\n')
            else:
                tmp = str(board[i][j])[9:12]
                if tmp == "NON":
                    print('|___', end = '' if j!=5 else '|\n')
                elif tmp == "INT":
                    print('|+++', end = '' if j!=5 else '|\n')
                else:
                    print('|' + tmp, end = '' if j!=5 else '|\n')
    
    print('_________________________\n')

def print_actions(tile_idx):
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

def get_interacting_station(x, y):
    print("here")
    print((x - interaction_vector[y][x][1], y - interaction_vector[y][x][0]))
    return board[x - interaction_vector[y][x][1]][y - interaction_vector[y][x][0]]

def move(dir):
    next_loc_x = user.location[0] + (1 if dir == ACTIONS.DOWN else -1 if dir == ACTIONS.UP else 0)
    next_loc_y = user.location[1] + (1 if dir == ACTIONS.RIGHT else -1 if dir == ACTIONS.LEFT else 0)
    if next_loc_x > 6 or next_loc_x < 1 or next_loc_y > 5 or next_loc_y < 0 or (board[next_loc_x][next_loc_y] != STATIONS.NONE and board[next_loc_x][next_loc_y] != STATIONS.INTERACTION):
        print(next_loc_x, next_loc_y)
        return STATUS.ERR_BUMP
    user.location = (next_loc_x, next_loc_y)
    return STATUS.OK

def cook():
    x = user.location[0]
    y = user.location[1]
    if board[x][y] != STATIONS.INTERACTION:
        return STATUS.ERR_INTERACTION
    s = get_interacting_station(x,y)
    print(s)
    if s != STATIONS.COOK and user.hold.instructions != "cook":
        return STATUS.ERR_ACTION
    return STATUS.OK

def chop():
    x = user.location[0]
    y = user.location[1]
    if board[x][y] != STATIONS.INTERACTION:
        return STATUS.ERR_INTERACTION
    s = get_interacting_station(x,y)
    if s != STATIONS.CHOP and user.hold.instructions != "chop":
        return STATUS.ERR_ACTION
    return STATUS.OK

def take():
    x = user.location[0]
    y = user.location[1]
    if board[x][y] != STATIONS.INTERACTION:
        return STATUS.ERR_INTERACTION
    s = get_interacting_station(x,y)
    if s.value > 10 or s.value < 5:
        return STATUS.ERR_ACTION
    user.hold = Food(s.value)
    user.isHolding = True
    return STATUS.OK

def put():
    x = user.location[0]
    y = user.location[1]
    if board[x][y] != STATIONS.INTERACTION:
        return STATUS.ERR_INTERACTION
    if (x,y) != (1,5):
        return STATUS.ERR_ACTION
    finished.append(user.hold)
    user.hold = None
    user.isHolding = False
    return STATUS.OK

def reach_end():
    #TODO
    #unfinish
    #wrong thing or more thing?
    return STATUS.OK


if __name__ == "__main__":

    print("\n\n========= MAKING: " + CURR_RECIPE + " =========")

    define_board()
    add_interaction_area()
    read_tiles(READ_CV)
    print_actions(-1)
    print_board()

    for idx,t in enumerate(tiles):
        if wait_next() == '':
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

            print_actions(idx)
            print_board()

            if status != STATUS.OK:
                print(emoji.emojize(":angry_face_with_horns: "), end='')
                print(status)
                print()
                return_to_start()
    reach_end()