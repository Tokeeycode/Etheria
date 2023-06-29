from BLACKFORGE2 import *

from CONSTANTS import *

import time
from camera import Camera
from level import Level
from gamedata import maps
from player import Player

class Game():
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('Etheria')
		self.level = Level(maps[1], self, self.screen)
		self.camera = Camera(self, 6, 100)
		pygame.key.set_repeat(0)
	   
	def event_handler(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.player.attacking = True
					self.player.attack_time = pygame.time.get_ticks()  
					self.player.cooldowns()
		
	def run(self):
		last_time = time.time()
		
		self.running = True
		while self.running:
			self.dt = time.time() - last_time
			self.dt *= 60.0
			last_time = time.time()
			self.screen.fill([140, 160, 200])
			
			self.event_handler()           
			self.level.draw_level(self.screen)
			self.player.update(self.dt)
			self.camera.update_position()
		
			
			self.clock.tick(FPS)
			pygame.display.flip()
			
	
if __name__ == "__main__":
	game = Game()
	game.run()
		
		
		