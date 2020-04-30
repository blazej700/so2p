class Map_editor():
	def __init__(self):
		self.stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)
		curses.start_color()


		self.info_pad = self.stdscr.subpad(4,100,0,0)

		curses.init_pair(1, 69, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
		curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)



	def update_cordinants(self):
		if event == ord('w'):
			x=x-1
		elif event == ord('s'):
			x=x+1
		elif event == ord('a'):
			y=y-1
		elif event == ord('d'):
			y=y+1
		elif event == ord(':'):
			last_state = state
			state = "menu" #??? 아니 후이 많이 많이 후이 

	def menu(self):
		curses.curs_set(2)
		curses.echo()
		selector.type = "none"
		inf.state_msg = "Type command"
		self.info_pad.bkgd(curses.color_pair(5))
		self.info_pad.border()
		inf.draw(self.info_pad)
		self.info_pad.refresh()
		
		text_input = self.stdscr.subpad(3,60,4,20)
		text_input.border()
		text_input.refresh()
		text_input.move(1,1)
		input_string = text_input.getstr().decode(encoding="utf-8")

		if str(input_string) == "exit":
			break
		elif input_string == "dev":
			dev = not dev
			state = last_state
		elif input_string == "1":
			state = "select"
			inf.msg = "Select node and push enter"
		elif input_string == '2':
			state = "new_node"
			inf.msg = "Place node and push enter"
			curent_item = Node((x,y))
		elif input_string == '':
			state = last_state
		elif input_string == 'e':
			state = "drawing_line"
			inf.msg = "Place node and push enter"
			curent_item = Node((x,y))
		elif input_string == '3':
			pass
		else:
			inf.msg = "{}: not editor command".format(input_string)

		XD = {"dev" : lambda : self.dev = not self.dev, 
			"1" : self.select_mode, 
			"2" : self.place_object, 
			"e" : self.draw_line }

	def select_mode(self):
		pass

	def place_object(self, object):
		curent_item.pos = (x,y)
		mapMatrix[x][y] = 2
		curent_item.id = nodes_counter
		scen[(x,y)]=(copy.deepcopy(curent_item))
		inf.msg = "Add node : {0}. {1},{2}".format(nodes_counter,x,y)
		nodes_counter += 1
		selected_node = None

	def draw_line(self):
		pass

	def event_chooser(self):
		pass

	def update_scene(self):
		self.stdscr.refresh()		
		selector.pos = (x,y)
		selector.draw(self.stdscr)
		self.stdscr.refresh()

		self.info_pad.bkgd(curses.color_pair(5))
		self.info_pad.border()
		inf.draw(self.info_pad)
		self.info_pad.refresh()

		time.sleep(1/20)
		self.stdscr.clear()
		self.stdscr.refresh()



		for l in lines:
			l.draw(self.stdscr)
			self.stdscr.refresh()

		for a in scen:
			scen[a].dev = dev
			#scen[a].color = color
			scen[a].draw(self.stdscr)
			self.stdscr.refresh()

	def run(self):

		curent_item = Selector((5,5))
		selector = Selector((5,5))
		selected_node = None
		inf = Informator((1,1))
		inf.msg=""
		line = Line()

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
		state = "menu"
		last_state = state

		while True:


			if state != "menu":
				curses.noecho()
				curses.curs_set(0)
				self.stdscr.nodelay(1)
				event = self.stdscr.getch()

				if event == ord('w'):
					x=x-1
				elif event == ord('s'):
					x=x+1
				elif event == ord('a'):
					y=y-1
				elif event == ord('d'):
					y=y+1
				elif event == ord(':'):
					last_state = state
					state = "menu" 


			if state == "select":
				selector.type = "select"
				inf.msg = "Select node and push enter"

				selector.color = 3
				if mapMatrix[x][y]:
					selector.color = 2
					selected_node = scen[(x,y)]
					inf.msg = "Selected node : {0}. {1},{2} push enter to continue".format(selected_node.id,x,y)
					if event == ord('\n'):
						last_state = state
						state="menu"
						selector.color = 3


			elif state == "drawing_line":
				selector.type = "node"
				inf.state_msg = "New node with conection"

				line.pos_from=selected_node.pos
				line.pos_to=(x,y)
				line.calc()
				line.draw(self.stdscr)

				if mapMatrix[x][y]:
					selector.type = "select"
					selector.color = 2

				if event == ord('\n'):
					if mapMatrix[x][y]:
						inf.msg = "Add line to : {0}. {1},{2}".format(scen[(x,y)].id,x,y)
						graph[selected_node.id][scen[(x,y)].id]

					else:
						curent_item.pos = (x,y)
						mapMatrix[x][y] = 2
						curent_item.id = nodes_counter
						scen[(x,y)]=(copy.deepcopy(curent_item))
						inf.msg = "Add node : {0}. {1},{2}".format(nodes_counter,x,y)
						graph[selected_node.id][curent_item.id]

					nodes_counter += 1
					lines.append(copy.deepcopy(line))
					selected_node = None
					state = "select"
					inf.msg = "Select node and push enter"


			elif state == "new_node":
				selector.type = "node"
				inf.state_msg = "New node"
				

				if event == ord('\n'):
					curent_item.pos = (x,y)
					mapMatrix[x][y] = 2
					curent_item.id = nodes_counter
					scen[(x,y)]=(copy.deepcopy(curent_item))
					inf.msg = "Add node : {0}. {1},{2}".format(nodes_counter,x,y)
					nodes_counter += 1
					selected_node = None
					

			elif state == "menu":
				curses.curs_set(2)
				curses.echo()
				selector.type = "none"
				inf.state_msg = "Type command"
				self.info_pad.bkgd(curses.color_pair(5))
				self.info_pad.border()
				inf.draw(self.info_pad)
				self.info_pad.refresh()
				
				text_input = self.stdscr.subpad(3,60,4,20)
				text_input.border()
				text_input.refresh()
				text_input.move(1,1)
				input_string = text_input.getstr().decode(encoding="utf-8")

				if str(input_string) == "exit":
					break
				elif input_string == "dev":
					dev = not dev
					state = last_state
				elif input_string == "1":
					state = "select"
					inf.msg = "Select node and push enter"
				elif input_string == '2':
					state = "new_node"
					inf.msg = "Place node and push enter"
					curent_item = Node((x,y))
				elif input_string == '':
					state = last_state
				elif input_string == 'e':
					state = "drawing_line"
					inf.msg = "Place node and push enter"
					curent_item = Node((x,y))
				elif input_string == '3':
					pass
				else:
					inf.msg = "{}: not editor command".format(input_string)

				


			self.stdscr.refresh()		
			selector.pos = (x,y)
			selector.draw(self.stdscr)
			self.stdscr.refresh()

			self.info_pad.bkgd(curses.color_pair(5))
			self.info_pad.border()
			inf.draw(self.info_pad)
			self.info_pad.refresh()

			time.sleep(1/20)
			self.stdscr.clear()
			self.stdscr.refresh()



			for l in lines:
				l.draw(self.stdscr)
				self.stdscr.refresh()

			for a in scen:
				scen[a].dev = dev
				#scen[a].color = color
				scen[a].draw(self.stdscr)
				self.stdscr.refresh()




		curses.endwin()


me = Map_editor()
me.run()