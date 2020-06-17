import sys
import pygame

class Visualizer:
	def __init__(self,width=640,height=480):
		pygame.init()
		self.clock = clock = pygame.time.Clock()
		self.fps = 120
		self.width, self.height = width, height
		self.display = pygame.display
		self.screen = self.display.set_mode((self.width, self.height))
		self.display.set_caption('Visualizer_pygame')
		self.icon = pygame.image.load('SPCX.ico')
		self.display.set_icon(self.icon)
		self.running = True
		self.background_colour = (0,0,0)
		self.x,self.y = int(self.width/2),int(self.height/2)
		self.debug = False
		
		
	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if self.debug:
					print(pygame.key.name(event.key),"DOWN")
				else:
					pass
			if event.type == pygame.KEYUP:
				if self.debug:
					print(pygame.key.name(event.key),"UP")
				else:
					pass
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.debug:
					print(event.pos,event.button)
				else:
					pass
			if event.type == pygame.MOUSEBUTTONUP:
				if self.debug:
					print(event.pos,event.button)
				else:
					pass
			if event.type == pygame.MOUSEMOTION:	
				self.x = event.pos[0]
				self.y = event.pos[1]			
				if self.debug:
					print(event.pos,event.rel,event.buttons)

				else:
					pass

	def run(self):
		while self.running:
			self.handle_events()
			self.screen.fill(self.background_colour)
			color = (255,255,255)
			center = self.x,self.y
			radius = 10
			pygame.draw.circle(self.screen, color, center, radius) 
			#self.display.update()#UPDATE WHOLE SCREEN,IF NO ARGUMENTS GIVEN SAME AS FLIP
			self.display.flip()# UPDATE ENTIRE SCREEN
			self.clock.tick(self.fps)
			print("FPS:",int(round(self.clock.get_fps())),end="\r")
			
			
V = Visualizer()
V.run()
'''	
pygame.init()
clock = pygame.time.Clock()
(width, height) = (640, 480)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('GUI')
programIcon = pygame.image.load('SPCX.ico')
pygame.display.set_icon(programIcon)

running = True
while running:
	background_colour = (0,0,0)
	screen.fill(background_colour)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			print(pygame.key.name(event.key),"DOWN")
		if event.type == pygame.KEYUP:
			print(pygame.key.name(event.key),"UP")
		if event.type == pygame.MOUSEBUTTONDOWN:
			print(event.pos,event.button)
		if event.type == pygame.MOUSEBUTTONUP:
			print(event.pos,event.button)
		if event.type == pygame.MOUSEMOTION:
			print(event.pos,event.rel,event.buttons)
	clock.tick(60) 
pygame.quit()
sys.exit()
'''
