
import heapq
from PIL import Image, ImageDraw


class Cell():
	#Class for each cell (1x1) of the board with parameters: 
	# Reachable - is it possible to get to the cell
	# x - the x coordinate of the cell
	# y - the y coordinate of the cell
	# parent - allows relations/graph structure between the cells on a path/graph
	# g - cost from start cell to current cell
	# h - heuristic cost from current cell to goal cell
	# f = g + h - the expected cost function for any given cell
	def __init__(self, x, y, reachable):
		self.reachable = reachable
		self.x = x
		self.y = y
		self.parent = None
		self.g = 0
		self.h = 0
		self.f = 0

	#To make ordering of heap work properly when values might be identical
	def __lt__(self, other):
		return self.f < other.f

class AStar():
	#The main class of the algorithm with parameters:
	#opened - a heap containing the cells that are queued at any given time
	#closed - a set containing visited cells (set avoids duplicates)
	#cells - a list of all the cells in the grid
	#grid_height - The height of the grid
	#grid_width - The width of the grid
	#start - The starting cell
	#goal - The ending cell
	def __init__(self):
		self.opened = []
		heapq.heapify(self.opened)
		self.closed = set()
		self.cells = []
		self.grid_height = 0
		self.grid_width = 0
		self.start = None
		self.goal = None

	def init_grid(self):
		#Initialize the grid from the txt-file
		#Updates cells with all the cells, sets width, height, 
		#start and goal and if a cell is reachable
		with open(filename) as f:
			grid = f.read().splitlines()
		self.grid_width = len(grid)
		self.grid_height = len(grid[0])
		start = []
		goal = []
		for x in range(self.grid_width):
			for y in range(self.grid_height):
				if(grid[x][y] == "#"):
					reachable = False
				elif (grid[x][y] == "A"):
					start = [x,y]
					reachable = True
				elif (grid[x][y] == "B"):
					goal = [x,y]
					reachable = True
				else:
					reachable = True
				self.cells.append(Cell(x, y, reachable))
		self.start = self.get_cell(start[0],start[1])
		self.goal = self.get_cell(goal[0],goal[1])

	def get_cell(self, x, y):
		#return the cell object corresponding to a given coordinate.
		return self.cells[x * self.grid_height + y]

	def get_heuristic(self, cell):
		#return the manhattan distance from the goal 
		#cell to the current cell, i.e. h(n)
		return (abs(cell.x - self.goal.x) + abs(cell.y - self.goal.y))

	def get_neighbours(self, cell):
		#return list of neighbouring cells clockwise starting 
		#from the rightmost one
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

	def get_path(self):
		#Get the path of the algorithm as a list (or print as text)
		cell = self.goal
		while cell.parent is not self.start:
			cell = cell.parent
			#print('path: cell: %d,%d' % (cell.x, cell.y))
			pathList.append((cell.x, cell.y))
		return pathList

	def update_cell(self, adj, cell):
		#Given a cell and a neighbour/adjacent cell, 
		#update the neighbours expected cost and set 
		#neigh. cell to child of reference cell
		adj.g = cell.g + 1
		adj.h = self.get_heuristic(adj)
		adj.parent = cell
		adj.f = adj.g + adj.h 
	
	def process(self):
		#The main algorithm: A* search.
		#initialize
		self.init_grid()
		#Start node is added to the "opened" heap queue
		heapq.heappush(self.opened, (self.start.f, self.start))

		#Main loop invariant - continues as long as there are opened cells
		while (len(self.opened)):
			#pop the first element from the heap, i.e. the cell with lowest f value.
			f, cell = heapq.heappop(self.opened)
			#add the cell to the set of closed/visited cells.
			self.closed.add(cell)
			#If the current cell is the goal cell we are done.
			if cell is self.goal:
				#self.display_path()
				break
			#loop through list of adjecent cells
			adj_cells = self.get_neighbours(cell)
			for adj_cell in adj_cells:
				if adj_cell.reachable and adj_cell not in self.closed:
					#if neighbouring cell is reachable and not closed/visited, proceed:
					if (adj_cell.f, adj_cell) in self.opened:
						#if neighbouring cell is opened we need to see if this path is better:
						if adj_cell.g > cell.g + 1:
							#if the new path is better, then relax the adjacent cell.
							self.update_cell(adj_cell, cell)
					else:
						#adjacent cell not opened, therefore update and push to heap to explore path further
						self.update_cell(adj_cell, cell)
						heapq.heappush(self.opened, (adj_cell.f, adj_cell))




choice = input("Choose map: 1,2,3 or 4 \n")
while(choice not in [1,2,3,4]):
	choice = input("Not a valid value, please try again \n")

filename = "board-1-" + str(choice) + ".txt"
a = AStar()
pathList = a.get_path()
path = a.process()


with open(filename) as f:
 	grid = f.read().splitlines()
out = open("outBoard1-" + str(choice) + ".txt",'w')
for x in range(a.grid_width):
	for y in range(a.grid_height):
		if (x,y) in pathList:
			out.write('o')
		else:
			out.write(grid[x][y])
	out.write('\n')
out.close()


im = Image.new("RGB", (20*a.grid_height, 20*a.grid_width), (255, 255, 255))
draw = ImageDraw.Draw(im)
draw.line(((0,0), (0, 20*a.grid_width)), fill=(0,0,0), width = 1)
draw.line(((0,0), (20*a.grid_height, 0)), fill=(0,0,0), width = 1)
draw.line(((20*a.grid_height, 20*a.grid_width-1), (0, 20*a.grid_width-1)), fill=(0,0,0), width = 1)
draw.line(((20*a.grid_height - 1, 0), (20*a.grid_height - 1, 20*a.grid_width)), fill=(0,0,0), width = 1)

for x in range(a.grid_width):
	for y in range(a.grid_height-1, -1, -1):
		if (grid[x][y]=="#"):
			#draw black square dimension 20x20
			draw.rectangle(((20*y,20*x), (20*(y+1), 20*(x+1))) , fill=(0,0,0), outline=(0,0,0))
		elif ((x,y) in pathList):
			#draw blue rectangle
			draw.rectangle(((20*y+7,20*x+7), (20*y+7+4, 20*x+7+4)) , fill=(30,144,255), outline=(30,144,255))
		elif (grid[x][y]=="B"):
			draw.rectangle(((20*y+7,20*x+7), (20*y+7+4, 20*x+7+4)) , fill=(124,252,0), outline=(124,252,0))
		elif (grid[x][y]=="A"):
			draw.rectangle(((20*y+7,20*x+7), (20*y+7+4, 20*x+7+4)) , fill=(255,0,0), outline=(255,0,0))

del draw
im.save("test1-" + str(choice) + ".png", "PNG")

