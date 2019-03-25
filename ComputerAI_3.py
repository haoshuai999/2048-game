import random
from BaseAI_3 import BaseAI

class ComputerAI(BaseAI):
    def getMove(self, grid):
        """ Returns a randomly selected cell if possible """
        cells = grid.getAvailableCells()
        return random.choice(cells) if cells else None