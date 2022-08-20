from Enums import ACTIONS

class User:
    def __init__(self, start_loc):
        self.location = start_loc
        self.hold = None
        self.isHolding = False