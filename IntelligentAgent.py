import random
from BaseAI import BaseAI
import time
import math
#could not figure out how to implement my heuristics correctly... wrote the code for it and weighted but having issues with float multiplication :(
class IntelligentAgent(BaseAI):
	def __init__(self):
		self.start = time.process_time()

	def getMove(self, grid):
	        self.start = time.process_time()
	        move = self.maximize(grid, 0, float('-inf'), float('inf'))[0]
	        moveset = grid.getAvailableMoves()
	        if move == None:
	        	return moveset[0][0]
	        else:
	        	return move

	def maximize(self, grid, depth, alpha, beta):
		if depth > 8 or time.process_time() - self.start > .2:
			return None, 0
		move = None
		utility = float('-inf')
		for options in grid.getAvailableMoves():
			four = .1 * self.minimize(options[1], 2, (2+depth), alpha, beta)
			two = .9 * self.minimize(options[1], 2, (2+depth), alpha, beta)
			util_new = ((four + two)/2)
			if util_new > utility:
				move = options[0]
				utility = util_new
			if utility >= beta:
				break
			if utility > alpha:
				alpha = utility
		return move, utility

	def minimize(self, grid, value, depth, alpha, beta):
		if depth > 8 or time.process_time() - self.start > .2:
			return None, self.heuristics(grid)
		utility = float('inf')
		for options in grid.getAvailableCells():
			temp = grid.clone()
			temp.insertTile(options, value)
			util_new = self.maximize(temp, alpha, beta, (depth+1))[1]
			if util_new < utility:
				utility = util_new
			if utility <= beta:
				break
			else:
				beta = utility
		return utility

	def heuristics(self, grid):
		score = 0
		occupied = 0
		total = 0
		for row in range(len(grid.map)):
			for col in range(len(grid.map[0])):
				cell = grid.map[row][col]
				if cell == 0:
					score += 1
				else:
					occupied += 1
					total += cell
				if row<3 and col <3 and cell >= grid.map[row][col+1]:
					score += 1
					if grid.map[col][row] >= grid.map[col][row+1]:
						score += 1

		average_tile_value = total/occupied
		score += math.log2(average_tile_value)

		return score

