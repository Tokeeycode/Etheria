from BLACKFORGE2 import *

class Player(Entity):
	def __init__(self, game, size:int, position:tuple, speed:int, groups:list):
		super().__init__(size, position, speed, groups)
		self.game = game
		self.image = get_image('../assests/player/idle/Idle1.png').convert_alpha()
		self.image = scale_images([self.image], (32, 32))[0]
		self.rect = self.image.get_rect(topleft=self.position)
		self.collision_area = pygame.Rect(self.rect.topleft, (96, 96))
	
	def move(self, dt):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.velocity.y = -self.speed * dt
		elif keys[pygame.K_s]:
			self.velocity.y = self.speed * dt
		else:
			self.velocity.y = 0
		if keys[pygame.K_a]:
			self.velocity.x = -self.speed * dt
		elif keys[pygame.K_d]:
			self.velocity.x = self.speed * dt
		else:
			self.velocity.x = 0
   
	def update(self, dt):
		self.move(dt)
		self.rect.x += self.velocity.x
		self.physics.horizontal_movement_collision(self, self.game.level.terrain)
		self.rect.y += self.velocity.y
		self.physics.vertical_movement_collision(self, self.game.level.terrain)
		if self.velocity.magnitude() != 0:
			self.velocity = self.velocity.normalize()