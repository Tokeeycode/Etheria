from BLACKFORGE2 import *

from CONSTANTS import *

import time
from camera import Camera
from level import Level
from gamedata import maps
from player import Player
from projectile import Bullet

class Game():
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
		pygame.display.set_caption('Etheria')
		self.level = Level(maps[1], self, self.screen)
		self.camera = Camera(self, self.player, 6, 100)
		pygame.key.set_repeat(0)
	   
	def event_handler(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.player.attacking = True
					self.player.attack_time = pygame.time.get_ticks()  
					self.player.cooldowns(PLAYER_ATTACK_COOLDOWN)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F11:
					pygame.display.toggle_fullscreen()
				if event.key == pygame.K_r and not self.player.casting:
					self.player.casting = True
					self.player.projectiles.append(
						Bullet(self, *self.player.hurtbox.topleft, 'fireball', 32, self.level.projectile_group)
					)
					self.player.cooldowns(PLAYER_ATTACK_COOLDOWN)
     		
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
			self.camera.update_position(self.level.level_topleft, self.level.level_bottomright, self.level.level_width, self.level.level_height, SCREEN_WIDTH, SCREEN_HEIGHT)
		
			
			self.clock.tick(FPS)
			pygame.display.flip()
			
	
if __name__ == "__main__":
	game = Game()
	game.run()
		
		
		