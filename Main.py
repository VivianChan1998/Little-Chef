from difflib import IS_CHARACTER_JUNK
import numpy as np
import emoji
from Enums import STATUS, STATIONS, ACTIONS
from Food import Food
from User import User
import serial
import queue
import time
import TileCamera
import math
import pygame
import os

IS_CONNECT = True
READ_CV = True
CURR_RECIPE = "HAMBURGER"
TIME_WAIT_S = 0

'''
Global Parameters Init
'''
START_POINT = (6,0)
board = np.full((7,6), STATIONS.NONE)
board[0][5] = STATIONS.FINISH # make sure the location of finish counter
user = User(START_POINT)
tiles = [] # RPi code should break it down into one single array for this code
tile_idx = -1
positions = []
finished = []
status = STATUS.OK
RECIPES = {
    "HAMBURGER": ["BUN", "LETTUCE", "TOMATO", "MEAT"],
    "SALAD": ["LETTUCE", "TOMATO"],
    "MACARONI": ["CHEESE", "SPAGHETTI"]
}
current_recipe = RECIPES[CURR_RECIPE]
ser = ''
cmds = []
COLOR_LIB = {"BUN": "ff4200", "LETTUCE": "00ff00", "TOMATO":"ff0000", "MEAT":"ff1010", "SPAGHETTI":"ffffff", "CHEESE": "ffffe0"}
COLOR_NONE = "000000"

pygame.init()
err_sound = pygame.mixer.Sound(r"ErrorSoundFormatted.wav")
cook_sound = pygame.mixer.Sound(r"CookingSound.wav")
chop_sound = pygame.mixer.Sound(r"ChoppingSound.wav")
put_sound = pygame.mixer.Sound(r"PutSound.wav")
take_sound = pygame.mixer.Sound(r"TakeAction.wav")

#pygame.mixer.music.play()

'''
BFS Function
'''
dRow = [-1, 0, 1,  0];
dCol = [ 0, 1, 0, -1];


def BFS(vis, row, col, pred, dist):
    q = queue.Queue()
    q.put((row, col))
    vis[row][col] = True
    dist[row][col] = 0
    d = 0

    while not q.empty():
        cell = q.get()
        d = dist[cell[0]][cell[1]] + 1
 
        for i in range(4):
            adjx = cell[0] + dRow[i]
            adjy = cell[1] + dCol[i]
 
            if adjx >= 1  and adjx <= 6  and adjy >= 0 and adjy < 6 and (board[adjx][adjy] == STATIONS.NONE or board[adjx][adjy] == STATIONS.INTERACTION) and not vis[adjx][adjy]:
                q.put((adjx, adjy))
                vis[adjx][adjy] = True
                if dist[adjx][adjy] > d:
                    dist[adjx][adjy] = d
                    pred[adjx][adjy] = cell;
            if adjx == 6 and adjy == 0:
                break

interaction_vector = [
    [( 0, 0),( 0, 0),( 0, 0),( 0, 0),( 0, 0),( 1, 0)],
    [( 0, 1),( 1, 0),( 1, 0),( 1, 0),( 1, 0),( 0,-1)],
    [( 0, 1),( 1, 0),( 1, 0),( 1, 0),( 1, 0),( 0,-1)],
    [( 0, 1),( 0, 1),( 0,-1),( 0, 1),( 0,-1),( 0,-1)],
    [( 0, 1),( 0, 1),( 0,-1),( 0, 1),( 0,-1),( 0,-1)],
    [( 0, 1),(-1, 0),(-1, 0),(-1, 0),(-1, 0),( 0,-1)],
    [( 0, 1),(-1, 0),(-1, 0),(-1, 0),(-1, 0),( 0,-1)]] # make sure the location of finish counter

trace_interaction = [
    [( 0, 0),( 0, 0),( 0, 0),( 0, 0),( 0, 0),( 1, 0)],
    [( 0, 1),( 1,-1),(-1, 0),( 1, 0),( 1, 0),( 0,-1)],
    [( 0, 1),( 1,-1),( 1, 0),( 1, 0),( 1, 0),( 0,-1)],
    [( 0, 1),( 0,-1),( 0,-1),( 0, 1),( 0,-1),( 0,-1)],
    [( 0, 1),( 0, 1),( 0,-1),( 0, 1),( 0,-1),( 0,-1)],
    [( 0, 1),(-1, 0),(-1, 0),(-1, 0),( 0,-1),( 0,-1)],
    [( 0, 1),(-1, 0),(-1, 0),(-1, 0),( 0,-1),( 0,-1)]
]

def read_tiles():
    if READ_CV:
        tmp, pos = TileCamera.get_tiles_5()
        print(tmp)
        for i in range(len(tmp)):
            t = tmp[i]
            p = pos[i]
            repeat = 1
            if t == '2' or t == '3' or t == '4':
                repeat = int(t) - 1
                print(repeat)
                if i!=len(tmp)-1:
                    t = tmp[i + 1]
            if t == 'U':
                for l in range(repeat):
                    tiles.append( ACTIONS.UP )
                    positions.append(p)
            elif t == 'D':
                for l in range(repeat):
                    tiles.append( ACTIONS.DOWN)
                    positions.append(p)
            elif t == 'R':
                for l in range(repeat):
                    tiles.append( ACTIONS.RIGHT )
                    positions.append(p)
            elif t == 'L':
                for l in range(repeat):
                    tiles.append( ACTIONS.LEFT )
                    positions.append(p)
            elif t == 'P':
                tiles.append( ACTIONS.PUT )
                positions.append(p)
            elif t == 'T':
                tiles.append( ACTIONS.TAKE )
                positions.append(p)
            elif t == 'K':
                tiles.append( ACTIONS.COOK )
                positions.append(p)
            elif t == 'C':
                tiles.append( ACTIONS.CHOP )
                positions.append(p)
        print('read CV...')
    else:
        tiles.append(ACTIONS.RIGHT)
        tiles.append(ACTIONS.UP)
        tiles.append(ACTIONS.UP)
        tiles.append(ACTIONS.RIGHT)
        tiles.append(ACTIONS.RIGHT)
        tiles.append(ACTIONS.UP)
        tiles.append(ACTIONS.TAKE)
        '''
        tiles.append(ACTIONS.DOWN)
        tiles.append(ACTIONS.RIGHT)
        tiles.append(ACTIONS.COOK)
        tiles.append(ACTIONS.RIGHT)
        tiles.append(ACTIONS.UP)
        tiles.append(ACTIONS.UP)
        tiles.append(ACTIONS.UP)
        tiles.append(ACTIONS.PUT)
        tiles.append(ACTIONS.DOWN)
        '''


def define_board():
    
    board[1][2] = STATIONS.COOK
    board[4][5] = STATIONS.CHOP
    board[4][0] = STATIONS.MEAT
    board[6][5] = STATIONS.LETTUCE
    board[2][0] = STATIONS.BUN
    board[3][3] = STATIONS.OBSTACLE
    board[5][2] = STATIONS.OBSTACLE
    
def return_to_start():
    print('return to start ============ ')
    pred = np.empty((7,6), dtype=object)
    vis = np.zeros((7,6))
    dist = np.full((7,6), 1000)
    BFS(vis, user.location[0], user.location[1], pred, dist)
    path = []
    crawl = (6,0)
    path.append(crawl)
    while pred[crawl] != None:
        path.insert(0, pred[crawl]);
        crawl = pred[crawl];
    print(path)

    for i in range(1, len(path)):
        dirx = path[i][0] - user.location[0]
        diry = path[i][1] - user.location[1]
        user.location = (user.location[0] + dirx, user.location[1] + diry)
        c = "MOVE_" + ('Y' if dirx!=0 else 'X') + ('-1' if diry<0 or dirx<0 else '+1')
        cmds.append(c)
        execute()

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
        if finished[i] != None:
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
        if i == tile_idx:
            print(emoji.emojize(":backhand_index_pointing_down: "), end = '')
        else:
            print("  ", end = '')
    print()
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
            print(emoji.emojize(":grinning_face_with_big_eyes:"), end = '')
        elif tile == ACTIONS.TAKE:
            print(emoji.emojize(":palm_up_hand:"), end = '')
        print(' ', end='')

def get_interacting_station(x, y):
    print(x)
    print(y)
    print(".....")
    if x>6 or x<0 or y>5 or y<0:
        return board[0][0]

    print(x-trace_interaction[x][y][1])
    print(y - trace_interaction[x][y][0])
    sta = board[x - trace_interaction[x][y][0]][y - trace_interaction[x][y][1]]
    
    return sta

def move(dir):
    next_loc_x = user.location[0] + (1 if dir == ACTIONS.DOWN else -1 if dir == ACTIONS.UP else 0)
    next_loc_y = user.location[1] + (1 if dir == ACTIONS.RIGHT else -1 if dir == ACTIONS.LEFT else 0)
    if next_loc_x > 6 or next_loc_x < 1 or next_loc_y > 5 or next_loc_y < 0 or (board[next_loc_x][next_loc_y] != STATIONS.NONE and board[next_loc_x][next_loc_y] != STATIONS.INTERACTION):
        print(next_loc_x, next_loc_y)
        return STATUS.ERR_BUMP
    user.location = (next_loc_x, next_loc_y)
    c = "MOVE_" + ('Y' if dir==ACTIONS.DOWN or dir==ACTIONS.UP else 'X') + ('-1' if dir==ACTIONS.LEFT or dir==ACTIONS.UP else '+1')
    cmds.append(c)
    print(c)
    return STATUS.OK

def cook():
    x = user.location[0]
    y = user.location[1]
    if board[x][y] != STATIONS.INTERACTION:
        return STATUS.ERR_INTERACTION
    s = get_interacting_station(x,y)
    '''
    if s != STATIONS.COOK and user.hold.instructions != "cook":
        return STATUS.ERR_ACTION
    '''
    cmds.append("SOUND_CO")
    return STATUS.OK

def chop():
    x = user.location[0]
    y = user.location[1]
    if board[x][y] != STATIONS.INTERACTION:
        return STATUS.ERR_INTERACTION
    s = get_interacting_station(x,y)
    '''
    if s != STATIONS.CHOP and user.hold.instructions != "chop":
        return STATUS.ERR_ACTION
    '''
    cmds.append("SOUND_CH")
    return STATUS.OK

def take():
    x = user.location[0]
    y = user.location[1]
    if board[x][y] != STATIONS.INTERACTION:
        return STATUS.ERR_INTERACTION
    s = get_interacting_station(x,y)
    print(s)
    '''
    if s.value > 10 or s.value < 5:
        print(s)
        return STATUS.ERR_ACTION
    '''
    user.hold = Food(s.value)
    user.isHolding = True
    cmds.append("SOUND_TA")
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
    cmds.append("SOUND_PU")
    return STATUS.OK

def reach_end():
    for ingredients in current_recipe:
        if ingredients not in finished:
            return STATUS.ERR_INCOMPLETE
    if len(current_recipe) != len(finished):
        return STATUS.ERR_INCOMPLETE
    print("end")
    return STATUS.OK

def check_err_execute():
    if status != STATUS.OK:
        print(emoji.emojize(":angry_face_with_horns: "), end='')
        print(status)
        print()
        cmds.append("SOUND_ERR") #TEMP
        
        execute()
        return_to_start()
        return False
    execute()
    return True

def execute():
    key = ''
    print(cmds)
    if(IS_CONNECT):
        send_wait_cmd(ser)
    else:
        key = input("------- press enter to continue... -------")
    cmds.clear()
    return key

def send_wait_cmd(ser):
    print("--------- handeling cmd ---------")
    # LED_T -> LED_B -> MOVE
    for c in cmds:
        print(c)
        if c[0] == 'S':
            print("SOUND")
            if c == "SOUND_ERR":
                pygame.mixer.Sound.play(err_sound)
            elif c == "SOUND_CO":
                pygame.mixer.Sound.play(cook_sound)
            elif c == "SOUND_CH":
                pygame.mixer.Sound.play(chop_sound)
            elif c == "SOUND_TA":
                pygame.mixer.Sound.play(take_sound)
            elif c == "SOUND_PU":
                pygame.mixer.Sound.play(put_sound)
        else:
            ser.write(c.encode('utf-8'))
            line = ""
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').rstrip()
                    print(line)
                    if line == "DONE":
                        break
    print("------------ cmd done ------------")
        
def wait_for_button():
    while True:
        if(IS_CONNECT):
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
                if line == "BUTTON":
                    cmds.append("E")
                    break
        else:
            key = input("type start >>> ")
            if key == 'start':
                break

if __name__ == "__main__":

    if(IS_CONNECT):
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()

    print("\n\n========= MAKING: " + CURR_RECIPE + " =========")

    define_board()
    add_interaction_area()
    

    while True:

        wait_for_button()

        user = User(START_POINT)
        tiles.clear()
        tile_idx = -1
        finished.clear()

        read_tiles()
        print_actions(-1)
        print_board()
        print(tiles)
        print(tile_idx)

        for t in tiles:

            tile_idx += 1
            t = tiles[tile_idx]
            p = positions[tile_idx]
            print(t)

            print(p)

            cmds.append("LEDT_" + str(math.floor(p[0]/2)) + str(p[1]))
            
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
            
            cmds.append("LEDB_" + (COLOR_NONE if not user.isHolding else COLOR_LIB[user.hold.name]))

            print_actions(tile_idx)
            print_board()

            if not check_err_execute():
                cmds.append("LEDB_" + COLOR_NONE)
                break
            print("\n WAITING.... \n")
            time.sleep(TIME_WAIT_S)

        if tile_idx == len(tiles) -1:
            status = reach_end()
            cmds.append("LEDB_" + COLOR_NONE)
            check_err_execute()
