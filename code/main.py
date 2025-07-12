import pygame, sys
from settings import *
#from debug import debug
from level import Level
from menu import Menu

class Game:
	def __init__(self):
		  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption("Pylda - Mini Zelda in Python")
		self.clock = pygame.time.Clock()

		self.level = Level()

		# icon 
		icon_surface = pygame.image.load('./graphics/menu/logo.png').convert_alpha()
		icon_surface = pygame.transform.smoothscale(icon_surface, (64, 64))
		pygame.display.set_icon(icon_surface)
		
		# sound
		main_sound = pygame.mixer.Sound('./audio/main.ogg')
		main_sound.set_volume(0.5)
		main_sound.play(loops = -1)
	
	def fade_in(self, speed=5):
		fade_surface = pygame.Surface((WIDTH, HEIGTH)).convert()
		fade_surface.fill((0, 0, 0))

		for alpha in range(0, 255 + speed, speed):
			self.screen.fill(WATER_COLOR)
			self.level.run()
			fade_surface.set_alpha(255 - alpha)
			self.screen.blit(fade_surface, (0, 0))
			pygame.display.update()
			self.clock.tick(FPS)


	def run(self):
		self.fade_in()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	menu = Menu()
	menu.run()
	pygame.time.delay(300)
	game.run()	