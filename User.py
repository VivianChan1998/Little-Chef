from Enums import Actions

class User:
    def __init__(self):
        self.location = (0,0)
        self.action = Actions.NONE
        self.hold = None
        self.isHolding = False