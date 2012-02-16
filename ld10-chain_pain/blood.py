import pygame
from random import randint as rand
class Blood:

  def __init__(self, screen, center_pos):
    self.screen = screen
    self.center = center_pos
    self.red = (255, 0, 0)

    self.blank_image = pygame.Surface( (100,100) )
    self.blank_image.set_colorkey( (0, 0, 0) )
    self.render_image = pygame.Surface( (100,100) )
    self.render_image.set_colorkey( (0, 0, 0) )

    self.image = self.blank_image
    self.rect = self.image.get_rect()
    center_pos = [self.center[0] + 64/2, self.center[1] + 64/2]
    self.rect.center = center_pos
    

  def render_blood(self):
    leftx = 0
    lefty = 0 # Left = Top
    rightx = 100
    righty = 100
    off = 20
    # Erase old stuff every so often
    if rand(1, 4) == 4:
      self.render_image.fill( (0, 0, 0) )
    self.image = self.render_image

    for _ in xrange(100):
      randx = rand(0, 100)
      randy = rand(0, 100)
      pos = randx, randy
      if (randx - leftx <= off and randy - lefty <= off) or \
          (randx - leftx <= off and righty - randy <= off) or \
          (rightx - randx <= off and righty - randy <= off) or \
          (rightx - randx <= off and randy - lefty <= off):
        continue # Corners
      pygame.draw.line(self.image, self.red, pos, pos)
