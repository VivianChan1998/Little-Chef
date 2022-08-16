from argparse import Action
import numpy as np
from Enums import Stations
from Enums import Actions
import Food
from User import User

'''
Global Parameters Init
'''
board = np.full((6,6), Stations.NONE)
user = User()
finish_counter = []

if __name__ == "__main__":
    print("Hello")