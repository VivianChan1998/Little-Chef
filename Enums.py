from enum import Enum

class STATIONS(Enum):
    NONE = 0
    STOVE = 1
    CHOP = 2
    FINISH = 3
    OBSTACLE = 4
    LETTUCE = 5
    TOMATO = 6
    BUN = 7
    MEAT = 8
    CHEESE = 9
    SPAGHETTI = 10
    INTERACTION = 20

class ACTIONS(Enum):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    COOK = 5
    CHOP = 6
    PUT = 7
    TAKE = 8

class STATUS(Enum):
    ERR_BUMP = 0
    ERR_INTERACTION = 1
    ERR_ACTION = 2
    ERR_INCOMPLETE = 3
    OK = 4