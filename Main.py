from argparse import Action
import numpy as np
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
counter = []

'''
TEMP
'''
board[5][4] = Stations.STOVE 
board[2][3] = Stations.MEAT
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




if __name__ == "__main__":
    print_board()