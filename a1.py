import curses
import time
import copy
import math

#class Node():




class Semaphor():
	
	def __init__(self, pos):
		self.pos = pos
		self.semaphor = "_"
		self.name = "Semaphor"
		self.dev = False

	def open(self):
		self.semaphor = "/"

	def close(self):
		self.semaphor = "_"

	def draw(self, screen):
		screen.addstr(self.pos[0], self.pos[1]+1, self.semaphor)
		screen.addstr(self.pos[0]+1, self.pos[1], "|")

class Informator():

	def __init__(self, pos):
		self.pos = pos
		self.name = "Informator"
		self.msg = ""
		self.sel_pso = (0,0)
		self.color = 5


	def draw(self, screen):
		screen.addstr(self.pos[0], self.pos[1], self.msg, curses.color_pair(self.color))
		screen.addstr(self.pos[0]+1, self.pos[1], "{0},{1}".format(self.sel_pso[0],self.sel_pso[1]), curses.color_pair(self.color))


class Line():

	def __init__(self):
		self.name = "Line"
		self.pos_from = (0,0)
		self.pos_to = (0,0)
		self.line = []
		self.color = 0
		self.pos = (0,0)

	def calc(self):
		self.line = []
		d = math.sqrt(math.pow(self.pos_from[0]-self.pos_to[0],2) + math.pow(self.pos_from[1]-self.pos_to[1],2))
		if d > 0:	
			vx = (self.pos_to[0] - self.pos_from[0])/d
			vy = (self.pos_to[1] - self.pos_from[1])/d
			nx=self.pos_from[0]
			ny=self.pos_from[1]
			for _ in range(int(d)):
				self.line.append((int(nx), int(ny)))
				nx+=vx 
				ny+=vy
		if len(self.line) > 0:
			self.line.pop(0)
		if len(self.line) > 0:
			self.pos = self.line[0]

	def draw(self, screen):
		#if len(self.line) > 0:
			#screen.addstr(3, 0,"{0},{1}".format(self.line[0][1],self.line[0][0]))
		for p in self.line:
			screen.addstr(p[0], p[1], "-", curses.color_pair(self.color))
		

class Selector():

	def __init__(self, pos):
		self.pos = pos
		self.name = "Selector"
		self.color = 3
		self.msg = ""


	def draw(self, screen):
		screen.addstr(self.pos[0], self.pos[1]-1, "[", curses.color_pair(self.color))
		screen.addstr(self.pos[0], self.pos[1]+1, "]", curses.color_pair(self.color))
		screen.addstr(self.pos[0], self.pos[1]+2, self.msg)

class TracVertical():

	def __init__(self, size, pos):
		self.pos = pos
		for i in range(size):
			self.track = self.track + "-"

class TracHorizontal():

	def __init__(self, pos):
		self.pos = pos
		self.color = 0
		self.name = "TracHorizontal"
		self.dev = False
		self.semaphor = False
		self.size = 0
		self.id = 0


	def draw(self, screen):
		if self.semaphor:
			string = "x"
		else:
			string = "o"
		# for i in range(self.size):
		# 	string = string + "-"

		screen.addstr(self.pos[0], self.pos[1], string, curses.color_pair(self.color))
		if self.dev:
		 	screen.addstr(self.pos[0]+1, self.pos[1], str(self.id), curses.color_pair(self.color))	




stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
curses.start_color()
#curses.mousemask(1)

curses.init_pair(1, 69, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)


test = stdscr.subpad(4,100,0,0)


def xd(screen, pos):
	screen.addstr(pos[0], pos[1]+11,   "**")
	screen.addstr(pos[0]+1, pos[1], "ㅁㅁ-ㅁㅁ-ㅁㅁ-ㅁㅁ>")


# def line(fr,to,screen):
# 	d = math.sqrt( math.pow(fr[0]-to[0],2) + math.pow(fr[1]-to[1],2))
# 	if d == 0:
# 		return
# 	vx = (to[1] - fr[1])/d
# 	vy = (to[0] - fr[0] )/d
# 	screen.addstr(10, 10, str(vx))
# 	nx=fr[0]
# 	ny=fr[1]
# 	while int(nx)<to[1]:
# 		screen.addstr(int(ny), int(nx), ".")
# 		nx+=vx 
# 		ny+=vy

	


s1 = Selector((2,2))
selector = Selector((5,5))
selected_node = None
inf = Informator((1,1))
inf.msg="Init"
line = Line()


#stdscr.addstr(10,0,"¦")

x = 5
y = 5
n = 250

nodes_counter = 0

graph = [[0] * n for _ in range(n)]
path = []
blocks = []
scen = {}
mapMatrix= [[0] * n for _ in range(n)]
color = 0
dev = False
lines = []
state = "select"

#scen[(0,0)]=inf

while True:
	stdscr.nodelay(1)
	#stdscr.keypad(1)
	c = stdscr.getch()
	if c == ord('q'):
		break
	elif c == ord('`'):
		dev = not dev
	elif c == ord('w'):
		x=x-1
	elif c == ord('s'):
		x=x+1
	elif c == ord('a'):
		y=y-1
	elif c == ord('d'):
		y=y+1
	elif c == ord('t'):
		selector.msg = "Track"
		s1 = TracHorizontal((x,y))
	elif c == ord('y'):
		selector.msg = "Semaphor"
		s1 = Semaphor((x,y))
	elif c == ord('z'):
		
		if s1.name == "Semaphor":
			if mapMatrix[x+2][y] == 2:
				scen[(x,y)]=(copy.deepcopy(s1))
				scen[(x+2,y)].semaphor = True
				mapMatrix[x][y+1] = 4
				mapMatrix[x+1][y] = 4
		elif s1.name == "TracHorizontal":
			s1.pos = (x,y)
			mapMatrix[x][y] = 2
			s1.id = nodes_counter
			scen[(x,y)]=(copy.deepcopy(s1))
			inf.msg = "Add node : {0}. {1},{2}".format(nodes_counter,x,y)
			nodes_counter += 1
			selected_node = None
			lines.append(copy.deepcopy(line))

		elif scen[(x,y)].name == "TracHorizontal":
			selected_node = scen[(x,y)]
			inf.msg = "Selected node : {0}. {1},{2}".format(selected_node.id,x,y)
			selected_node.color = 4

	inf.sel_pso = selector.pos	
			
	if s1.name == "Semaphor":
		if mapMatrix[x+2][y] == 2:
			selector.color = 2
		else:
			selector.color = 3

	if selected_node != None:
		line.pos_from=selected_node.pos
		line.pos_to=(x,y)
		line.calc()
		line.draw(stdscr)
	stdscr.refresh()		
	selector.pos = (x,y)
	selector.draw(stdscr)
	stdscr.refresh()

	test.bkgd(curses.color_pair(5))
	test.border()

	inf.draw(test)
	test.refresh()

	time.sleep(1/20)
	stdscr.clear()
	stdscr.refresh()



	for l in lines:
		l.draw(stdscr)
		stdscr.refresh()

	for a in scen:
		scen[a].dev = dev
		#scen[a].color = color
		scen[a].draw(stdscr)
		stdscr.refresh()








curses.endwin()




class TracBlock():

	def __init__(self, size, pos):
		self.pos = pos
		for i in range(size):
			self.track = self.track + "-"



class Curve():
	pass

class Switch():
	pass


