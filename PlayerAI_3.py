import random
import time
import math
from BaseAI_3 import BaseAI

maxTime = 0.22
defaultProbability  = 0.9

class PlayerAI(BaseAI):
    def __init__(self):
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
    def getMove(self, grid):
        # Selects a random move and returns it
        # moveset = grid.getAvailableMoves()
        # return random.choice(moveset)[0] if moveset else None
        # print(moveset)
        # print("Final Result: %d" % self.CalUtility(grid))
        return self.Decision(grid)

    def CalculateTime(self):
        if time.process_time() - self.prevTime > maxTime:

            return True

        return False

    def CalUtility(self, grid):
        empty_room_value = 0
        at_corner_value = 0
        smooth_value = 0
        #max_value = 0
        #max_value = grid.getMaxTile()
        default_weight = [[30, 15, 8, 3],[8, 5, 3, 1],[5, 3, 1, 0],[1, 0, 0, 0]]
        for i in range(grid.size):
            for j in range(grid.size):
                at_corner_value += grid.map[i][j] * default_weight[i][j]
                # if i < 3:
                #     smooth_value += abs(grid.map[i][j] - grid.map[i + 1][j])
                # if j < 3:
                #     smooth_value += abs(grid.map[i][j] - grid.map[i][j + 1])
                try:
                    smooth_value += abs(grid.map[i][j] - grid.map[i + 1][j])
                except:
                    smooth_value += 0
                try:
                    smooth_value += abs(grid.map[i][j] - grid.map[i - 1][j])
                except:
                    smooth_value += 0
                try:
                    smooth_value += abs(grid.map[i][j] - grid.map[i][j + 1])
                except:
                    smooth_value += 0
                try:
                    smooth_value += abs(grid.map[i][j] - grid.map[i][j - 1])
                except:
                    smooth_value += 0
                if grid.map[i][j] == 0:
                    empty_room_value += grid.getMaxTile()
        total_value = at_corner_value + empty_room_value / 16 - smooth_value
        # print(at_corner_value)
        # print(empty_room_value)
        # print(smooth_value)
        # print("\n")
        # print(total_value)
        return total_value

    def Chance(self, grid, alpha, beta, level, limit):
        if level == limit or self.CalculateTime() or grid.canMove()==False:
            return (grid, self.CalUtility(grid))

        result1 = self.Minimize(grid, alpha, beta, self.possibleNewTiles[0], level + 1, limit)
        config1 = result1[0]
        utility1 = result1[1]
        
        result2 = self.Minimize(grid, alpha, beta, self.possibleNewTiles[1], level + 1, limit)
        config2 = result2[0]
        utility2 = result2[1]

        possibleConfig = [result1,result2]
        config = possibleConfig[random.random() > self.probability]
        Utility = utility1 * 0.9 + utility2 * 0.1
        Grid = (config, Utility)
        return Grid



    def Minimize(self, grid, alpha, beta, tile, level, limit):
        if level == limit or self.CalculateTime() or grid.canMove()==False:
            return (grid, self.CalUtility(grid))

        minUtility = float('inf')
        minGrid = (None, minUtility)

        for child in grid.getAvailableCells():
            temp_grid = grid.clone()
            temp_grid.insertTile(child,tile)
            result = self.Maximize(temp_grid, alpha, beta, level + 1, limit)
            config = result[0]
            utility = result[1]

            if utility < minUtility:
                #print(utility)
                minUtility = utility
                minGrid = (config, minUtility)
                #print (minGrid)

            if minUtility <= alpha:
                break

            if minUtility < beta:
                beta = minUtility

        return minGrid

    def Maximize(self, grid, alpha, beta, level, limit):
        if level == limit or self.CalculateTime() or grid.canMove()==False:
            return (grid, self.CalUtility(grid))

        maxUtility = float('-inf')
        maxGrid = (None, maxUtility)

        for child in grid.getAvailableMoves():
            temp_grid = grid.clone()
            temp_grid.move(child[0])
            result = self.Chance(temp_grid, alpha, beta, level + 1, limit)
            config = result[0]
            utility = result[1]

            if utility > maxUtility:
                maxUtility = utility
                maxGrid = (config, maxUtility)

            if maxUtility >= beta:
                break

            if maxUtility > alpha:
                alpha = maxUtility

        return maxGrid

    def Decision(self, grid):
        self.prevTime = time.process_time()
        current_level = 0
        limit = 0
        alpha = float('-inf')
        beta = float('inf')
        maxUtility = float('-inf')
        move_index = None
        while self.CalculateTime() == False:
            limit += 1
            for child in grid.getAvailableMoves():
                temp_grid = grid.clone()
                temp_grid.move(child[0])
                utility = self.Chance(temp_grid, alpha, beta, current_level, limit)[1]
                if utility > maxUtility:
                    maxUtility = utility
                    move_index = child[0]

                if maxUtility >= beta:
                    break

                if maxUtility > alpha:
                    alpha = maxUtility

        return move_index