from BLACKFORGE2 import *

from CONSTANTS import *

class Camera():
    
	def __init__(self, game, player, scroll_speed:int, interpolation:int):
		self.game = game
		self.player = self.game.player
		self.level_scroll = pygame.math.Vector2()
		self.scroll_speed = scroll_speed
		self.interpolation = interpolation

	def horizontal_scroll(self):
		self.level_scroll.x += (
			(
				self.player.rect.centerx - self.level_scroll.x - (HALF_WIDTH - self.player.size.x)
			) / self.interpolation * self.scroll_speed
			)

	def vertical_scroll(self):
		self.level_scroll.y += (
			(
				(self.player.rect.centery - 50) - self.level_scroll.y - (HALF_HEIGHT - self.player.size.y)
			) / self.interpolation * self.scroll_speed
			)

	def pan_cinematic(self):
		pass

	def update_position(self, level_topleft_rect:pygame.Rect, level_bottomright_rect:pygame.Rect, level_width:int, level_height:int, SCREEN_WIDTH:int, SCREEN_HEIGHT:int):
		self.horizontal_scroll()
		self.vertical_scroll()

		# constrain camera movement
		if level_topleft_rect.left + self.level_scroll.x < 0:
			self.level_scroll.x = 0
		elif level_bottomright_rect.right - self.level_scroll.x < SCREEN_WIDTH:
			self.level_scroll.x = level_width - SCREEN_WIDTH

		if level_topleft_rect.top - self.level_scroll.y > 0:
			self.level_scroll.y = 0
		elif level_bottomright_rect.bottom - self.level_scroll.y < SCREEN_HEIGHT:
			self.level_scroll.y = level_height - SCREEN_HEIGHT