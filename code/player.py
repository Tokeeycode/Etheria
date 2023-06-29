from typing import Self
from BLACKFORGE2 import *
from CONSTANTS import *
from projectile import Bullet

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
		self.animation_speed = PLAYER_ANIMATION_SPEED
		self.attacking = False
		self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
		self.attack_time = None
		self.projectiles = []
  
	def import_player_assets(self):
		self.animations = {'idle_down':[], 'idle_left':[], 'idle_right':[], 'idle_up':[], 'up':[], 'down':[], 'left':[], 'right':[], 'attack_up':[], 'attack_down':[], 'attack_left':[], 'attack_right':[]}

		for animation in self.animations.keys():
			full_path = CHAR_PATH + animation
			self.animations[animation] = import_folder(full_path)
   
	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()
			
	
	def move(self, dt):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w] and not self.attacking:
			self.status = 'up'
			self.velocity.y = -self.speed * dt
		elif keys[pygame.K_s] and not self.attacking:
			self.status = 'down'
			self.velocity.y = self.speed * dt
		else:
			self.velocity.y = 0
		if keys[pygame.K_a] and not self.attacking:
			self.status = 'left'
			self.velocity.x = -self.speed * dt
		elif keys[pygame.K_d] and not self.attacking:
			self.status = 'right'
			self.velocity.x = self.speed * dt
		else:
			self.velocity.x = 0

		
	
	def projectile_handler(self):
		for projectile in self.projectiles:
			projectile.draw(self.game.screen)
			projectile.update()

	def get_status(self):
		if self.velocity.x == 0 and self.velocity.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = 'idle' + '_' + self.status
	
		if self.attacking:
			self.velocity.x = 0
			self.velocity.y = 0
			if not 'attack' in self.status:
				self.status = self.status.replace('idle', 'attack')
			else:
				self.status = self.status
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('attack','idle')
	
	def animate(self):
		animation = self.animations[self.status]
		self.frame_index += self.animation_speed * self.game.dt
		if self.frame_index >= len(animation):
			self.frame_index = 0
		self.image = pygame.transform.scale(animation[int(self.frame_index)], (64, 64))
		self.rect = self.image.get_rect(center = self.rect.center)
	
	def cooldowns(self, time):
		current_time = pygame.time.get_ticks()
		
		if self.attacking:
			if current_time - self.attack_time >= time:
				self.attacking = False	 
	def update(self, dt):
		self.move(dt)
		self.get_status()
		self.animate()
		self.cooldowns(PLAYER_ATTACK_COOLDOWN)
		self.projectile_handler()
		self.rect.x += self.velocity.x
		self.physics.horizontal_movement_collision(self, self.game.level.terrain)
		self.rect.y += self.velocity.y
		self.physics.vertical_movement_collision(self, self.game.level.terrain)
		if self.velocity.magnitude() != 0:
			self.velocity = self.velocity.normalize()
		self.draw(self.game.screen)
		if self.attacking:
			self.animation_speed = 0.50
		else:
			self.animation_speed = PLAYER_ANIMATION_SPEED
   
	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft - self.game.camera.level_scroll)

		