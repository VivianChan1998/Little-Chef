from enum import Enum

class Stations(Enum):
    NONE = 0
    STOVE = 1
    CHOP = 2
    CONTER = 3
    OBSTACLE = 4
    LETTUCE = 5
    TOMATO = 6
    BUN = 7
    MEAT = 8
    CHEESESPAGHETTI = 9

class Actions(Enum):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    COOK = 5
    CHOP = 6
    PUT = 7
    TAKE = 8
