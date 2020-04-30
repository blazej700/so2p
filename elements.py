import curses
import time
import copy
import math


class SceneElement():
	def __init__(self, pos):
		self.pos = pos
		self.name = ""
		self.dev = False

	def draw(self):
		raise NotImplementedError()

class Semaphor(SceneElement):
	def __init__(self, pos):
		super().__init__(pos)
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
		screen.refresh()

class Informator(SceneElement):
	def __init__(self, pos):
		super().__init__(pos)
		self.name = "Informator"
		self.msg = ""
		self.sel_pso = (0,0)
		self.color = 5
		self.state_msg = ""

	def draw(self, screen):
		screen.addstr(self.pos[0], self.pos[1]+20, self.state_msg, curses.color_pair(self.color))
		screen.addstr(self.pos[0]+1, self.pos[1]+20, self.msg, curses.color_pair(self.color))
		screen.addstr(self.pos[0]+1, self.pos[1], "{0},{1}".format(self.sel_pso[0],self.sel_pso[1]), curses.color_pair(self.color))
		screen.refresh()


class Line(SceneElement):
	def __init__(self, pos=(0,0)):
		super().__init__(pos)
		self.name = "Line"
		self.pos_from = (0,0)
		self.pos_to = (0,0)
		self.line = []
		self.color = 0
		

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
		for p in self.line:
			screen.addstr(p[0], p[1], "-", curses.color_pair(self.color))
		screen.refresh()


class Selector(SceneElement):
	def __init__(self, pos):
		super().__init__(pos)
		self.name = "Selector"
		self.color = 3
		self.msg = ""
		self.type = ""

	def set_type(self, map_element):
		if map_element is not None:
			if map_element.name == "Node":
				self.type = "node"
			else:
				self.type = "select"
		else:
				self.type = "select"


	def draw(self, screen):
		
		if self.type == "select":
			screen.addstr(self.pos[0], self.pos[1]-1, "[", curses.color_pair(self.color))
			screen.addstr(self.pos[0], self.pos[1]+1, "]", curses.color_pair(self.color))
		elif self.type == "node":
			screen.addstr(self.pos[0], self.pos[1], "o", curses.color_pair(1))
		elif self.type == "chuj":
			pass

		self.msg = "{0}x{1}".format(self.pos[0], self.pos[1])
		screen.addstr(self.pos[0], self.pos[1]+2, self.msg)
		screen.refresh()


class Node(SceneElement):
	def __init__(self, pos):
		super().__init__(pos)
		self.color = 0
		self.name = "Node"
		self.dev = False
		self.semaphor = False
		self.size = 0
		self.id = 0

		self.msg = ""
		self.type = ""

	def set_type(self, map_element):
		pass


	def draw(self, screen):
		if self.semaphor:
			string = "x"
		else:
			string = "o"

		screen.addstr(self.pos[0], self.pos[1], string, curses.color_pair(self.color))
		if self.dev:
		 	screen.addstr(self.pos[0]+1, self.pos[1], str(self.id), curses.color_pair(self.color))	
		#self.msg = "{0}x{1}".format(self.pos[0], self.pos[1])
		#screen.addstr(self.pos[0], self.pos[1]+2, self.msg)
		screen.refresh()

class TextLabel(SceneElement):
	def __init__(self, pos, max_line = 1, color = 0):
		super().__init__(pos)
		self.name = "TextLabel"
		self.text = []
		self.color = color
		self.max_line = max_line

	def draw(self, screen):
		while len(self.text) > self.max_line:
			self.text.pop(0)
		i = 0
		for x in self.text:
			screen.addstr(self.pos[0]+i, self.pos[1], x, curses.color_pair(self.color))
			screen.refresh()
			i+=1

