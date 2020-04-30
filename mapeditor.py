import curses
import time
import copy
import math
from elements import Semaphor, Informator, Line, Selector, Node, TextLabel


class Map():
	def __init__(self):
		self.n = 250
		self.graph = [[0] * self.n for _ in range(self.n)]
		self.path = []
		self.blocks = []
		self.scen = {}
		self.mapMatrix= [[0] * self.n for _ in range(self.n)]
		self.lines = []
		self.nodes_counter = 0
		self.dev = False
		self.pos = (404,404)

	def add_element(self, element, second_element = None):
		if element.name == "Node":
			self.add_node(element, second_element)
		elif element.name == "Line":
			self.add_line(element)
		else:
			raise RuntimeError("Element is not instance of CLASS_NAME")


	def add_line(self, line):
		self.lines.append(copy.deepcopy(line))

	def add_non_maped_elemet(self, map_object):
		self.scen[map_object.pos]=copy.deepcopy(map_object)
		self.mapMatrix[map_object.pos[0]][map_object.pos[1]]=1
		map_object = None
		
	def add_node(self, node, node_connected = None):
		node.id = self.nodes_counter
		self.nodes_counter += 1
		if node_connected != None : self.graph[node.id][node_connected.id]=1
		self.add_non_maped_elemet(node)

	def draw(self, screen):
		for l in self.lines:
			l.draw(screen)

		for a in self.scen:
			self.scen[a].dev = self.dev
			self.scen[a].draw(screen)
			
			

class MapEditor():

	def __init__(self, app_map):
		self.app_map = app_map
		self.current_element = None
		self.line = None

	def node_mode(self, pos):
		self.current_element = Node(pos)

	def line_mode(self, pos):
		self.line = Line()
		self.line.pos_from = pos

	def add_ce(self):
		if self.current_element is not None:
			self.app_map.add_element(self.current_element)
			self.current_element = None
		if self.line is not None:
			self.app_map.add_element(self.line)
			self.line = None


class Window():

	def init(self):
		self.stdscr = None

	def draw(self):
		pass

	def get_event(self):
		curses.noecho()
		curses.curs_set(0)
		self.stdscr.nodelay(1)
		event = self.stdscr.getch()
		self.stdscr.refresh()
		#if event < 256 and event > 0:
		return event
		#elif event == curses.KEY_RESIZE:
			#return 'r'
		#else:
			#return None

	def get_text(self, p = (0,0)):
		self.stdscr.refresh()
		curses.curs_set(2)
		curses.echo()
		self.stdscr.move(p[0],p[1])
		input_string = self.stdscr.getstr().decode(encoding="utf-8")
		curses.noecho()
		curses.curs_set(0)
		self.stdscr.refresh()
		return input_string

class SubWindow(Window):
	def __init__(self, screen, pos, size, color = 0, border = False, kupa = False):
		if isinstance(screen, Window):
			self.screen = screen.stdscr
		else:
			self.screen = screen
		self.pos = pos
		self.size = size
		self.color = color
		self.border = border
		self.stdscr = self.screen.subwin(size[0],size[1],pos[0],pos[1])
		self.elements = []

		self.kupa = kupa

	def reset(self, pos, size):
		self.pos = pos
		self.size = size
		self.stdscr.resize(self.size[0],self.size[1])
		self.stdscr.mvwin(self.pos[0],self.pos[1])

	def draw(self):
		self.stdscr.bkgd(curses.color_pair(self.color))
		if self.border:
			self.stdscr.border()
		i = 0
		for e in self.elements:
			if self.kupa:
				self.stdscr.addstr(2+i, 2, "{0},{1}".format(e.pos[0],e.pos[1]))
			e.draw(self.stdscr)
			i+=1
		#self.stdscr.refresh()


	def clear(self):
		#self.stdscr.redrawwin()
		self.stdscr.clear()
		self.stdscr.refresh()


class MainWindow(Window):

	def __init__(self):
		self.stdscr = curses.initscr()
		self.size = self.stdscr.getmaxyx()
		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)
		curses.start_color()

		curses.init_pair(1, 69, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)
		curses.init_pair(6, curses.COLOR_BLACK, 69)
		curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_RED)

		self.elements = []

	def get_size(self):
		self.size = self.stdscr.getmaxyx()
		return self.size

	def draw(self):
		for e in self.elements:
			e.draw(self.stdscr)

	def clear(self):
		self.stdscr.erase()
		self.stdscr.clear()
		self.stdscr.refresh()


class App():

	def __init__(self):
		self.screen = MainWindow()

		self.app_map = Map()
		self.map_editor = MapEditor(self.app_map)

		self.size = self.screen.size

		self.cord = ((int(self.size[0]/2), int(self.size[1]/2)))

		self.runing = True

		self.bar_window = SubWindow(self.screen, (0,0), (3,self.size[1]), 5, True)
		self.editor_window = SubWindow(self.screen, (3,0), (self.size[0]-3,self.size[1]), 0, True, True)
		self.command_window = SubWindow(self.screen, (int(self.size[0]/3),int(self.size[1]/3)), (3,int(self.size[1]/3)), 0, True)

		self.KEY_w = ord('w')
		self.KEY_a = ord('a')
		self.KEY_s = ord('s')
		self.KEY_d = ord('d')
		self.KEY_pp = ord(':')
		self.KEY_1 = ord('1')
		self.KEY_2 = ord('2')
		self.KEY_ent = ord('\n')
		self.KEY_q = ord('q')

		self.new_node_label = TextLabel((1,1))
		self.cord_label = TextLabel((1,15))
		self.new_node_label.text.append("[1] new node |")


		self.EDITOR_B = { self.KEY_1 : (lambda : self.map_editor.node_mode(self.cord)),
						 self.KEY_ent : self.map_editor.add_ce,
						 self.KEY_q : self.none_mode,
						 self.KEY_2 : (lambda : self.map_editor.line_mode(self.cord))}

	def stop(self):
		self.runing = False
		
	def reload(self):
		old = self.size
		self.size = self.screen.get_size()
		self.bar_window.reset((0,0), (3,self.size[1]),)
		self.editor_window.reset((3,0), (self.size[0]-3,self.size[1]))
		self.command_window.reset((int(self.size[0]/3),int(self.size[1]/3)), (3,int(self.size[1]/3)))
		self.t1.text.append("Ressized. Old size: {0}x{1} new size: {2}x{3}".format(old[0],old[1],self.size[0],self.size[1]))


	def none_mode(self):
		self.bar_window.elements.remove(self.new_node_label)
		self.bar_window.color = 5
		self.s1.type = "select"
		self.current_mode = None

	def move_cord(self, n_cord):
		self.cord = (self.cord[0] + n_cord[0], self.cord[1] + n_cord[1])
		if self.cord[0]+5 > self.size[0]:
			self.cord = (self.size[0]-5, self.cord[1])

		if self.cord[1]+3 > self.size[1]:
			self.cord = (self.cord[0], self.size[1]-3)

		if self.cord[0] < 1:
			self.cord = (1, self.cord[1])

		if self.cord[1] < 2:
			self.cord = (self.cord[0], 2)

	def set(self):
		st1 = self.command_window.get_text((1,1))
		st2 = self.command_window.get_text((1,1))
		self.cord = (int(st1), int(st2))


	def text_menu(self):
		BB = {"exit" : "stop",
			  "quit" : "stop",
			  "stop" : "stop",
			  "spierdalaj" : "stop",
			  "q" : "stop",
			  "x" : "stop",
			  "edit" : "editor",
			  "editor" : "editor",
			  "e" : "editor",
			  "r" : "r",
			  "set" : "set"}
		B = {"stop" : self.stop,
			 "editor" : self.editor_mode,
			 "r" : self.r,
			 "set" : self.set}
		self.command_window.draw()
		st = self.command_window.get_text((1,1))
		if st in BB:
			B[BB[st]]()

	def editor_mode(self, event = None):
		self.bar_window.color = 6
		if self.new_node_label not in self.bar_window.elements:
			self.bar_window.elements.append(self.new_node_label)
		self.current_mode = self.editor_mode
		self.s1.set_type(self.map_editor.current_element)

		if event in self.EDITOR_B:
			self.EDITOR_B[event]()
		if self.map_editor.current_element is not None:
			self.map_editor.current_element.pos = self.cord
		if self.map_editor.line is not None:
			self.map_editor.line.pos_to = self.cord
			self.map_editor.line.calc()



	def r(self):
		self.screen.clear()
		self.bar_window.clear()
		self.editor_window.clear()
		self.command_window.clear()

	def run(self):

		self.current_mode = None
		self.s1 = Selector(self.cord)
		self.s1.type = "select"

		self.editor_window.elements.append(self.app_map)
		self.editor_window.elements.append(self.s1)
		
		self.t1 = TextLabel((1,1))
		self.bar_window.elements.append(self.t1)
		self.selected_element = None

		self.bar_window.elements.append(self.cord_label)

		A ={self.KEY_w : (lambda : self.move_cord((-1,0))),
			self.KEY_s : (lambda : self.move_cord((1,0))),
			self.KEY_a : (lambda : self.move_cord((0,-1))),
			self.KEY_d : (lambda : self.move_cord((0,1))),
			self.KEY_pp : (lambda : self.text_menu()),
			curses.KEY_RESIZE : (lambda : self.reload())}

		while self.runing:
			self.cord_label.text.append("{0}x{1} | {2}x{3}".format(self.cord[0],self.cord[1],69,69))
			self.s1.pos = self.cord
			#self.bar_window.draw()
			#self.s1.draw(self.editor_window.stdscr)
			self.editor_window.draw()
			#self.s1.draw(self.editor_window.stdscr)
			self.bar_window.draw()

			try:
				self.selected_element = self.app_map.scen[self.cord]
				self.s1.color = 2
			except:
				self.selected_element = None
				self.s1.color = 3

			a = self.editor_window.get_event()
			if a in A:
				A[a]()

			if self.current_mode is not None:
				self.current_mode(a)

			time.sleep(1/20)
			self.screen.clear()
			self.bar_window.clear()
			self.editor_window.clear()
			self.command_window.clear()



a1 = App()
a1.run()

curses.endwin()