from BLACKFORGE2 import *

from CONSTANTS import *

class Bullet:
    def __init__(self, x, y, game):
        self.game = game
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = get_image('../assets/player/spells/fireball/kenshi1.png')
        self.bullet = scale_images([self.bullet], (32, 32))
        # self.bullet.fill((255, 255, 255))
        self.bullet = pygame.transform.rotate(self.bullet[0], angle)
        self.speed = 5

    def update(self,):  
        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect)