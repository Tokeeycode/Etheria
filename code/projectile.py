from BLACKFORGE2 import *

from CONSTANTS import *

class Bullet(pygame.sprite.Sprite):
	def __init__(self, game, x, y, type, size, group):
		super().__init__(group)
		self.game = game
		self.position = pygame.math.Vector2(x, y)
		self.type = type
		self.size = size
		self.speed = 9

		mx, my = pygame.mouse.get_pos()
		self.dir = (mx - x, my - y)
		length = math.hypot(*self.dir)
		if length == 0.0:
			self.dir = (0, -1)
		else:
			self.dir = (self.dir[0]/length, self.dir[1]/length)

		self.angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))
		
		# animation 
		self.import_assets()
		self.frame_index = 0
		self.animation = self.animations[self.type]
		self.animation_speed = 0.35
		self.image = self.animations[self.type][self.frame_index]
		self.rect = self.image.get_rect(center = self.position)


	def import_assets(self):
		path = f'../assets/player/spells/'
		self.animations = {f'{self.type}':[],}
		
		for animation in self.animations.keys():
			full_path = path + animation
			self.animations[animation] = scale_images(import_folder(full_path), (self.size, self.size))

	def animate(self):
		animation = self.animations[self.type]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
			
		self.image = pygame.transform.rotate(animation[int(self.frame_index)], self.angle)

	def update(self):
		self.animate()
		self.position = pygame.math.Vector2(self.position[0]+self.dir[0]*self.speed, 
					self.position[1]+self.dir[1]*self.speed)
		self.rect.center = self.position
		

	def draw(self, surf):
		surf.blit(self.image, self.position)

