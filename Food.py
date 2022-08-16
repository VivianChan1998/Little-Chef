class Food:
    def __init__(self, foodName, instructions, isPreped = False):
        self.foodName = foodName
        self.instructions = instructions
        self.isPreped = isPreped
    def PrepFood(self):
        self.isPreped = True