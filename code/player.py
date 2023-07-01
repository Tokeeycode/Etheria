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
		self.casting = False
		self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
		self.attack_time = None
		self.projectiles = []

		self.hurtbox = pygame.Rect(self.rect.topleft, (20,20))
  
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
			for projectile in self.projectiles:
				projectile.position.y += PLAYER_SPEED
		elif keys[pygame.K_s] and not self.attacking:
			self.status = 'down'
			self.velocity.y = self.speed * dt
			for projectile in self.projectiles:
				projectile.position.y -= PLAYER_SPEED
		else:
			self.velocity.y = 0
		if keys[pygame.K_a] and not self.attacking:
			self.status = 'left'
			self.velocity.x = -self.speed * dt
			for projectile in self.projectiles:
				projectile.position.x += PLAYER_SPEED
		elif keys[pygame.K_d] and not self.attacking:
			self.status = 'right'
			self.velocity.x = self.speed * dt
			for projectile in self.projectiles:
				projectile.position.x -= PLAYER_SPEED
		else:
			self.velocity.x = 0

	def projectile_handler(self):
		for projectile in self.projectiles:
			projectile.update()
			projectile.draw(self.game.screen)
			# pygame.draw.rect(pygame.display.get_surface(), "red", projectile.rect)
			pass

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
		self.image = pygame.transform.scale(animation[int(self.frame_index)], PLAYER_IMG_SCALING)
		self.rect = self.image.get_rect(center = self.rect.center)
	
	def cooldowns(self, time):
		if int(self.attack_cooldown) <= 0:
			self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
			self.attacking = False
			self.casting = False
			# print("attack cooldown reset")

	def update(self, dt):
		self.move(dt)
		self.get_status()
		self.animate()
		self.projectile_handler()
		self.rect.x += self.velocity.x * dt
		self.physics.horizontal_movement_collision(self, self.game.level.terrain)
		self.rect.y += self.velocity.y * dt
		self.physics.vertical_movement_collision(self, self.game.level.terrain)
		if self.velocity.magnitude() != 0:
			self.velocity = self.velocity.normalize()
		self.draw(self.game.screen)

		""" COOLDOWN TIMER """
		if self.attacking or self.casting and self.attack_cooldown > 0:
			self.attack_cooldown -= 1 * self.game.dt
		self.cooldowns(PLAYER_ATTACK_COOLDOWN)
		# print(self.attack_cooldown, "attack status", self.casting)

		# update hurtbox
		# self.hurtbox.center = self.rect.center
		self.hurtbox.center = self.rect.center - self.game.camera.level_scroll

		print('rect position', self.hurtbox.center)
		
	def draw(self, surface):
		surface.blit(self.image, self.rect.topleft - self.game.camera.level_scroll)
		pygame.draw.rect(self.game.screen, "red", self.rect)
		pygame.draw.rect(self.game.screen, "white", self.hurtbox)

		