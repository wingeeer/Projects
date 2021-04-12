
import heapq
from collections import deque
from PIL import Image, ImageDraw


class Cell():
	#Class for each cell (1x1) of the board with parameters: 
	# x - the x coordinate of the cell
	# y - the y coordinate of the cell
	# parent - allows relations between the cells on a path
	# g - cost from start cell to current cell
	# h - heuristic cost from current cell to goal cell
	# f = g + h - the expected cost function
	def __init__(self, x, y, value):
		self.value = value
		self.x = x
		self.y = y
		self.parent = None
		self.g = 0
		self.h = 0
		self.f = 0

	#Override of < to make heap work properly
	def __lt__(self, other):
		return self.f < other.f

class AStar():
	#The main class of the algorithm with parameters:
	#
	#
	#
	#
	#
	#
	#
	#
	def __init__(self):
		self.opened = []
		if (alg == 2):
			self.opened = deque(self.opened)
		else:
			heapq.heapify(self.opened)
		self.closed = set()
		self.cells = []
		self.grid_height = 0
		self.grid_width = 0
		self.start = None
		self.goal = None

	def get_closed(self):
		return self.closed

	def get_opened(self):
		tmp = []
		for cell in self.opened:
			tmp.append(cell[1])
		return tmp

	#Initialize the grid from the txt-file
	def init_grid(self):
		with open(filename) as f:
			grid = f.read().splitlines()
		self.grid_width = len(grid)
		self.grid_height = len(grid[0])
		start = []
		goal = []
		for x in range(self.grid_width):
			for y in range(self.grid_height):
				ch = grid[x][y]
				if(ch=='w'):
					value = 100
				elif(ch=='m'):
					value = 50
				elif(ch=='f'):
					value = 10
				elif(ch=='g'):
					value = 5
				elif(ch=='r'):
					value = 1
				elif (ch == "A"):
					start = [x,y]
				elif (grid[x][y] == "B"):
					goal = [x,y]
				self.cells.append(Cell(x, y, value))
		self.start = self.get_cell(start[0],start[1])
		self.goal = self.get_cell(goal[0],goal[1])

	def get_cell(self, x, y):
		#return the cell object corresponding to a given coordinate.
		return self.cells[x * self.grid_height + y]

	def get_heuristic(self, cell):
		if (alg == 3):
			#Dijkstra
			return 0
		else:
			return (abs(cell.x - self.goal.x) + abs(cell.y - self.goal.y))

	def get_neighbours(self, cell):
		#return list of neighbouring cells clockwise starting from the rightmost one
		cells = []
		if cell.x < self.grid_width-1:
			cells.append(self.get_cell(cell.x+1, cell.y))
		if cell.y > 0:
			cells.append(self.get_cell(cell.x, cell.y-1))
		if cell.x > 0:
			cells.append(self.get_cell(cell.x-1, cell.y))
		if cell.y < self.grid_height-1:
			cells.append(self.get_cell(cell.x, cell.y+1))
		return cells

	def display_path(self):
		#Keep track of the path
		cell = self.goal
		while cell.parent is not self.start:
			cell = cell.parent
			#print('path: cell: %d,%d' % (cell.x, cell.y))
			pathList.append((cell.x, cell.y))

	def update_cell(self, adj, cell):
		#given a cell and a neighbour, update the neighbours expected cost and give parent-child relation between them
		adj.g = cell.g + adj.value
		adj.h = self.get_heuristic(adj)
		adj.parent = cell
		adj.f = adj.g + adj.h 
	
	def process(self):
		self.init_grid()
		#Start node is added to open heap queue or queue
		if (alg == 2):
			self.opened.append((self.start.f, self.start))
		else:
			heapq.heappush(self.opened, (self.start.f, self.start))
		#main loop invariant - continues as long as there are opened cells
		while (len(self.opened)):
			#pop the first element from the heap, i.e. the cell with lowest f value.
			if (alg == 2):
				f, cell = self.opened.popleft()
			else:
				f, cell = heapq.heappop(self.opened)
			#add the cell to the set of closed cells.
			self.closed.add(cell)
			#if the current cell is the goal cell we are done.
			if cell is self.goal:
				self.display_path()
				break
			#loop through list of adjecent cells
			adj_cells = self.get_neighbours(cell)
			for adj_cell in adj_cells:
				if adj_cell not in self.closed:
					if (adj_cell.f, adj_cell) in self.opened:
						#if neighbouring cell is opened we need to see if the path is better:
						if adj_cell.g > cell.g + adj_cell.value:
							#if the new path is better, update current adjacent cell.
							self.update_cell(adj_cell, cell)
					else:
						#adjacent cell not opened, therefore update and push to heap to explore path further
						self.update_cell(adj_cell, cell)
						if (alg == 2):
							self.opened.append((adj_cell.f, adj_cell))
						else:
							heapq.heappush(self.opened, (adj_cell.f, adj_cell))
						


choice = input("Choose map: 1,2,3 or 4 \n")
while(choice not in [1,2,3,4]):
	choice = input("Not a valid value, please try again \n")


alg = input("Choose algorithm: \n 1: A* search \n 2: BFS \n 3: Dijkstra \n")
while(alg not in [1,2,3]):
	alg = input()

filename = "boards/board-2-" + str(choice) + ".txt"
pathList = []
a = AStar()
path = a.process()


with open(filename) as f:
 	grid = f.read().splitlines()
out = open("out/outBoard2-" + str(choice) + str(alg) + ".txt",'w')
for x in range(a.grid_width):
 	for y in range(a.grid_height):
			out.write(grid[x][y])
	out.write('\n')
out.close()


im = Image.new("RGB", (20*a.grid_height, 20*a.grid_width), (255, 255, 255))
draw = ImageDraw.Draw(im)


closed = a.get_closed()
opened = a.get_opened()
for x in range(a.grid_width):
	for y in range(a.grid_height-1, -1, -1):
 		if (a.get_cell(x,y).value == 100):
 			#draw black square dimension 20x20
 			draw.rectangle(((20*y,20*x), (20*(y+1), 20*(x+1))) , fill=(30,144,255), outline=(30,144,255))
 		elif (a.get_cell(x,y).value == 50):
 			draw.rectangle(((20*y,20*x), (20*(y+1), 20*(x+1))) , fill=(169,169,169), outline=(169,169,169))
 		elif (a.get_cell(x,y).value == 10):
 			draw.rectangle(((20*y,20*x), (20*(y+1), 20*(x+1))) , fill=(0,100,0), outline=(0,100,0))
 		elif (a.get_cell(x,y).value == 5):
 			draw.rectangle(((20*y,20*x), (20*(y+1), 20*(x+1))) , fill=(152,251,152), outline=(152,251,152))
 		elif (a.get_cell(x,y).value == 1):
 			draw.rectangle(((20*y,20*x), (20*(y+1), 20*(x+1))) , fill=(205,133,63), outline=(205,133,63))
 		if ((x,y) in pathList):
 			#draw blue circle
 			draw.ellipse(((20*y+7,20*x+7), (20*y+7+4, 20*x+7+4)) , fill=(0,0,0), outline=(0,0,0))
 		elif (grid[x][y]=="B"):
 			draw.ellipse(((20*y+7,20*x+7), (20*y+7+4, 20*x+7+4)) , fill=(124,252,0), outline=(124,252,0))
 		elif (grid[x][y]=="A"):
 			draw.ellipse(((20*y+7,20*x+7), (20*y+7+4, 20*x+7+4)) , fill=(255,0,0), outline=(255,0,0))
 		elif (a.get_cell(x,y) in closed):
 			#draw x
 			draw.line(((20*y+6,20*x+6), (20*y+14, 20*x+14)), fill=(40,40,40), width = 1)
 			draw.line(((20*y+6,20*x+14), (20*y+14, 20*x+6)), fill=(40,40,40), width = 1)
 		elif (a.get_cell(x,y) in opened):
 			#draw.ellipse(((20*y+7,20*x+7), (20*y+7+4, 20*x+7+4)) , fill=(255,55,0), outline=(255,55,0))
 			draw.polygon(((20*y + 5.5, 20*x + 8), (20*y + 9.5, 20*x +13), (20*y + 13.5, 20*x + 8)), fill=(55,55,55))
			draw.polygon(((20*y + 5.5, 20*x + 11), (20*y + 9.5, 20*x + 6), (20*y + 13.5, 20*x + 11)), fill=(55,55,55))
del draw
im.save("out/IMG/test2-" + str(choice) + str(alg) + ".png", "PNG")

#implement total price print.
cost = 0
for (x,y) in pathList:
	cost += a.get_cell(x,y).value
print cost


