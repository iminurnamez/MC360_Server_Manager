import pygame
from pygame.locals import *
from pygame import Color


class Label(object):
	def __init__(self, group, font_size, text, text_color, rect_attribute, x, y, bground_color = "black"):
		self.text = pygame.font.Font("freesansbold.ttf", font_size).render(text, True, Color(text_color), Color(bground_color))			
		self.rect_pos_dict = {"topleft": self.text.get_rect(topleft = (x, y)),
							 "topright": self.text.get_rect(topright = (x, y)),
							 "bottomleft": self.text.get_rect(bottomleft = (x, y)),
							 "bottomright": self.text.get_rect(bottomright = (x, y)),
							 "midtop": self.text.get_rect(midtop = (x, y)),
							 "midbottom": self.text.get_rect(midbottom = (x, y)),
							 "center": self.text.get_rect(center = (x, y)),
							 "midleft": self.text.get_rect(midleft = (x, y)),
							 "midright": self.text.get_rect(midright = (x, y))}
		self.rect = self.rect_pos_dict[rect_attribute]
		group.append(self)		
		
class DataLine(object):
	def __init__(self, name, point_list, color):
		self.name = name
		self.point_list = point_list
		self.color = pygame.Color(color)
		self.graphing = True
		
	def draw_line(self, surface, x_scale, y_scale, base):
		scaled_point_list = [(point[0] * x_scale, base - int(point[1] * y_scale/2)) for point in self.point_list] 
		pygame.draw.lines(surface, self.color, False, scaled_point_list)
		
def show_graph(economy):
	pygame.init()
	surface = pygame.display.set_mode((1080, 740))
	pygame.display.set_caption("Price History")
	FPS = 30
	fpsClock = pygame.time.Clock()
	SCREENWIDTH = 1080
	HALFWIDTH = SCREENWIDTH / 2
	SCREENHEIGHT = 740
	HALFHEIGHT = SCREENHEIGHT / 2

	text16 = pygame.font.Font("freesansbold.ttf", 16)
	text20 = pygame.font.Font("freesansbold.ttf", 20)
	
	x_scale = 10
	y_scale = 20
	y_scale_mod = 1
	base = 500
	window = surface.get_rect()
		
	while x_scale * economy.cycle_count > window.width:
		x_scale -= 1
	data_lines = []
	vert = base + 20
	horiz = window.left + 50
	for item in economy.price_history:
		data_line = DataLine(item, economy.price_history[item][1:], economy.price_history[item][0]) 
		data_line.graph_text = text16.render(data_line.name, True, data_line.color, Color("black"))
		data_line.graph_text_rect = data_line.graph_text.get_rect(topleft = (horiz, vert))
		vert += data_line.graph_text_rect.height + 10
		if vert + data_line.graph_text_rect.height + 10 > window.bottom - 30:
			vert = base + 20
			horiz += 120
		data_lines.append(data_line)
	
	blit_list = []
	exit_label = Label(blit_list, 20, "Exit", "blue", "midbottom",
						window.centerx, window.bottom - 20, "lightgray")
	instruct1_label = Label(blit_list, 16, "Click on an item's name to toggle that line on the graph.",
						"white", "topleft", exit_label.rect.right + 20, base + 50)
	instruct2_label = Label(blit_list, 16, "Use the arrow keys to expand or compress the graph.",
						"white", "topleft", instruct1_label.rect.left, instruct1_label.rect.bottom + 20)
	all_off_label = Label(blit_list, 16, "Hide All", "blue", "bottomleft", window.left + 200, window.bottom - 10, "lightgray")
	low_end_label = Label(blit_list, 16, "Low End", "blue", "bottomleft", window.left + 10, window.bottom - 10, "lightgray")
	mid_range_label = Label(blit_list, 16, "Mid Range", "blue", "bottomleft", low_end_label.rect.right + 10, window.bottom - 10, "lightgray")
	high_end_label = Label(blit_list, 16, "High End", "blue", "bottomleft", mid_range_label.rect.right + 10, window.bottom - 10, "lightgray")
	
	low_end = []
	mid_range = []
	high_end = []
	for data_line in data_lines:
		if data_line.name in ["Diamond", "Gold Ore", "Gold Ingot", "Iron Ore",
				"Iron Ingot", "Leather", "Redstone Dust", "Coal", "Obsidian"]:
			high_end.append(data_line)
		elif data_line.name in ["Cobblestone", "Dirt", "Gravel", "Leaves",
							"Cactus", "Pumpkin", "Sand", "Sapling",
							"Wheat", "Wheat Seeds"]:
			low_end.append(data_line)
		else:
			mid_range.append(data_line)
			
	expandingx = False
	expandingy = False
	compressingx = False
	compressingy = False
	
	while True:
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				x, y = event.pos
				if exit_label.rect.collidepoint(x, y):
					pygame.quit()
					return False
				elif all_off_label.rect.collidepoint(x, y):
					for data_line in data_lines:
						data_line.graphing = False
				elif low_end_label.rect.collidepoint(x,y):
					for data_line in high_end + mid_range:
						data_line.graphing = False
					for data_line in low_end:
						data_line.graphing = True
					y_scale = 300
					y_scale_mod = 20
				elif mid_range_label.rect.collidepoint(x, y):
					for data_line in high_end + low_end:
						data_line.graphing = False
					for data_line in mid_range:
						data_line.graphing = True
					y_scale = 50
					y_scale_mod = 5
				elif high_end_label.rect.collidepoint(x, y):
					for data_line in mid_range + low_end:
						data_line.graphing = False
					for data_line in high_end:
						data_line.graphing = True
					y_scale = 15
					y_scale_mod = .5
				for data_line in data_lines:
					if data_line.graph_text_rect.collidepoint(x, y):
						data_line.graphing = not data_line.graphing
			elif event.type == KEYDOWN:
				if event.key == K_RIGHT:
					expandingx = True
				elif event.key == K_UP:
					expandingy = True
				elif event.key == K_LEFT:
					compressingx = True
				elif event.key == K_DOWN:
					compressingy = True
				elif event.key == K_s:
					pygame.image.save(surface, "screenshot.png")
			elif event.type == KEYUP:
				if event.key == K_RIGHT:
					expandingx = False
				elif event.key == K_UP:
					expandingy = False
				elif event.key == K_LEFT:
					compressingx = False
				elif event.key == K_DOWN:
					compressingy = False
		if expandingx:
			x_scale += .2
		elif expandingy:
			y_scale += 1 * y_scale_mod
		elif compressingx and x_scale > 0:
			x_scale -= .2
		elif compressingy and y_scale > 0:
			y_scale -= 1 * y_scale_mod
		
		surface.fill(Color("black"))
		for data_line in data_lines:
			surface.blit(data_line.graph_text, data_line.graph_text_rect)
			if data_line.graphing:
				data_line.draw_line(surface, x_scale, y_scale, base)
		for label in blit_list:
			surface.blit(label.text, label.rect)
		pygame.draw.line(surface, Color("white"), (window.left, base), (window.right, base))
		pygame.display.update()
		fpsClock.tick(FPS)

def single_commodity_graph(economy, commodity):
	pygame.init()
	SCREENWIDTH = 1080
	HALFWIDTH = SCREENWIDTH / 2
	SCREENHEIGHT = 740
	HALFHEIGHT = SCREENHEIGHT / 2
	surface = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
	data_line = DataLine(commodity, economy.price_history[commodity][1:], economy.price_history[commodity][0])
	x_scale = 50
	while economy.cycle_count * x_scale > SCREENWIDTH:
		x_scale -= .5
	max_y = economy.base_prices[commodity]
	min_y = economy.base_prices[commodity]
	for point in economy.price_history[commodity][1:]:
		if point[1] > max_y:
			max_y = point[1]
		if point[1] < min_y:
			min_y = point[1]
	y_scale = SCREENHEIGHT/(((max_y - min_y)/2) + economy.base_prices[commodity])
	
	surface.fill(Color("black"))
	pygame.draw.line(surface, Color("white"), (0, SCREENHEIGHT - economy.base_prices[commodity] * y_scale/2),
						(SCREENWIDTH, SCREENHEIGHT - economy.base_prices[commodity] * y_scale/2) , 2)
	data_line.draw_line(surface, x_scale, y_scale, SCREENHEIGHT)
	pygame.image.save(surface, commodity + ".png")
	