from typing import Self
from BLACKFORGE2 import *

from CONSTANTS import *

class Player(Entity):
	def __init__(self, game, size:int, position:tuple, speed:int, groups:list):
		super().__init__(size, position, speed, groups)
		self.game = game
		self.import_player_assets()
		self.image = get_image('../assets/player/idle_down/Idle1.png')
		self.rect = self.image.get_rect(topleft=self.position)
		self.collision_area = pygame.Rect(self.rect.topleft, (96, 96))
  
		self.status = 'down'
		self.animation = self.animations[self.status]
		self.frame_index = 0
		self.animation_speed = 0.15
  
	def import_player_assets(self):
		self.animations = {'idle_down':[], 'idle_left':[], 'idle_right':[], 'idle_up':[], 'up':[], 'down':[], 'left':[], 'right':[]}

		for animation in self.animations.keys():
			full_path = CHAR_PATH + animation
			self.animations[animation] = import_folder(full_path)
			
			
	def move(self, dt):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.status = 'up'
			self.velocity.y = -self.speed * dt
		elif keys[pygame.K_s]:
			self.status = 'down'
			self.velocity.y = self.speed * dt
		else:
			self.velocity.y = 0
		if keys[pygame.K_a]:
			self.status = 'left'
			self.velocity.x = -self.speed * dt
		elif keys[pygame.K_d]:
			self.status = 'right'
			self.velocity.x = self.speed * dt
		else:
			self.velocity.x = 0
   
	def get_status(self):

		if self.velocity.x == 0 and self.velocity.y == 0:
			if not 'idle' in self.status:
				self.status = 'idle' + '_' + self.status
	
	def animate(self):
		animation = self.animations[self.status]
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		self.rect = self.image.get_rect(center = self.rect.center)
	
	def update(self, dt):
		self.move(dt)
		self.get_status()
		self.animate()
		self.rect.x += self.velocity.x
		self.physics.horizontal_movement_collision(self, self.game.level.terrain)
		self.rect.y += self.velocity.y
		self.physics.vertical_movement_collision(self, self.game.level.terrain)
		if self.velocity.magnitude() != 0:
			self.velocity = self.velocity.normalize()
		self.draw(self.game.screen)
   
	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft - self.game.camera.level_scroll)

		